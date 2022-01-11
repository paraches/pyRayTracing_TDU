from ..PVector import PVector
from ..Ray import Ray
from ..IntersectionPoint import IntersectionPoint
from ..Material import Material
from .Shape import Shape


class Plane(Shape):
    def __init__(self, normal=PVector(0, 1, 0), position=PVector(0), material=Material()):
        super(Shape, self).__init__()
        self.material = material
        self.normal = normal.copy().normalize()
        self.position = position.copy()

    def test_intersection(self, ray: Ray):
        dn_dot = ray.direction.dot(self.normal)
        if dn_dot != 0:
            t = (self.position.dot(self.normal) - ray.start.dot(self.normal)) / dn_dot
            if t > 0:
                distance = t * ray.direction.mag()
                position = ray.get_point(t)
                normal = self.normal.copy()
                return IntersectionPoint(distance, position, normal)
        return None
