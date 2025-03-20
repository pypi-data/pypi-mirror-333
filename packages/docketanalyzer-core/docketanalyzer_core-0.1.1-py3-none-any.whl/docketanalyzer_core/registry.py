import importlib
import inspect
import pkgutil
from typing import Any, Optional
from types import ModuleType


class Registry:
    """
    A registry system that automatically discovers and registers objects based on custom criteria.

    Usage example:

    ```python
    from docketanalyzer import Registry
    from somewhere import SomeBaseClass


    class SomeRegistry(Registry):
        def find_filter(self, obj):
            return (
                isinstance(obj, type) and
                issubclass(obj, SomeBaseClass) and
                obj is not SomeBaseClass
            )


    some_registry = SomeRegistry()

    # Find subclasses of SomeBaseClass in this module
    some_registry.find(recurse=True)

    # Import these into the current namespace
    some_registry.import_registered()
    ```
    """

    def __init__(self) -> None:
        self._registry: dict[str, Any] = {}
        self.module: ModuleType = inspect.getmodule(inspect.stack()[1][0])

    def register(self, name: str, obj: Any) -> None:
        if name in self._registry:
            raise ValueError(f"'{name}' already exists.")
        self._registry[name] = obj

    def get(self, name: str) -> Any:
        if name not in self._registry:
            raise ValueError(f"'{name}' does not exist.")
        return self._registry[name]

    def all(self) -> list[Any]:
        return list(self._registry.values())

    def find_filter(self, obj: Any) -> bool:
        """
        Override this method to define what objects should be registered.
        Should return True for objects that should be included in the registry.
        """
        raise NotImplementedError(
            "Subclasses must implement find_filter() to define registration criteria."
        )

    def find(self, module: Optional[ModuleType] = None, recurse: bool = False) -> None:
        """
        Find and register all objects in the module that match the registration criteria.
        """
        if module is None:
            module = self.module
        if isinstance(module, str):
            module = importlib.import_module(module)
        for _, submodule_name, _ in pkgutil.walk_packages(module.__path__):
            submodule = importlib.import_module(f"{module.__name__}.{submodule_name}")
            for name in dir(submodule):
                obj = getattr(submodule, name)
                if recurse and isinstance(obj, importlib.machinery.ModuleSpec):
                    next_module = importlib.util.module_from_spec(obj)
                    if hasattr(next_module, "__path__"):
                        self.find(module=next_module)
                if self.find_filter(obj) and name not in self._registry:
                    self.register(name, obj)

    def import_registered(self) -> None:
        """
        Import the registered classes into the current module's namespace.
        """
        for cls in self.all():
            setattr(self.module, cls.__name__, cls)
