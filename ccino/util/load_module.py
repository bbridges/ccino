import sys
import os.path


PYTHON_3_5 = sys.version_info[0] == 3 and sys.version_info[1] >= 5
PYTHON_3_3 = sys.version_info[0] == 3 and sys.version_info[1] >= 3


if PYTHON_3_5:
    from importlib.util import spec_from_file_location, module_from_spec
elif PYTHON_3_3:
    from importlib.machinery import SourceFileLoader
else:
    from imp import load_source


def load_module(path):
    """Load a module by its path.

    This will not return the module.

    Args:
        path: The filepath of the module.
    """

    file_name = os.path.split(path)[1]

    module_name = os.path.splitext(file_name)[0]

    if PYTHON_3_5:
        spec = spec_from_file_location(module_name, path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
    elif PYTHON_3_3:
        SourceFileLoader(module_name, path).load_module()
    else:
        load_source(module_name, path)
