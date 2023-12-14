from base import *
from entities import *
from blocks import *
from items import *
import random


manager = ScenesManager()

ents = [NPC('npc', (random.randint(-1000, 1000), random.randint(-1000, 1000))) for _ in range(16)]
blcks = [Wall('block', (random.randint(100, 1000), random.randint(100, 1000), random.randint(100, 1000), random.randint(100, 1000))) for _ in range(5)]
enms = [Enemy('enemy', (random.randint(-1000, 1000), random.randint(-1000, 1000)), damage=2) for _ in range(16)]
shts = [Shooter('shooter', (random.randint(-1000, 1000), random.randint(-1000, 1000)), damage=2) for _ in range(0)]
player = Player((0, 0), health=250)
scene = Scene(manager, player)
scene.add_objects(*ents)
scene.add_objects(*blcks)
scene.add_objects(*enms)
scene.add_objects(*shts)
scene.add_objects(Weapon('sword', (-100, -100), damage=60))
manager.add_scene(scene)
