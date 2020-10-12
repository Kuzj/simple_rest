from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module

class ActionError(Exception):
    """Base class for exceptions in action."""
    pass

class ActionNotFound(ActionError):
    pass

actions_list = []
package_dir = Path(__file__).resolve().parent
for (_, module_name, _) in iter_modules([package_dir]):
    import_module(f"{__name__}.{module_name}")
    actions_list.append(module_name)
