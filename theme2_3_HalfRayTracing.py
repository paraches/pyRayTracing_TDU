import math
from unittest import TestCase
from GeometryUtils.PVector import PVector
from GeometryUtils.Ray import Ray
from GeometryUtils.IntersectionPoint import IntersectionPoint
from GeometryUtils.Shapes.Sphere import Sphere


def equals_pv(v1: PVector, v2: PVector):
    return math.isclose(v1.x, v2.x) and math.isclose(v1.y, v2.y) and math.isclose(v1.z, v2.z)


def equals_ip(ip1: IntersectionPoint, ip2: IntersectionPoint):
    return math.isclose(ip1.distance, ip2.distance) and \
           equals_pv(ip1.position, ip2.position) and \
           equals_pv(ip1.normal, ip2.normal)


class TestTheme2_3(TestCase):
    def test_case_1(self):
        sph = Sphere(PVector(0, 0, 5), 1)

        start = PVector(0, 0, -5)
        direction = PVector(-1, 1, 0).sub(start)
        ray = Ray(start, direction)

        res = sph.test_intersection(ray)

        self.assertIsNone(res)

    def test_case_2(self):
        sph = Sphere(PVector(0, 0, 5), 1)

        start = PVector(0, 0, -5)
        direction = PVector(0, 0, 0).sub(start)
        ray = Ray(start, direction)

        expect = IntersectionPoint(9, PVector(0, 0, 4), PVector(0, 0, -1))

        res = sph.test_intersection(ray)

        self.assertIsNotNone(res)
        self.assertTrue(equals_ip(expect, res))

    def test_case_3(self):
        sph = Sphere(PVector(0, 0, 5), 1)

        start = PVector(0, 0, -5)
        direction = PVector(math.sqrt(25.0 / 99.0), 0, 0).sub(start)
        ray = Ray(start, direction)

        distance = (9900.0 / 5000.0) * ray.direction.mag()
        position = ray.get_point(9900.0 / 5000.0)
        normal = position.sub(sph.center)
        expect = IntersectionPoint(distance, position, normal)

        res = sph.test_intersection(ray)

        self.assertIsNotNone(res)
        self.assertTrue(equals_ip(expect, res))
