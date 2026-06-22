"""QBot command limit helpers."""


def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))
