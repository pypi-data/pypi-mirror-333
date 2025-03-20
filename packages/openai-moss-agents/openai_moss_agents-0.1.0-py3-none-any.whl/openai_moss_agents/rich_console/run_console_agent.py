try:
    import rich
except ImportError:
    raise ImportError(f'Please install Rich with `pip install "openai-moss-agents[console]"` or `pip install rich`')

from typing import Union
from agents import Agent, Runner
from openai.types.responses.response_stream_event import (
    ResponseFunctionCallArgumentsDoneEvent
)
from pydantic import BaseModel
from rich.prompt import Prompt
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
import json


async def run_console_agent(agent: Agent, query: Union[str, None] = None, debug: bool = False) -> None:
    console = Console()
    console.print(Panel(
        Markdown(agent.instructions),
        title=f"Agent {agent.name} Instructions",
    ))
    console.print(Panel(
        "print /quit to quit",
        title="help"
    ))
    while True:
        if query:
            prompt = query
            console.print(query)
            query = None
        else:
            prompt = Prompt.ask("<<<")
        if prompt == "/quit":
            break
        console.print("\n")

        response = Runner.run_streamed(agent, prompt)
        console.print("AI >>>: \n")

        item_id = ""
        async for event in response.stream_events():
            if debug and hasattr(event, "data") and isinstance(event.data, BaseModel):
                console.print("\n")
                console.print_json(event.data.model_dump_json())
            elif hasattr(event, "data") and hasattr(event.data, "delta"):
                if item_id != event.data.item_id:
                    console.print("\n")
                item_id = event.data.item_id
                console.print(event.data.delta, end="")

        console.print("\n")
        console.print(Panel(
            Markdown(response.final_output),
            title="AI",
        ))
