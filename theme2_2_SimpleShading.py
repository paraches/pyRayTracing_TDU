import math
import os
import pygame
from PGScreen import screen_setup, key_loop
from GeometryUtils.PVector import PVector


def map_range(value: float, in_min: float, in_max: float, out_min: float, out_max: float):
    return out_min + (((value - in_min) / (in_max - in_min)) * (out_max - out_min))


def constrain(value: float, min_value: float = 0.0, max_value: float = 1.0):
    return min(max_value, max(min_value, value))


def theme2_2_simple_shading():
    # screen size
    width = 512
    height = 512

    # screen_setup
    screen = screen_setup(width, height, os.path.basename(__file__))
    background_color = pygame.Color(100, 149, 237)

    # Scene setting
    pe = PVector(0, 0, -5)
    pc = PVector(0, 0, 5)
    r = 1.0
    pl = PVector(-5, 5, -5)
    ka = 0.01
    kd = 0.69
    ks = 0.3
    alpha = 8.0
    ia = 0.1
    ii = 1.0

    # loop
    for y in range(height):
        for x in range(width):
            pw = PVector(map_range(x, 0, width - 1, -1, 1), map_range(y, 0, height - 1, 1, -1), 0)
            de = pw.sub(pe)

            # chapter 3
            # theme 1-5
            #
            # |p - pc|^2 = r^2
            # p = s + td
            # |s + td - pc|^2 = r^2
            # |s - pc + td|^2 = r^2
            # |be + td|^2 = r^2   be = s - pc (ball eye)
            # |be|^2 + 2(be dot d)t + |d|^2t^2 = r^2
            # |d|^2t^2 + 2(be dot d)t + |be|^2 - r^2 = 0
            # A = |d|^2, B = 2(be dot d), C = |be|^2 - r^2
            # t = -B +/- sqrt(B^2 - 4AC) / 2A
            be = pe.sub(pc)
            a = de.mag_sq()
            b = 2 * be.dot(de)
            c = be.mag_sq() - r ** 2
            d = b ** 2 - 4 * a * c

            if d < 0:
                color = background_color
            else:
                if d == 0:
                    t = - b / (2 * a)
                else:
                    t_minus = (-b + math.sqrt(d)) / (2 * a)
                    t_plus = (-b - math.sqrt(d)) / (2 * a)
                    t = min(t_minus, t_plus)

                if t > 0:
                    # Chapter 5
                    # summary of reflection
                    #
                    # Rr = Ra + Rd + Rs

                    #
                    # ambient reflection
                    # Ra = kaIa
                    ra = ka * ia

                    #
                    # diffuse reflection
                    # Rd = kdIi(n dot l), |n| = 1, |l| = 1 (normalize)
                    # kd = 1.0, Ii = 1.0
                    # Rd = (n dot l)
                    # n = pi - pc,  pi = pe + tde
                    # l = pl - pi
                    pi = pe.add(de.mult(t))
                    n = pi.sub(pc).normalize()
                    l = pl.sub(pi).normalize()
                    nl = n.dot(l)
                    nl = constrain(nl)
                    rd = kd * ii * nl

                    #
                    # specular  reflection
                    # Rs = ksIi(v dot r) ** alpha
                    # v = -d, |v| = 1
                    v = de.reverse().normalize()
                    # r = 2(n dot l)n - l
                    # r = 2(nl)n - l, |r| = 1
                    r_vector = n.mult(2 * nl).sub(l).normalize()
                    vr = v.dot(r_vector)
                    vr = constrain(vr)
                    rs = ks * ii * (vr ** alpha)
                    rs = constrain(rs)

                    rr = constrain(ra + rd + rs)

                    color = pygame.Color((rr * 255, rr * 255, rr * 255))
                else:
                    color = background_color

            screen.set_at((x, y), color)

    # update screen
    pygame.display.flip()

    # wait esc key
    key_loop()


if __name__ == '__main__':
    theme2_2_simple_shading()
