from .onlyaml import parse
from .readonly_config import ReadonlyDict

# These are the only items accessible when importing the package
__all__ = ["parse", "ReadonlyDict"]
