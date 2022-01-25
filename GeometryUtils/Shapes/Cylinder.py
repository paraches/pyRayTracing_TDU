import math
from .Shape import Shape
from ..Ray import Ray
from ..PVector import PVector
from ..Material import Material
from ..IntersectionPoint import IntersectionPoint


class Cylinder(Shape):
    def __init__(self, center=PVector(), radius=1.0, height=2.0, material=Material()):
        super(Cylinder, self).__init__(material)
        self.center = center
        self.radius = radius
        self.height = height

    def test_plane_intersection(self, ray: Ray, normal: PVector):
        dn_dot = ray.direction.dot(normal)
        intersection_point = None
        if dn_dot != 0:
            center = self.center.add(normal.mult(self.height / 2))
            t = (center.dot(normal) - ray.start.dot(normal)) / dn_dot
            if t > 0:
                position = ray.get_point(t)
                if position.sub(center).mag() <= self.radius:
                    distance = t * ray.direction.mag()
                    intersection_point = IntersectionPoint(distance, position, normal)

        return intersection_point

    def test_intersection(self, ray: Ray):
        # EX-5-EX

        # bottom plane
        intersection_point = self.test_plane_intersection(ray, PVector(0, -1, 0))

        # top plane
        top_intersection_point = self.test_plane_intersection(ray, PVector(0, 1, 0))
        if top_intersection_point is not None:
            if intersection_point is None or top_intersection_point.distance < intersection_point.distance:
                intersection_point = top_intersection_point

        # |(p - pc)M|^2 = r^2
        # M = |1 0 0|
        #     |0 0 0|
        #     |0 0 1|
        # p = s + td
        # - h / 2 <= y_distance h / 2
        # |(td + s - pc)M|^2 = r^2
        # m = s - pc
        # |(td + m)M|^2 = r^2
        # |dM|^2t^2 + 2(dM dot mM)t + |mM|^2 - r^2 = 0
        # A = |dM|^2
        # B = 2(dM dot mM)
        # C = |mM|^2 - r^2
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
            position = ray.get_point(t)
            y_delta = position.y - self.center.y
            if (-self.height / 2) <= y_delta <= self.height / 2:
                distance = t * ray.direction.mag()
                nx = 2 * (position.x - self.center.x)
                ny = 0
                nz = 2 * (position.z - self.center.z)
                normal = PVector(nx, ny, nz).normalize()
                body_intersection_point = IntersectionPoint(distance, position, normal)
                if intersection_point is None or body_intersection_point.distance < intersection_point.distance:
                    intersection_point = body_intersection_point

        return intersection_point
