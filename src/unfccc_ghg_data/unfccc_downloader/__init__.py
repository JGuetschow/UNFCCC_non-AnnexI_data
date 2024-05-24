"""
Download submissions from the UNFCCC website

Collection of scripts and helper functions to download different types of sumbissions
from the UNFCCC website.
"""
from .unfccc_submission_info import get_BTR_name_and_URL, get_unfccc_submission_info

__all__ = [
    "get_unfccc_submission_info",
    "get_BTR_name_and_URL",
]
