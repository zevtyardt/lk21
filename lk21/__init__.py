"""cari anime dan film subtitle Indonesia"""

__version__ = "1.5.61"
__author__ = "Val"
__license__ = "MIT"
__all__ = [
    "extractors",
    "Bypass"
]

from .cli import main
from .extractors.bypasser import Bypass
