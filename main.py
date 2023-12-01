import pygame, random
from entities import Player, NPC, Enemy
from base import ScenesManager, Scene
from blocks import Block

FPS = 60


if __name__ == '__main__':
    manager = ScenesManager()
    screen, running = None, True
    player = Player((50, 50))
    ents = [NPC('npc', (random.randint(0, 1000), random.randint(0, 1000))) for _ in range(10)]
    blcks = [Block('block', (random.randint(0, 1000), random.randint(0, 1000)))for _ in range(10)]
    enms = [Enemy('enemy', (random.randint(0, 1000), random.randint(0, 1000))) for _ in range(5)]
    scene = Scene(manager, ents + blcks + enms, player)
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
