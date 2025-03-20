import os
import inspect
import importlib.util
from injector import Injector as jInjector, singleton

from ..domain.model import Presentation, Service, Config, Repository


class Injector:
    _injector = jInjector

    def __init__(self, folder_path_to_register: str = ""):
        self._injector = jInjector()
        self._registered_classes = set()
        if folder_path_to_register:
            self.register_all_from_folder(folder_path_to_register)

    def register(self, cls):
        """Registers a class in the injector, ensuring no duplicates."""
        if cls in self._registered_classes:
            return

        print(f"Registering {cls}")
        self._injector.binder.bind(cls, to=cls, scope=singleton)
        self._registered_classes.add(cls)

    def register_all_from_folder(self, folder: str):
        """Registers all classes in a folder in the injector, excluding imported ones."""
        assert isinstance(folder, str), "folder must be a string"
        assert os.path.exists(folder), "folder must exist"
        assert os.path.isdir(folder), "folder must be a directory"

        for root, _, files in os.walk(folder):
            for file in files:
                if not file.endswith(".py") or file == "__init__.py":
                    continue

                module_name = file[:-3]
                module_path = os.path.join(root, file)
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                for _, attr in inspect.getmembers(module, inspect.isclass):
                    if (
                        attr.__module__ == module.__name__
                        and issubclass(
                            attr, (Presentation, Service, Config, Repository)
                        )
                        and attr not in (Presentation, Service, Config, Repository)
                    ):
                        # Ensures class is from this module
                        self.register(attr)

        return self

    def get(self, class_name):
        return self._injector.get(class_name)

    def get_all_by_type(self, base_class):
        """Recursively fetch all unique subclasses of the given base class and return their instances."""

        def get_subclasses(cls):
            """Recursively get all unique subclasses of a class."""
            subclasses = set(cls.__subclasses__())
            for subclass in list(subclasses):
                subclasses.update(get_subclasses(subclass))
            return subclasses

        subclasses = get_subclasses(base_class)
        unique_classes = {cls for cls in subclasses if cls in self._registered_classes}

        return [self.get(cls) for cls in unique_classes]
