import pygame

def screen_setup(width, height, title=None):
    pygame.init()
    if title is not None:
        pygame.display.set_caption(title)
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
