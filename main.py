import pygame
from base import ScenesManager
from Scene1 import manager

FPS = 60


if __name__ == '__main__':
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            manager.show(event)
            manager.clock.tick(FPS)
        manager.show(None)
        manager.clock.tick(FPS)
    pygame.quit()
    sys.exit()
