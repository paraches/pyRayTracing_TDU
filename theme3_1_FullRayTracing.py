import os

import pygame
import timeit
from PGScreen import screen_setup, key_loop
from GeometryUtils.PVector import PVector
from GeometryUtils.FColor import FColor
from GeometryUtils.Ray import Ray
from GeometryUtils.LightSources.PointLightSource import PointLightSource
from GeometryUtils.Shapes.Sphere import Sphere
from GeometryUtils.Shapes.Plane import Plane
from GeometryUtils.GeometryUtil import map_range, constrain, C_EPSILON
from GeometryUtils.Material import Material
from GeometryUtils.Scene import Scene


def ray_trace(scene: Scene, ray: Ray) -> FColor | None:
    nearest_shape, nearest_intersection = scene.test_intersection_with_all(ray)
    if nearest_intersection is None:
        return None

    # ray tracing
    # Rr = Ra + sigma_lights(Rd + Rs)

    # ambient light reflection
    # Ra = kaIa
    # Rr = Ra
    rr = nearest_shape.material.ambient_factor * scene.ambient_intensity

    # + sigma_lights(Rd + Rs)
    for light_source in scene.light_sources:
        lighting = light_source.lighting_at(nearest_intersection.position)

        # shadow
        # shadow ray: start = pi + epsilon * l
        #             direction l
        shadow_ray = Ray(nearest_intersection.position.add(lighting.direction.mult(C_EPSILON)), lighting.direction)
        shadow_shape, shadow_intersection = scene.test_intersection_with_all(shadow_ray, lighting.distance, True)
        if shadow_shape and shadow_intersection:
            continue

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
            vv = ray.direction.reverse().normalize()
            vr = vv.dot(rv)
            vr = constrain(vr)
            rs = (nearest_shape.material.specular_factor * lighting.intensity).mult(
                vr ** nearest_shape.material.shininess)

        # add light source's diffuse and specular reflection
        # Rd + Rs
        rr = rr + rd + rs

    return rr


def theme3_1_full_ray_tracing():
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
            reflection = ray_trace(scene, eye_ray)

            if reflection is None:
                color = background_color
            else:
                color = pygame.Color(reflection.to_pygame_color_tuple())
            screen.set_at((x, y), color)

    # update screen
    pygame.display.flip()


if __name__ == '__main__':
    loop = 5
    result = timeit.timeit('theme3_1_full_ray_tracing()', globals=globals(), number=loop)
    print(f'avg: {result / loop} sec')  # avg: 21.51888637939701

    # wait esc key
    key_loop()
