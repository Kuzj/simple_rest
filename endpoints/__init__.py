from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module
from typing import List
from types import ModuleType

endpoints_list: List[ModuleType] = []
package_dir = Path(__file__).resolve().parent
for (_, module_name, _) in iter_modules([package_dir]):
    endpoints_list.append(import_module(f"{__name__}.{module_name}"))
