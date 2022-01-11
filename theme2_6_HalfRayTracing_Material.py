import os
import pygame
from PGScreen import screen_setup, key_loop
from GeometryUtils.PVector import PVector
from GeometryUtils.FColor import FColor
from GeometryUtils.Ray import Ray
from GeometryUtils.LightSources.PointLightSource import PointLightSource
from GeometryUtils.Shapes.Sphere import Sphere
from GeometryUtils.Shapes.Plane import Plane
from GeometryUtils.GeometryUtil import map_range, constrain
from GeometryUtils.Material import Material


def theme2_6_half_ray_tracing_material():
    # screen size
    width = 512
    height = 512

    # screen_setup
    screen = screen_setup(width, height, os.path.basename(__file__))
    background_color = pygame.Color(100, 149, 237)

    # Scene setting

    # eye position
    pe = PVector(0, 0, -5)

    # shapes
    shapes = [
        Sphere(PVector(3, 0, 25), 1, Material(FColor(0.01), FColor(0.69, 0, 0), FColor(0.30), 8.0)),
        Sphere(PVector(2, 0, 20), 1, Material(FColor(0.01), FColor(0, 0.69, 0), FColor(0.30), 8.0)),
        Sphere(PVector(1, 0, 15), 1, Material(FColor(0.01), FColor(0, 0, 0.69), FColor(0.30), 8.0)),
        Sphere(PVector(0, 0, 10), 1, Material(FColor(0.01), FColor(0, 0.69, 0.69), FColor(0.30), 8.0)),
        Sphere(PVector(-1, 0, 5), 1, Material(FColor(0.01), FColor(0.69, 0, 0.69), FColor(0.30), 8.0)),
        Plane(PVector(0, 1, 0), PVector(0, -1, 0), Material(FColor(0.01), FColor(0.69, 0.69, 0.69), FColor(0.30), 8.0))
    ]

    # light source
    pl = PVector(-5, 5, -5)
    ii = FColor(1.0)    # Ii
    light_source = PointLightSource(pl, ii)

    # ambient light source
    i_ambient = FColor(0.1)

    # loop
    for y in range(height):
        for x in range(width):
            pw = PVector(map_range(x, 0, width - 1, -1, 1), map_range(y, 0, height - 1, 1, -1), 0)

            # eye
            eye_ray = Ray(pe, pw.sub(pe))

            # check each shape's intersection
            intersections = [(shape, shape.test_intersection(eye_ray)) for shape in shapes if shape.test_intersection(eye_ray) is not None]
            if len(intersections) == 0:
                screen.set_at((x, y), background_color)
                continue

            # find the nearest shape
            shape, nearest_intersection = min(intersections, key=lambda intersection: intersection[1].distance)

            # ray tracing
            lighting = light_source.lighting_at(nearest_intersection.position)

            # ambient light reflection
            # Ra = kaIa
            ra = shape.material.ambient_factor * i_ambient

            # diffuse reflection
            # Rd = kdIi(nv dot lv), |nv| = 1, |lv| = 1
            nl = nearest_intersection.normal.dot(lighting.direction)
            nl = constrain(nl)
            rd = (shape.material.diffuse_factor * lighting.intensity).mult(nl)

            # specular reflection
            # Rs = ksIi(vv dot rv)^a
            # rv = 2(nv dot lv)nv - lv
            # |nv| = 1, |lv| = 1, |vv| = 1, |rv| = 1
            rs = FColor(0.0)
            if nl > 0:
                rv = nearest_intersection.normal.mult(2 * nl).sub(lighting.direction).normalize()
                vv = eye_ray.direction.reverse().normalize()
                vr = vv.dot(rv)
                vr = constrain(vr)
                rs = (shape.material.specular_factor * lighting.intensity).mult(vr ** shape.material.shininess)

            # all reflection
            # Rr = Ra + Rd + Rs
            rr = ra + rd + rs
            color = pygame.Color(rr.to_pygame_color_tuple())

            screen.set_at((x, y), color)

    # update screen
    pygame.display.flip()

    # wait esc key
    key_loop()


if __name__ == '__main__':
    theme2_6_half_ray_tracing_material()
