C_EPSILON: float = 1.0 / 512.0


def map_range(value: float, in_min: float, in_max: float, out_min: float, out_max: float):
    return out_min + (((value - in_min) / (in_max - in_min)) * (out_max - out_min))


def constrain(value: float, min_value: float = 0.0, max_value: float = 1.0):
    return min(max_value, max(min_value, value))
