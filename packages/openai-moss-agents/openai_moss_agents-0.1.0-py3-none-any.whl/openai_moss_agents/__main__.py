from openai_moss_agents.moss_tool import MOSSProtocolTool


def main() -> None:
    from argparse import ArgumentParser
    import sys
    parser = ArgumentParser()
    parser.add_argument("modulename", help="The name of a python module")
    parsed = parser.parse_args(sys.argv[1:])
    modulename = parsed.modulename

    tool = MOSSProtocolTool(modulename)
    print(tool.with_instruction(""))
