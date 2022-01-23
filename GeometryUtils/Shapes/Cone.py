import math
from .Shape import Shape
from ..Ray import Ray
from ..PVector import PVector
from ..Material import Material
from ..IntersectionPoint import IntersectionPoint


class Cone(Shape):
    def __init__(self, center=PVector(), radius=1.0, height=1.0, material=Material()):
        super(Shape, self).__init__()
        self.center = center.copy()
        self.radius = radius
        self.height = height
        self.material = material

    def test_intersection(self, ray: Ray):
        #   EX-4-EX
        #
        #   bottom normal = (0, -1, 0)
        bottom_normal = PVector(0, -1, 0)
        #   test intersection with ray and bottom
        dn_dot = ray.direction.dot(bottom_normal)
        bottom_intersection_point = None
        if dn_dot != 0:
            t = (self.center.dot(bottom_normal) - ray.start.dot(bottom_normal)) / dn_dot
            if t > 0:
                bottom_position = ray.get_point(t)
                if bottom_position.sub(self.center).mag() <= self.radius:
                    bottom_distance = t * ray.direction.mag()
                    bottom_intersection_point = IntersectionPoint(bottom_distance, bottom_position, bottom_normal)

        #   test intersection with ray and cone
        #
        #   bottom center pc = (cx, cy, cz)
        #   radius r
        #   height h
        #   (x - cx)^2 + (z-cz)^2 = (r/h)^2(y - cy - h)^2
        #
        #   x = sx + tdx, y = sy + tdy, z = sz + tdz
        #
        #   Use following Vector version in Hint-2
        dv = ray.direction
        #   |(pv - pc - hv)M|^2 = 0
        #   pv = sv + tdv
        #
        #   hv = (0)
        #        (h)
        #        (0)
        hv = PVector(0, self.height, 0)
        #   M = (1   0   0)
        #       (0 ri/h  0)
        #       (0   0   1)
        #
        #   |(sv + tdv - pc - hv)M|^2 = 0
        #   |(tdv + sv - pc - hv)M|^2 = 0
        #   mv = sv - pc - hv
        m = ray.start.sub(self.center).sub(hv)
        #   |(tdv + m) dot M|^2 = 0
        #   |tdvM + mvM|^2 = 0
        #   |dvM|^2t^2 + 2(dvM dot mvM)t + |mvM|^2 = 0
        #   A = |dvM|^2
        a = dv.x * dv.x - (dv.y * self.radius / self.height) ** 2 + dv.z * dv.z
        #   B = 2(dvM dot mvM)
        b = 2 * (dv.x * m.x - (dv.y * self.radius / self.height * m.y * self.radius / self.height) + dv.z * m.z)
        #   C = |mvM|^2
        c = m.x * m.x - (m.y * self.radius / self.height) ** 2 + m.z * m.z
        # D = B^2 - 4AC
        d = b * b - 4 * a * c

        if d < 0:
            return bottom_intersection_point

        if d == 0:
            t = float(-b / (2 * a))
        else:
            t_plus = (-b + math.sqrt(d)) / (2 * a)
            t_minus = (-b - math.sqrt(d)) / (2 * a)
            t = min(t_plus, t_minus) if t_plus > 0 and t_minus > 0 else max(t_plus, t_minus)

        if t <= 0:
            return bottom_intersection_point

        distance = t * ray.direction.mag()
        if bottom_intersection_point is not None and distance > bottom_intersection_point.distance:
            return bottom_intersection_point
        position = ray.start.add(ray.direction.mult(t))
        # check distance between position and self.center is in range [-h, 0]
        far = self.center.y - position.y
        if far < -self.height or far > 0:
            return bottom_intersection_point
        # calc normal
        nx = 2 * (position.x - self.center.x)
        ny = -2 * (self.radius / self.height) ** 2 * (position.y - self.center.y - self.height)
        nz = 2 * (position.z - self.center.z)
        normal = PVector(nx, ny, nz).normalize()
        return IntersectionPoint(distance, position, normal)
