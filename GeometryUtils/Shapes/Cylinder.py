import math
from .Shape import Shape
from ..Ray import Ray
from ..PVector import PVector
from ..Material import Material
from ..IntersectionPoint import IntersectionPoint


class Cylinder(Shape):
    def __init__(self, center=PVector(), radius=1.0, height=2.0, material=Material()):
        super(Cylinder, self).__init__()
        self.center = center
        self.radius = radius
        self.height = height
        self.material = material

    def test_intersection(self, ray: Ray):
        # A = |dM|^2
        # B = 2(dM dot mM)
        # C = |mM|^2 - r^2
        # M = |1 0 0|
        #     |0 0 0|
        #     |0 0 1|
        # m = s - pc
        dv = ray.direction
        dvmv = PVector(dv.x, 0, dv.z)
        a = dvmv.mag_sq()
        m = ray.start.sub(self.center)
        mmv = PVector(m.x, 0, m.z)
        b = 2 * dvmv.dot(mmv)
        c = mmv.mag_sq() - self.radius ** 2
        d = b ** 2 - 4 * a * c

        if d < 0:
            return None
        elif d == 0:
            t = -b / (2 * a)
        else:
            t_plus = (-b + math.sqrt(d)) / (2 * a)
            t_minus = (-b - math.sqrt(d)) / (2 * a)
            t = min(t_plus, t_minus) if t_plus > 0 and t_minus > 0 else max(t_plus, t_minus)

        if t > 0:
            distance = t * ray.direction.mag()
            position = ray.start.add(ray.direction.mult(t))
            y_delta = position.y - self.center.y
            if (-self.height / 2) <= y_delta <= self.height / 2:
                nx = 2 * (position.x - self.center.x)
                ny = 0
                nz = 2 * (position.z - self.center.z)
                normal = PVector(nx, ny, nz)
                return IntersectionPoint(distance, position, normal)

        return None
