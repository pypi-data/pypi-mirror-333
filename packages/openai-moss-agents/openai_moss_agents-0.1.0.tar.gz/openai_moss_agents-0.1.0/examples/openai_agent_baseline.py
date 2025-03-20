import asyncio

from agents import Agent
from openai_moss_agents.moss_tool import MOSSProtocolTool
from openai_moss_agents.rich_console import run_console_agent
from openai_moss_agents.example_moss_libs import math_lib

tool = MOSSProtocolTool(
    # use the math_lib's source code for LLM context.
    modulename=math_lib.__name__,
)

instruction = tool.with_instruction("assistant for human")

agent = Agent(
    name="jojo",
    instructions=instruction,
    model="gpt-4",
    tools=[tool.as_agent_tool()]
)

if __name__ == "__main__":
    asyncio.run(run_console_agent(agent, "(293324 + 2934320) * 12343 = ?", debug=False))
