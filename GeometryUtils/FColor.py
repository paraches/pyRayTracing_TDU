from GeometryUtil import constrain


class FColor:
    def __init__(self, *args):
        arg_count = len(args)
        if arg_count not in [0, 1, 3]:
            raise ValueError("Constructor's args count is 0 or 1 or 3.")
        if arg_count == 3:
            red = float(args[0])
            green = float(args[1])
            blue = float(args[2])
        elif arg_count == 1:
            red = green = blue = float(args[0])
        else:
            red = green = blue = float(0)
        self.red = red
        self.green = green
        self.blue = blue

    def __add__(self, other):
        return FColor(self.red + other.red, self.green + other.green, self.blue + other.blue)

    def __mul__(self, other):
        return FColor(self.red * other.red, self.green * other.green, self.blue * other.blue)

    def __str__(self):
        return f'[{self.red}, {self.green}, {self.blue}]'

    # original is toColor function to get `color` object.
    def to_pygame_color_tuple(self, r: float = 1.0, g: float = 1.0, b: float = 1.0):
        red = int(255 * constrain(self.red, 0, r))
        green = int(255 * constrain(self.green, 0, g))
        blue = int(255 * constrain(self.blue, 0, b))
        return red, green, blue

    def mult(self, other: float):
        return FColor(self.red * other, self.green * other, self.blue * other)

    def copy(self):
        return FColor(self.red, self.green, self.blue)

    def set(self, r, g, b):
        self.red = float(r)
        self.green = float(g)
        self.blue = float(b)

    @classmethod
    def color_pi(cls, *args):
        res = FColor(1, 1, 1)
        for arg in args:
            res *= arg
        return res
