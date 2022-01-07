from ..PVector import PVector
from ..Ray import Ray
from Shape import Shape


class Sphere(Shape):
    def __init__(self, center=PVector(), radius: float = 1.0):
        self.center = center.copy()
        self.radius = radius

    def test_intersection(self, ray: Ray):
        pass
