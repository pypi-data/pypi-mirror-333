import asyncio

from agents import Agent
from openai_moss_agents.moss_tool import MOSSProtocolTool
from openai_moss_agents.example_moss_libs import terminal
from openai_moss_agents.example_moss_libs.terminal_lib import TerminalProvider
from openai_moss_agents.rich_console import run_console_agent

tool = MOSSProtocolTool(
    modulename=terminal.__name__,
    providers=[TerminalProvider()],
)

instruction = tool.with_instruction("assistant for human")

agent = Agent(
    name="jojo",
    instructions=instruction,
    model="gpt-4",
    tools=[tool.as_agent_tool()]
)

if __name__ == "__main__":
    asyncio.run(run_console_agent(agent, "what operating system are you in?"))
