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

MOSS_INTRODUCTION = """
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
    name: str
    description: str
    container: Container
    pycontext: PyContext

    def __init__(
            self,
            modulename: str,
            *,
            real_modulename: Union[str] = None,
            name: str = "moss",
            description: str = (
                    "Useful to execute code in the python context that MOSS provide to you."
                    "The code must include a `run` function."
            ),
            container: Union[Container, None] = None,
            providers: Union[List[Provider], None] = None,
            bindings: Union[Dict[Any, Any], None] = None,
            injections: Union[Callable[[...], Dict[str, Any]], None] = None,
            local_values: Union[Dict[str, Any], None] = None,
            pycontext: Optional[PyContext] = None,
    ):
        self.modulename: str = modulename
        if real_modulename is None:
            real_modulename = modulename
        self.real_modulename = real_modulename
        self.name = name
        self.description = description
        if container is None:
            container = get_container()
        self.container = container
        self.providers = providers
        self.injections = injections
        self.bindings = bindings
        self.local_values = local_values
        if pycontext is None:
            pycontext = PyContext(
                modulename=self.real_modulename,
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
        runtime = self.get_runtime()
        with runtime:
            moss_pom = self._get_moss_instruction_pom(runtime)
            main_pom = TextPOM().with_children(
                TextPOM(
                    title="MOSS Protocol Tool",
                    content=MOSS_META_PROMPT,
                ),
                moss_pom,
                TextPOM(
                    title="Instruction",
                    content=agent_instructions,
                )
            )
            return main_pom.get_prompt(runtime.container())

    def get_moss_instruction(self) -> str:
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
        injections_pom = self.reflect_injections_pom(injections)

        content = MOSS_INTRODUCTION.format(
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
        params = CodeParameter.func_parameters_schema()
        print("+++++++++++++++=", params)
        return FunctionTool(
            name=self.name,
            description=self.description,
            params_json_schema=params,
            on_invoke_tool=self.on_invoke_tool,
        )

    async def on_invoke_tool(self, rc: RunContextWrapper[PyContext], arguments: str) -> str:
        code_arguments = CodeParameter.unmarshall(arguments)
        code = code_arguments.unmarshall_code()

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
                # run the codes.
                result = runtime.execute(target="run", code=code, args=[moss])

                # check operator result
                pycontext = result.pycontext
                # rebind pycontext to session
                rc.pycontext = pycontext
                self.pycontext = pycontext

                # handle std output
                std_output = result.std_output
                return self.wrap_std_output(std_output)

            except Exception as e:
                return self.wrap_error(e)

    def reflect_injections_pom(self, injections_pom: Dict[str, Any]) -> PromptObjectModel:
        properties_pom = TextPOM(
            title="Moss Injected properties",
        )
        for key, injection in injections_pom.items():
            if isinstance(injection, PromptObjectModel):
                properties_pom.add_child(injection)
        return properties_pom

    def wrap_error(self, error: Union[str, Exception]) -> str:
        return f"Error during executing `{self.name}` code: {error}"

    def wrap_std_output(self, std_output: str) -> str:
        return f"`{self.name}` output:\n```text\n{std_output}\n```"
