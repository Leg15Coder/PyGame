import pygame
from functions import end, start
from base import ScenesManager

FPS = 60


if __name__ == '__main__':
    running, clock, manager = start(ScenesManager)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            manager.show(event)
            clock.tick(FPS)
        manager.show(None)
        clock.tick(FPS)
    end(manager)
