import os
import pygame
from PGScreen import screen_setup, key_loop
from GeometryUtils.PVector import PVector
from GeometryUtils.FColor import FColor
from GeometryUtils.Ray import Ray
from GeometryUtils.LightSources.PointLightSource import PointLightSource
from GeometryUtils.Shapes.Sphere import Sphere
from GeometryUtils.GeometryUtil import map_range, constrain


def theme2_4_half_ray_tracing():
    # screen size
    width = 512
    height = 512

    # screen_setup
    screen = screen_setup(width, height, os.path.basename(__file__))
    background_color = pygame.Color(100, 149, 237)

    # Scene setting

    # eye position
    pe = PVector(0, 0, -5)

    # Sphere
    pc = PVector(0, 0, 5)
    r = 1.0
    sphere = Sphere(pc, r)

    # light source
    pl = PVector(-5, 5, -5)
    ii = FColor(1.0)    # Ii
    light_source = PointLightSource(pl, ii)

    # theme 2-4
    k_ambient = FColor(0.01)
    k_diffuse = FColor(0.69, 0.0, 0.0)
    k_specular = FColor(0.3)
    alpha = 8.0

    # ambient light source
    i_ambient = FColor(0.1)

    # ambient light reflection
    # Ra = kaIa
    ra = k_ambient * i_ambient

    # loop
    for y in range(height):
        for x in range(width):
            pw = PVector(map_range(x, 0, width - 1, -1, 1), map_range(y, 0, height - 1, 1, -1), 0)

            # eye
            eye_ray = Ray(pe, pw.sub(pe))

            # check intersection
            intersection = sphere.test_intersection(eye_ray)
            if intersection is None:
                screen.set_at((x, y), background_color)
                continue

            # ray tracing
            lighting = light_source.lighting_at(intersection.position)

            # diffuse reflection
            # Rd = kdIi(nv dot lv), |nv| = 1, |lv| = 1
            nl = intersection.normal.dot(lighting.direction)
            nl = constrain(nl)
            rd = (k_diffuse * lighting.intensity).mult(nl)

            # specular reflection
            # Rs = ksIi(vv dot rv)^a
            # rv = 2(nv dot lv)nv - lv
            # |nv| = 1, |lv| = 1, |vv| = 1, |rv| = 1
            rs = FColor(0.0)
            if nl > 0:
                rv = intersection.normal.mult(2 * nl).sub(lighting.direction).normalize()
                vv = eye_ray.direction.reverse().normalize()
                vr = vv.dot(rv)
                vr = constrain(vr)
                rs = (k_specular * lighting.intensity).mult(vr ** alpha)

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
    theme2_4_half_ray_tracing()
