from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module
from typing import (Dict, List)
from inspect import (getmembers, isfunction, signature)

class ActionError(Exception):
    """Base class for exceptions in action."""
    pass

class ActionNotFound(ActionError):
    pass

class MethodNotFound(ActionError):
    pass

class ArgumentMissing(ActionError):
    pass

class ActionFormatError(ActionError):
    pass

actions_dict: Dict[str, Dict[str, List[str]]] = {}
package_dir = Path(__file__).resolve().parent
for (_, module_name, _) in iter_modules([package_dir]):
    module = import_module(f"{__name__}.{module_name}")
    module_functions = (f for f in getmembers(module) if isfunction(f[1]))
    function_dict = {}
    for func in module_functions:
        function_dict[func[0]] = list(signature(func[1]).parameters.keys())
    actions_dict[module_name] = function_dict
