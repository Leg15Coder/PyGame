import pygame
import sys
from base import ScenesManager
from Scene1 import manager

FPS = 60


if __name__ == '__main__':
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            manager.show(event)
            clock.tick(FPS)
        manager.show(None)
        clock.tick(FPS)
    pygame.quit()
    sys.exit()
