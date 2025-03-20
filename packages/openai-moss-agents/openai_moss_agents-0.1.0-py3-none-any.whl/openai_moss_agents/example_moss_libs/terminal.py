from ghostos_moss import Moss as Parent
from openai_moss_agents.example_moss_libs.terminal_lib.abcd import Terminal


class Moss(Parent):

    terminal: Terminal
    """your terminal """
