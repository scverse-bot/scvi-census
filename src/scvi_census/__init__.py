from importlib.metadata import version

from . import data, model

__all__ = ["data", "model"]

__version__ = version("scvi-census")
