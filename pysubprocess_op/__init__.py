try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata
__version__ = importlib_metadata.version(__name__)

print(f"import --> {__name__} ({__version__})")

# need this if use ext via import package: tdpoetry_op.ext
from .ext import Ext1

# these are only avail if import package, cant find them if the ext DAT imports
Folder = __path__[0]
"""str: fullpath to the package folder"""

Tox = f"{Folder}/net.tox"
"""str: fullpath to the tox file"""

