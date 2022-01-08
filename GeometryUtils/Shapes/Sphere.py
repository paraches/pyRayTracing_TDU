from ..PVector import PVector
from ..Ray import Ray
from .Shape import Shape
from ..IntersectionPoint import IntersectionPoint
import math


class Sphere(Shape):
    def __init__(self, center=PVector(), radius: float = 1.0):
        self.center = center.copy()
        self.radius = radius

    def test_intersection(self, ray: Ray):
        # s = ray.start
        # d = ray.direction
        # temp = |s - pc|^2
        tmp = ray.start.sub(self.center).mag()
        # A = |d|^2
        a = ray.direction.mag_sq()
        # B = 2(s dot d - pc dot d)
        b = 2 * (ray.start.dot(ray.direction) - self.center.dot(ray.direction))
        # C = |s - pc|^2 - r^2
        c = tmp ** 2 - self.radius * self.radius
        # D = B^2 - 4AC
        d = b ** 2 - 4 * a * c

        if d < 0:
            return None

        if d == 0:
            t = -b / (2 * a)
        else:
            t_plus = (-b + math.sqrt(d)) / (2 * a)
            t_minus = (-b - math.sqrt(d)) / (2 * a)
            t = min(t_plus, t_minus) if t_plus > 0 and t_minus > 0 else max(t_plus, t_minus)

        if t > 0:
            distance = t * ray.direction.mag()
            position = ray.start.add(ray.direction.mult(t))
            normal = position.sub(self.center).normalize()
            res = IntersectionPoint(distance, position, normal)
            return res
        else:
            return None
