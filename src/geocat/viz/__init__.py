from .taylor import *
from .util import *

# get version from pyproject.toml
from importlib.metadata import version as _version
try:
    __version__ = _version("geocat.viz")
except Exception:
    # Local copy or not installed with setuptools.
    # Disable minimum version checks on downstream libraries.
    __version__ = "999"
