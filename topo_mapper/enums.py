from enum import Enum


class Feature(Enum):
    FALLS = 0
    PARKING = 1
    TRAIL_JUNCTION = 2
    UNIQUE_FEATURE = 3
    TRAIL_HEAD = 4


def stringToFeature(val: str) -> Feature:
    val = val.upper()

    if val == "FALLS":
        return Feature.FALLS

    if val == "PARKING":
        return Feature.PARKING

    if val == "TRAIL_JUNCTION":
        return Feature.TRAIL_JUNCTION

    if val == "UNIQUE_FEATURE":
        return Feature.UNIQUE_FEATURE

    if val == "TRAIL_HEAD":
        return Feature.TRAIL_HEAD
