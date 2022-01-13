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
from GeometryUtils.Scene import Scene


def theme2_8_full_ray_tracing():
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

    # light sources
    lights = [
        PointLightSource(PVector(-5, 5, -5), FColor(0.5)),
        PointLightSource(PVector(5, 0, -5), FColor(0.5)),
        PointLightSource(PVector(5, 20, -5), FColor(0.5)),
    ]

    # ambient light source
    i_ambient = FColor(0.1)

    scene = Scene(shapes, lights, i_ambient)

    # loop
    for y in range(height):
        for x in range(width):
            pw = PVector(map_range(x, 0, width - 1, -1, 1), map_range(y, 0, height - 1, 1, -1), 0)

            # eye
            eye_ray = Ray(pe, pw.sub(pe))

            # find the nearest shape and intersection
            nearest_shape, nearest_intersection = scene.test_intersection_with_all(eye_ray)
            if nearest_intersection is None:
                screen.set_at((x, y), background_color)
                continue

            # ray tracing
            # Rr = Ra + sigma_lights(Rd + Rs)

            # ambient light reflection
            # Ra = kaIa
            # Rr = Ra
            rr = nearest_shape.material.ambient_factor * i_ambient

            # + sigma_lights(Rd + Rs)
            for light_source in lights:
                lighting = light_source.lighting_at(nearest_intersection.position)

                # diffuse reflection
                # Rd = kdIi(nv dot lv), |nv| = 1, |lv| = 1
                nl = nearest_intersection.normal.dot(lighting.direction)
                nl = constrain(nl)
                rd = (nearest_shape.material.diffuse_factor * lighting.intensity).mult(nl)

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
                    rs = (nearest_shape.material.specular_factor * lighting.intensity).mult(vr ** nearest_shape.material.shininess)

                # add light source's diffuse and specular reflection
                # Rd + Rs
                rr = rr + rd + rs

            color = pygame.Color(rr.to_pygame_color_tuple())
            screen.set_at((x, y), color)

    # update screen
    pygame.display.flip()

    # wait esc key
    key_loop()


if __name__ == '__main__':
    theme2_8_full_ray_tracing()
