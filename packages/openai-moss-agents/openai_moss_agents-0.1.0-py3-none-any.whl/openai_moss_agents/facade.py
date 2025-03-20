from typing import Optional, Dict, Any, List, Union
from ghostos_container import Container, Provider, provide
from ghostos_moss import (
    DefaultMOSSProvider, MossCompiler, MossRuntime,
    PyContext,
)

__all__ = [
    'get_container',
    'set_container',
    'compile_moss_runtime',
    'get_moss_compiler',
    'bootstrap_container',
    'Container', 'Provider', 'provide',
]

_container: Optional[Container] = None


def get_container() -> Container:
    """
    get global ioc container
    """
    global _container
    if _container is None:
        container = Container(name="langchain-moss")
        container.register(DefaultMOSSProvider())
        _container = container
        _container.bootstrap()
    return _container


def set_container(container: Container) -> None:
    """
    set global ioc container
    """
    global _container
    _container = container


def bootstrap_container(container: Container) -> None:
    """
    bootstrap a container and set it as global ioc container
    :param container:
    """
    container.bootstrap()
    set_container(container)


def get_moss_compiler(container: Optional[Container] = None) -> MossCompiler:
    """
    get moss compiler from the  ioc container
    :param container: if None, use global ioc container
    :return: MossCompiler
    """
    if container is None:
        container = get_container()
    return container.force_fetch(MossCompiler)


def compile_moss_runtime(
        modulename: Union[str, None] = None,
        *,
        container: Optional[Container] = None,
        providers: List[Provider] = None,
        bindings: Dict[Any, Any] = None,
        local_values: Dict[str, Any] = None,
        injections: Dict[str, Any] = None,
        pycontext: PyContext = None,
) -> MossRuntime:
    """
    syntax sugar to get moss runtime
    moss compile python code to a temporary module, and can run code inside it.
    So MossRuntime is python module level interpreter.

    :param modulename: the compiled temporary modulename
    :param container: the ioc container for moss, if none, use global ioc container
    :param providers: the providers for MossRuntime.container() which inherit the global ioc container
    :param bindings: set bindings to the MossRuntime.container() by key / value
    :param local_values: replaced the compiled module's local values by key
    :param injections: the injections for `Moss` class in the module. if none, use ioc container for dynamic injections.
    :param pycontext: the pycontext keep the long-term variables for Moss class in the compiled module.
                      save the pycontext at somewhere can keep the long-term variables.
    :return:  MossRuntime to execute new code with python context.
    """
    compiler = get_moss_compiler(container)
    if pycontext:
        compiler = compiler.join_context(pycontext)

    if providers:
        for p in providers:
            compiler.register(p)
    if bindings:
        for key, val in bindings.items():
            compiler.bind(key, val)

    if local_values:
        compiler = compiler.with_locals(**local_values)

    if injections:
        compiler = compiler.injects(**injections)

    with compiler:
        return compiler.compile(modulename)
