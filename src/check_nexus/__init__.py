"""
check_i16_nexus files against Diamond NeXus specification
"""

from .check import check_metadata, set_logging_level
from .validate import validate_nexus
from .dat_file_comparison import convert_and_compare_dat

__version__ = '0.2.0'
__date__ = '2024/12/11'

__all__ = ['check_metadata', 'validate_nexus', 'set_logging_level', 'convert_and_compare_dat']
