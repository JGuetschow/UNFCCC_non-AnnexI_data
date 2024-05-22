"""
Define the CRF specifications here for easy access
"""

from .crf2021_specification import CRF2021
from .crf2022_specification import CRF2022
from .crf2023_aus_specification import CRF2023_AUS
from .crf2023_specification import CRF2023
from .crt1_specification import CRT1

__all__ = [
    "CRF2021",
    "CRF2022",
    "CRF2023",
    "CRF2023_AUS",
    "CRT1",
]
