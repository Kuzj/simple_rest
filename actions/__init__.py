from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module
from typing import List

class ActionError(Exception):
    """Base class for exceptions in action."""
    pass

class ActionNotFound(ActionError):
    pass

actions_name_list: List[str] = []
package_dir = Path(__file__).resolve().parent
for (_, module_name, _) in iter_modules([package_dir]):
    import_module(f"{__name__}.{module_name}")
    actions_name_list.append(module_name)
