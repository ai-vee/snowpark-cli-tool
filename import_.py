import sys
import types

from aivee_dev_tools.files import load_file_as_text
from aivee_dev_tools.path_management import  find_paths
from aivee_dev_tools.exceptions import ValidationError
from aivee_dev_tools.logger import Logger

logger = Logger.logger

def import_module(
    module_name: str = None,
    module_file: str = None
) -> types.ModuleType:
    mod = types.ModuleType(module_name)
    mod.__file__ = module_file

    # add ref in sys.modules
    sys.modules[module_name] = mod

    # read src code
    src_code = load_file_as_text(module_file)

    # compile src code
    compiled_code= compile(
        src_code,
        filename=module_file,
        mode='exec'
    )

    # exec compiled code and stored its global namespace
    exec(compiled_code, mod.__dict__)

    return mod
