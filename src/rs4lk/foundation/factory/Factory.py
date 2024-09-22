import importlib
from typing import Any

from ..exceptions import ClassNotFoundError


def class_for_name(module_name: str, class_name: str) -> Any:
    m = importlib.import_module(module_name + "." + class_name)
    camel_case_class_name = "".join(map(lambda x: x.capitalize(), class_name.split('_'))) \
        if '_' in class_name else class_name
    return getattr(m, camel_case_class_name)


class Factory(object):
    __slots__ = ['module_template', 'name_template']

    def get_module_name(self, args: tuple) -> str:
        return self.module_template % args

    def get_class_name(self, args: tuple) -> str:
        return self.name_template % args

    def get_class(self, module_args: tuple = (), class_args: tuple = ()) -> Any:
        module_name = self.get_module_name(module_args)
        class_name = self.get_class_name(class_args)

        try:
            return class_for_name(module_name, class_name)
        except ImportError as e:
            if e.name == "%s.%s" % (module_name, class_name):
                raise ClassNotFoundError
            else:
                raise ImportError from e

    def create_instance(self, module_args: tuple = (), class_args: tuple = ()) -> Any:
        return self.get_class(module_args, class_args)()
