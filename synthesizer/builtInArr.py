from array import array
from enum import Enum


class ArrType(Enum):
    #                     dtype         bytes size
    int8 = "b"      # signed integer        1
    uint8 = "B"     # unsigned integer      1

    int16 = "i"     # signed integer        2
    uint16 = "I"    # unsigned integer      2

    int32 = "l"     # signed integer        4
    uint32 = "L"    # unsigned integer      4

    int64 = "q"     # signed integer        8
    uint64 = "Q"    # unsigned integer      8

    float = "f"     # floating-point        4
    double = "d"    # floating-point        8

    # "h"             signed integer        2
    # "H"             unsigned integer      2


def createArray(dt: ArrType, size: int, init: int | float = 0) -> array:
    return array(dt.value, (init for _ in range(size)))
