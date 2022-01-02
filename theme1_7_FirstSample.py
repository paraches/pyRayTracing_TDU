from PVector import PVector


def map_range(value: float, in_min: float, in_max: float, out_min: float, out_max: float):
    return out_min + (((value - in_min) / (in_max - in_min)) * (out_max - out_min))


def theme1_7_first_sample():
    # screen size
    width = 512
    height = 512

    # Scene setting
    pe = PVector(0, 0, -5)
    pc = PVector(0, 0, 5)
    r = 1.0

    # loop
    for y in range(height):
        for x in range(width):
            pw = PVector(map_range(x, 0, width, 0, height), map_range(y, 0, width, 0, height), 0)
            de = pw.sub(pe)


