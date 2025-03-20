import asyncio

from agents import Runner, Agent
from openai_moss_agents.moss_tool import MOSSProtocolTool
from openai_moss_agents.example_moss_libs import math_lib


async def main():
    tool = MOSSProtocolTool(
        math_lib.__name__,
    )

    instruction = tool.with_instruction("assistant for human")
    print(instruction)

    agent = Agent(
        name="jojo",
        instructions=instruction,
        model="gpt-4-turbo",
        tools=[tool.as_agent_tool()]
    )

    result = Runner.run_streamed(agent, "hello, (12343 + 293439) * 1220 = ?")
    async for event in result.stream_events():
        print(event)

    return result.final_output


if __name__ == "__main__":
    r = asyncio.run(main())
    print(r)
