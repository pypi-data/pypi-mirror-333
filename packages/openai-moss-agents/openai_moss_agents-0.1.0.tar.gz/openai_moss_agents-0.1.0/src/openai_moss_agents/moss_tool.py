from typing import Union, List, Callable, Optional, Dict, Any
from agents import FunctionTool
from typing_extensions import Self
from openai_moss_agents.facade import get_container, compile_moss_runtime
from ghostos_moss import PyContext, MossRuntime
from ghostos_common.prompter import PromptObjectModel, TextPOM
from ghostos_container import Container, Provider
from pydantic import BaseModel, Field
from agents import RunContextWrapper

__all__ = [
    "MOSSProtocolTool", "CodeParameter", "MOSS_META_PROMPT",
]

# Moss Meta Prompt for agent using `moss protocol tool`
MOSS_META_PROMPT = """
You are equipped with the MOSS (Model-oriented Operating System Simulator).
Which provides you a way to control your body / tools / thoughts through Python code.

basic usage: 
1. MOSS protocol are wrapped into `moss protocol tool`, you can generate code with them.
2. each `moss protocol tool` will provide you a python module context (MOSS context).
3. the code you generated in `moss protocol tool`, will be executed by the tool's MOSS interpreter.

the python code you generated with `moss protocol tool`, must include a `run` function, follow the pattern:
```python
def run(moss: Moss):
    \"""
    :param moss: instance of the class `Moss`, the properties on it will be injected with runtime implementations.
    :return: None
    \"""
```

Then the MOSS system will append your code to the python module context that provided to you, 
and execute the `run` function. 
The stdout (like print(...) ) will send to you as message. 

Notices: 
* Your code will **APPEND** to the MOSS context, so **DO NOT REPEAT THE DEFINED CODE ALREADY IN THE MODULE**.
* if the python code context can not fulfill your will, do not use the tool.
* you can reply as usual without calling the moss protocol tool. use it only when you know what you're doing.
* in your code generation, comments is not required, comment only when necessary.
* never call the `run` function in your code generation. Let the MOSS interpreter do so.
"""

# the instruction tell agent about the moss tool's python context.
MOSS_CONTEXT_INTRODUCTION = """
The python context `{modulename}` that moss protocol tool `{tool_name}` provides to you are below:

```python
{source_code}
```

interfaces of some imported attrs are:
```python
{imported_attrs_prompt}
```

{magic_prompt_info}
"""


class CodeParameter(BaseModel):
    """
    the function call parameters for llm, from `moss protocol tool`
    """
    code: str = Field(
        description="the python code (only) that executed in the moss module context. ",
    )

    @classmethod
    def unmarshall(cls, arguments: str) -> Self:
        return cls.model_validate_json(arguments)

    def unmarshall_code(self) -> str:
        code = self.code
        if code.startswith("```python"):
            code = code[len("```python"):]
        if code.startswith("```"):
            code = code[len("```"):]
        if code.endswith("```"):
            code = code[:-len("```")]
        return code.strip()

    @classmethod
    def func_parameters_schema(cls) -> Dict[str, Any]:
        parameters = cls.model_json_schema()
        if parameters is None:
            parameters = {"type": "object", "properties": {}}
        properties = parameters.get("properties", {})
        params_properties = {}
        for key in properties:
            _property = properties[key]
            if "title" in _property:
                del _property["title"]
            params_properties[key] = _property
        parameters["properties"] = params_properties
        if "title" in parameters:
            del parameters["title"]
        parameters["additionalProperties"] = False
        return parameters


class MOSSProtocolTool:
    """
    The Tool based on MOSS Protocol, to provide python interface for openai-agent

    With MossProtocolTool, most python module can directly provide to the LLM,
    and the LLM code generation can be executed by MossRuntime in a temporary python ModuleType instance.

    MOSS (model-oriented operating system simulator) Protocol does four things:
    1. Reflect python code:
        (usually from a python module) into prompt for LLM,
        let it understand how to use the provided libraries.
    2. Runtime injection:
        if the python code has a class Named `Moss` and extends `ghostos_moss.Moss`,
        all the properties defined on it will be dynamic injected from IoC Container, or manually provided injections.
    3. Execute the code:
        The LLM code generation in the `moss protocol tool` will be executed in the python code context.
        The code generation will be appended to the tail of the origin code, and be executed.
    4. Context Managing:
        The data types like `int`, `str`, `bool`, `float`, `BaseModel` ... bound to the Moss class,
        will be saved into the PyContext, and restore from it.
        So in multi-turns conversation, the pycontext can keep long-term variables available for LLMs.
    """

    name: str
    description: str
    container: Container
    pycontext: PyContext

    def __init__(
            self,
            modulename: Union[str, None] = None,
            *,
            source_modulename: Union[str, None] = None,
            name: str = "moss",
            description: str = (
                    "Useful to execute code in the python context that MOSS provide to you."
                    "The code must include a `run` function."
            ),
            code: Union[str, None] = None,
            container: Union[Container, None] = None,
            providers: Union[List[Provider], None] = None,
            bindings: Union[Dict[Any, Any], None] = None,
            injections: Union[Callable[[...], Dict[str, Any]], None] = None,
            local_values: Union[Dict[str, Any], None] = None,
            pycontext: Optional[PyContext] = None,
    ):
        """
        :param modulename:  the modulename for the compiled module. if none, use "__moss__" instead.
        :param source_modulename:  if not given, tool read source from modulename; otherwise read from real_modulename.
        :param code: if given, use the code instead of source from module for the pycontext.
        :param name: name of this tool. there may be multiple `moss protocol tool` for one Agent.
        :param description: description of this tool.
        :param container: If is None, use global IoC Container in openai_moss_agents.facade
        :param providers: the ioc container providers for the MossRuntime.container() only.
        :param bindings: the ioc container singletons for the MossRuntime.container() only.
        :param injections: defines the injections for the `Moss` class in the module,
                           instead of dependency injection from MossRuntime.container()
        :param local_values: defines the local values to replace the compiled module.__dict__ .
                             for example, use can replace the `print`, `os` and `sys` in the module.
        :param pycontext: long-term variables for the `Moss` class in the module.


        How to use MossProtocolTool?

        instruction = tool.with_instruction("assistant for human") # prepare instruction with moss prompt.
        agent = Agent(
            name="jojo",
            instructions=instruction,
            model="gpt-4",
            tools=[tool.as_agent_tool()]  # provide moss protocol tool to the agent.
        )
        """
        self.modulename: str = modulename
        if source_modulename is None:
            source_modulename = modulename
        self.source_modulename = source_modulename
        self.name = name
        self.description = description
        if container is None:
            container = get_container()
        self.container = container
        self.providers = providers
        self.injections = injections
        self.bindings = bindings
        self.local_values = local_values

        self.compile_modulename = modulename
        if modulename is None:
            self.compile_modulename = "__moss__"
        if pycontext is None:
            pycontext = PyContext(
                modulename=self.source_modulename,
                code=code,
            )
        self.pycontext = pycontext

    def get_runtime(self, pycontext: Optional[PyContext] = None) -> MossRuntime:
        """
        get moss runtime.
        :param pycontext: the moss context keep long-term variables.
        :return: MossRuntime which can execute code with the pycontext.
        """
        return compile_moss_runtime(
            self.modulename,
            providers=self.providers,
            bindings=self.bindings,
            local_values=self.local_values,
            injections=self.injections,
            pycontext=pycontext,
        )

    def with_instruction(self, agent_instructions: str) -> str:
        """
        build agent instruction with moss meta instruction and tool instruction.
        :param agent_instructions: agent origin instruction.
        """
        runtime = self.get_runtime()
        with runtime:
            moss_pom = self._get_moss_instruction_pom(runtime)
            main_pom = TextPOM().with_children(
                TextPOM(
                    title="MOSS Protocol Tool",
                    content=MOSS_META_PROMPT,
                ).with_children(
                    moss_pom,
                ),
                TextPOM(
                    title="Instruction",
                    content=agent_instructions,
                )
            )
            return main_pom.get_prompt(runtime.container())

    def get_moss_instruction(self) -> str:
        """
        :return: the moss tool python context prompt.
        """
        runtime = self.get_runtime()
        with runtime:
            pom = self._get_moss_instruction_pom(runtime)
            return pom.get_prompt(runtime.container())

    def _get_moss_instruction_pom(self, runtime: MossRuntime) -> PromptObjectModel:
        prompter = runtime.prompter()
        source_code = prompter.get_source_code()
        imported_attrs_prompt = prompter.get_imported_attrs_prompt()
        magic_prompt = prompter.get_magic_prompt()
        magic_prompt_info = ""
        if magic_prompt:
            magic_prompt_info = f"more information about the module:\n```text\n{magic_prompt}\n```\n"

        injections = runtime.moss_injections()
        injections_pom = self._reflect_injections_pom(injections)

        content = MOSS_CONTEXT_INTRODUCTION.format(
            tool_name=self.name,
            modulename=runtime.module().__name__,
            source_code=source_code,
            imported_attrs_prompt=imported_attrs_prompt,
            magic_prompt_info=magic_prompt_info,
        )
        pom = TextPOM(
            title=f"Moss Protocol Tool `{self.name}`",
            content=content,
        )
        pom.add_child(injections_pom)
        return pom

    def as_agent_tool(self) -> FunctionTool:
        """
        wrap the `moss protocol tool` into openai-agent's tool
        """
        params = CodeParameter.func_parameters_schema()
        return FunctionTool(
            name=self.name,
            description=self.description,
            params_json_schema=params,
            on_invoke_tool=self.on_invoke_tool,
        )

    async def on_invoke_tool(self, rc: RunContextWrapper[PyContext], arguments: str) -> str:
        """
        the invoker for the openai-agent
        :param rc: run context wrapper
        :param arguments: the generated tool arguments.
        :return: stdout or errors after execute the LLM code generation.
        """

        # unmarshal the llm tool arguments into code.
        code_arguments = CodeParameter.unmarshall(arguments)
        code = code_arguments.unmarshall_code()

        # if pycontext is bound to the agent context, use it.
        pycontext = rc.context
        if pycontext is None:
            pycontext = self.pycontext

        runtime = self.get_runtime(pycontext)
        with runtime:

            # if code is not exists, inform the llm
            error = runtime.lint_exec_code(code)
            if error:
                return self.wrap_error(f"the moss code has syntax errors:\n{error}")

            moss = runtime.moss()
            try:
                # run the codes, and pass the `moss` instance from the `Moss` class to the `run` function.
                result = runtime.execute(target="run", code=code, args=[moss])

                # check operator result
                pycontext = result.pycontext
                # rebind pycontext to session
                rc.pycontext = pycontext
                self.pycontext = pycontext

                # handle std output, wrap it for llm
                std_output = result.std_output
                return self.wrap_std_output(std_output)

            except Exception as e:
                return self.wrap_error(e)

    @staticmethod
    def _reflect_injections_pom(moss_injections: Dict[str, Any]) -> PromptObjectModel:
        """
        read all the injections on the `moss` instance,
        and generate property prompt from the PromptObjectModel bound to it.

        :param moss_injections: the injections for the `Moss` class.
        :return:
        """
        properties_pom = TextPOM(
            title="Moss Injected properties",
        )
        for key, injection in moss_injections.items():
            if isinstance(injection, PromptObjectModel):
                properties_pom.add_child(injection)
        return properties_pom

    def wrap_error(self, error: Union[str, Exception]) -> str:
        """
        rewrite this method to wrap an error message.
        """
        return f"Error during executing `{self.name}` code: {error}"

    def wrap_std_output(self, std_output: str) -> str:
        """
        rewrite this method to wrap an output message.
        """
        return f"`{self.name}` output:\n```text\n{std_output}\n```"
