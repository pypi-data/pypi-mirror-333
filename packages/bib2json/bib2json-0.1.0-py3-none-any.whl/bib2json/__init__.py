"""
Bib2JSON converter for BibTeX to JSON conversion
"""

from .converter import convert_file, convert_string

__version__ = "0.1.0"
__all__ = ["convert_file", "convert_string"]