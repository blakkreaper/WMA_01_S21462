from enum import Enum


class ProcessingType(Enum):

    TRACKER = 1
    RAW = 0
    HUE = 2
    SATURATION = 3
    VALUE = 4
    MASK = 5