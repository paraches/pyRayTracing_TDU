import math
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
from GeometryUtils.Scene import Scene, Camera
from GeometryUtils.Toon import Toon


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

        # EX-7 Toon edge
        #
        # R'r = Rr  (when |n dot de| <= q
        #       Rt  (when |n dot de| > q
        # Rr -> edge color
        # q  -> edge thickness
        if nearest_shape.material.toon:
            edge_nl = nearest_intersection.normal.dot(ray.direction.normalize())
            if abs(edge_nl) < nearest_shape.material.toon.edge_thickness:
                rr = nearest_shape.material.toon.edge_color
                break

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
            # rre = pi + EPSIRONre, re
            rre = Ray(nearest_intersection.position.add(re.mult(C_EPSILON)), re)
            # Rre = intensity with rre
            rre = ray_trace_recursive(scene, rre, recursion_level + 1)
            if rre is not None:
                # Rm = kfRre
                rm = nearest_shape.material.catadioptric_factor * rre
                # Rr = Ra + sigma_lights(Rdi + Rri) + Rm
                rr = rr + rm

    # refraction
    if nearest_shape.material.use_refraction:
        refraction_color = FColor()

        i = ray.direction.normalize()
        # v = -i
        v = i.reverse()

        n = nearest_intersection.normal
        vn = v.dot(n)

        # set h1 and h2 with vn
        h1 = nearest_shape.material.refraction_index if vn < 0 else scene.global_refraction_index
        h2 = scene.global_refraction_index if vn < 0 else nearest_shape.material.refraction_index
        # if vn < 0, re-calc n and vn
        if vn < 0:
            n = n.reverse()
            vn = v.dot(n)

        # hr = h2 / h1
        hr = h2 / h1

        # cos t1 = (v dot n)
        # cos t2 = h1 / h2 sqrt(hr^2 - (1 - (cos t1)^2))
        cost1 = vn
        cost2 = h1 / h2 * math.sqrt(hr * hr - (1 - cost1 * cost1))

        # o = hr cos t2 - cos t1
        o = hr * cost2 - cost1

        # p1 = (hr cos t1 - cos t2) / (hr cos t1 + cos t2)
        # p2 = -o / (hr cos t2 + cos t1)
        p1 = (hr * cost1 - cost2) / (hr * cost1 + cost2)
        p2 = -o / (hr * cost2 + cost1)

        # cr = 1 / 2 (p1^2 + p2^2)
        # ct = 1 - cr
        cr = (p1 * p1 + p2 * p2) / 2
        ct = 1 - cr

        # Rf = kf(crRre + ctRfe)
        #    = kf cr Rre + kf ct Rfe

        # Rre
        dre = n.mult(2 * vn).sub(v)
        rre = Ray((nearest_intersection.position.add(dre.mult(C_EPSILON))), dre)

        # Rfe
        dfe = i.mult(h1 / h2).sub(n.mult(h1 / h2 * o))
        rfe = Ray((nearest_intersection.position.add(dfe.mult(C_EPSILON))), dfe)

        # kf
        kf = nearest_shape.material.catadioptric_factor

        # kf cr Rfe
        reflection_value = ray_trace_recursive(scene, rre, recursion_level + 1)
        if reflection_value is not None:
            refraction_color += kf * reflection_value.mult(cr)

        # kf ct Rfe
        refraction_value = ray_trace_recursive(scene, rfe, recursion_level + 1)
        if refraction_value is not None:
            refraction_color += kf * refraction_value.mult(ct)

        rr = rr + refraction_color

    # EX-6
    #
    # R'r = (1 - a)Rr + aRfog
    # a = 0                             g < gnear
    #   = (g - gnear) / (gfar - gnear)  gnear <= g <= gfar
    #   = 1                             gfar < g
    # g = |pa - pe|
    if scene.use_fog:
        distance = nearest_intersection.distance
        if scene.fog.fog_near <= distance <= scene.fog.fog_far:
            alpha = (distance - scene.fog.fog_near) / (scene.fog.fog_far - scene.fog.fog_near)
            rr = rr.mult(1 - alpha) + scene.fog.fog_color.mult(alpha)
        elif scene.fog.fog_far < distance:
            rr = scene.fog.fog_color

    return rr


def theme_ex_7():
    # screen size
    width = 512
    height = 512

    # screen_setup
    screen = screen_setup(width, height, os.path.basename(__file__))
    background_color = pygame.Color(100, 149, 237)

    # Scene setting

    # shapes
    sphere_toon = Toon()
    shapes = [
        Sphere(PVector(3, 0, 25), 1, Material(FColor(0.01), FColor(0.69, 0, 0), FColor(0.30), 8.0, toon=sphere_toon)),
        Sphere(PVector(2, 0, 20), 1, Material(FColor(0.01), FColor(0, 0.69, 0), FColor(0.30), 8.0, toon=sphere_toon)),
        Sphere(PVector(1, 0, 15), 1, Material(FColor(0.01), FColor(0, 0, 0.69), FColor(0.30), 8.0, toon=sphere_toon)),
        Sphere(PVector(0, 0, 10), 1, Material(FColor(0.01), FColor(0, 0.69, 0.69), FColor(0.30), 8.0, toon=sphere_toon)),
        Sphere(PVector(-1, 0, 5), 1, Material(FColor(0.01), FColor(0.69, 0, 0.69), FColor(0.30), 8.0, toon=sphere_toon)),
        Plane(PVector(0, 1, 0), PVector(0, -1, 0), Material(FColor(0.01), FColor(0.69), FColor(0.30), 8.0))
    ]

    # light sources
    lights = [
        PointLightSource(PVector(-5, 5, -5), FColor(0.5)),
        PointLightSource(PVector(5, 0, -5), FColor(0.5)),
        PointLightSource(PVector(5, 20, -5), FColor(0.5)),
    ]

    # ambient light source
    i_ambient = FColor(0.1)

    camera = Camera(PVector(0, 0, -5), PVector(), 23)
    from GeometryUtils.Scene import GLOBAL_REFRACTION_INDEX

    toon = Toon()
    scene = Scene(shapes, lights, i_ambient, GLOBAL_REFRACTION_INDEX, camera, width, height)

    # loop
    for y in range(height):
        for x in range(width):
            pw = scene.world_from_screen_coordinate(x, y)

            # eye
            eye_ray = Ray(scene.camera.position, pw.sub(scene.camera.position))

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
    theme_ex_7()
