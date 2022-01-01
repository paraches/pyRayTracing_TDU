import math
from numbers import Number


class PVector:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f'[{self.x}, {self.y}, {self.z}]'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def add(self, other):
        return PVector(self.x + other.x, self.y + other.y, self.z + other.z)

    def sub(self, other):
        return PVector(self.x - other.x, self.y - other.y, self.z - other.z)

    def mult(self, other):
        return PVector(self.x * other, self.y * other, self.z * other)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return PVector(self.y * other.z - self.z * other.y,
                       self.z * other.x - self.x * other.z,
                       self.x * other.y - self.y * other.x)

    def mag(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def mag_sq(self):
        return self.x * self.x + self.y * self.y + self.z * self.z

    def normalize(self):
        mag = self.mag()
        return PVector(self.x / mag, self.y / mag, self.z / mag)

    def copy(self):
        return PVector(self.x, self.y, self.z)

    @classmethod
    def sigma(cls, *args):
        result = PVector(0, 0, 0)
        i = 0
        while i < len(args):
            if isinstance(args[i], Number):
                if i+1 > len(args)-1 or not isinstance(args[i+1], cls):
                    raise TypeError()
                else:
                    k = args[i]
                    v = args[i+1]
                    result = result.add(v.mult(k))
                    i += 2
            elif isinstance(args[i], cls):
                result = result.add(args[i])
                i += 1
            else:
                raise TypeError(f'{type(args[i])} is wrong type')
        return result
