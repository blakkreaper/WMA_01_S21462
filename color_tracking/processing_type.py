"""
This an example of object tracking (we are not expecting more than
one object on the same recording).
"""

from enum import Enum


class ProcessingType(Enum):
    """
    Enum class representing the types of processes that can be done for frames.
    """

    TRACKER = 1
    RAW = 0
    HUE = 2
    SATURATION = 3
    VALUE = 4
    MASK = 5
