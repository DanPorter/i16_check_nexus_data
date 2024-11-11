"""
check_i16_nexus files against Diamond NeXus specification
"""

from .check import check_metadata, set_logging_level
from .validate import validate_nexus

__version__ = '0.1.1'
__date__ = '2024/11/11'

__all__ = ['check_metadata', 'validate_nexus', 'set_logging_level']
