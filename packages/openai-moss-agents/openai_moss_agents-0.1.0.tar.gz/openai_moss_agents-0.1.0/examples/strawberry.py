import asyncio

from agents import Agent
from openai_moss_agents.moss_tool import MOSSProtocolTool
from openai_moss_agents.rich_console import run_console_agent

# tool without any module, working as python interpreter
tool = MOSSProtocolTool()

instruction = tool.with_instruction("assistant for human")

moss_agent = Agent(
    name="moss_agent",
    instructions=instruction,
    model="gpt-4o",
    tools=[tool.as_agent_tool()]
)

if __name__ == "__main__":
    asyncio.run(run_console_agent(moss_agent, "how many r in strawberry? count them by moss", debug=False))
