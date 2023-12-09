from base import *
from entities import *
from blocks import *
import random


manager = ScenesManager()

ents = [NPC('npc', (random.randint(-1000, 1000), random.randint(-1000, 1000))) for _ in range(16)]
blcks = [Wall('block', (random.randint(100, 1000), random.randint(100, 1000), random.randint(100, 1000), random.randint(100, 1000))) for _ in range(5)]
enms = [Enemy('enemy', (random.randint(-1000, 1000), random.randint(-1000, 1000)), damage=2) for _ in range(10)]
shts = [Shooter('shooter', (random.randint(-1000, 1000), random.randint(-1000, 1000)), damage=2) for _ in range(6)]
player = Player((0, 0), health=200000)
scene = Scene(manager, player)
scene.add_objects(*ents)
scene.add_objects(*blcks)
scene.add_objects(*enms)
scene.add_objects(*shts)
manager.add_scene(scene)
