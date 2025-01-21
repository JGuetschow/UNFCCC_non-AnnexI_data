"""
Define the CRF specifications here for easy access
"""

from .crf2021_specification import CRF2021
from .crf2022_specification import CRF2022
from .crf2023_aus_specification import CRF2023_AUS
from .crf2023_specification import CRF2023
from .crf2024_specification import CRF2024
from .crt1_specification import CRT1
from .crt1_tun_specification import CRT1_TUN
from .ctf1_specification import CTF1

__all__ = [
    "CRF2021",
    "CRF2022",
    "CRF2023",
    "CRF2023_AUS",
    "CRF2024",
    "CRT1",
    "CRT1_TUN",
    "CTF1",
]
