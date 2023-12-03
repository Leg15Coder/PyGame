import pygame
import random
from db import db
from base import ScenesManager, Scene
from blocks import Block
from entities import Player, NPC, Enemy

FPS = 60


if __name__ == '__main__':
    manager = ScenesManager()
    screen, running = None, True
    ents = [NPC('npc', (random.randint(-1000, 1000), random.randint(-1000, 1000))) for _ in range(16)]
    blcks = [Block('block', (random.randint(-1000, 1000), random.randint(-1000, 1000)))for _ in range(16)]
    enms = [Enemy('enemy', (random.randint(-2000, 1000), random.randint(-1000, 1000)), damage=2) for _ in range(16)]
    scene = Scene(manager, ents + blcks + enms, Player((0, 0)))
    del ents, blcks, enms
    manager.add_scene(scene)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            manager.show(event)
            manager.clock.tick(FPS)
        manager.show(None)
        manager.clock.tick(FPS)
    pygame.quit()
