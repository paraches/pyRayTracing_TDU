import pygame
from PVector import PVector


def map_range(value: float, in_min: float, in_max: float, out_min: float, out_max: float):
    return out_min + (((value - in_min) / (in_max - in_min)) * (out_max - out_min))


def screen_setup(width, height):
    pygame.init()
    return pygame.display.set_mode((width, height))


def key_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_ESCAPE:
                    running = False
    pygame.quit()


def theme1_7_first_sample():
    # screen size
    width = 512
    height = 512

    # screen_setup
    screen = screen_setup(width, height)
    background_color = pygame.Color(0, 0, 255)
    ball_color = pygame.Color(255, 0, 0)

    # Scene setting
    pe = PVector(0, 0, -5)
    pc = PVector(0, 0, 5)
    r = 1.0

    # loop
    for y in range(height):
        for x in range(width):
            pw = PVector(map_range(x, 0, width - 1, -1, 1), map_range(y, 0, height - 1, -1, 1), 0)
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

            if d >= 0:
                color = ball_color
            else:
                color = background_color

            screen.set_at((x, y), color)

    # update screen
    pygame.display.flip()

    # wait esc key
    key_loop()


if __name__ == '__main__':
    theme1_7_first_sample()
