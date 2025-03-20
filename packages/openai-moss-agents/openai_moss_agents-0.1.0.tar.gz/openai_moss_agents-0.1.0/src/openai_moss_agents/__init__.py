from openai_moss_agents.facade import (
    get_container,
    set_container,
    compile_moss_runtime,
    get_moss_compiler,
    bootstrap_container,
    Container, Provider, provide,
)

from openai_moss_agents.moss_tool import (
    MOSS_META_PROMPT,
    MOSSProtocolTool,
    CodeParameter,
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agents import Agent


def agent_with_python_interpreter(name: str, instruction: str) -> "Agent":
    """
    simple example for create an agent with python interpreter
    :param name: agent name
    :param instruction: agent origin instruction
    """
    from agents import Agent
    moss_pure_python_interpreter = MOSSProtocolTool()
    instruction = moss_pure_python_interpreter.with_instruction(instruction)
    agent = Agent(name=name, instructions=instruction, tools=[moss_pure_python_interpreter.as_agent_tool()])
    return agent
