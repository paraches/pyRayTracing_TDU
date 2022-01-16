import os

import pygame
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


MAX_RECURSION = 8


def ray_trace(scene: Scene, ray: Ray) -> FColor | None:
    return ray_trace_recursive(scene, ray, 0)


def ray_trace_recursive(scene: Scene, ray: Ray, recursion_level: int) -> FColor | None:
    if recursion_level > MAX_RECURSION:
        return None

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

    # Perfect reflection
    if nearest_shape.material.use_perfect_reflectance:
        # re = 2(v dot n)n - v
        # n = pi.normal, v = ray.direction.reverse
        v = ray.direction.reverse().normalize()
        n = nearest_intersection.normal
        vn = v.dot(n)
        if vn > 0:
            re = n.mult(2 * v.dot(n)).sub(v)
            # re_ray = pi + EPSIRONre, re
            re_ray = Ray(nearest_intersection.position.add(re.mult(C_EPSILON)), re)
            # Rre = intensity with re_ray
            rre = ray_trace_recursive(scene, re_ray, recursion_level + 1)
            if rre is not None:
                # Rm = kfRre
                rm = nearest_shape.material.catadioptric_factor * rre
                # Rr = Ra + sigma_lights(Rdi + Rri) + Rm
                rr = rr + rm

    return rr


def theme3_2_full_ray_tracing():
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
        Sphere(PVector(-0.25, -0.5, 3), 0.5, Material(FColor(0), FColor(0), FColor(0), 0, True, FColor(1.0))),
        Plane(PVector(0, 1, 0), PVector(0, -1, 0), Material(FColor(), FColor(0.69), FColor(), 0)),
        Plane(PVector(0, -1, 0), PVector(0, 1, 0), Material(FColor(), FColor(0.69), FColor(), 0)),
        Plane(PVector(-1, 0, 0), PVector(1, 0, 0), Material(FColor(), FColor(0, 0.69, 0), FColor(), 0)),
        Plane(PVector(1, 0, 0), PVector(-1, 0, 0), Material(FColor(), FColor(0.69, 0, 0), FColor(), 0)),
        Plane(PVector(0, 0, -1), PVector(0, 0, 5), Material(FColor(), FColor(0.69), FColor(), 0)),
    ]

    # light sources
    lights = [
        PointLightSource(PVector(0, 0.9, 2.5), FColor(1.0)),
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

    # wait esc key
    key_loop()


if __name__ == '__main__':
    theme3_2_full_ray_tracing()
