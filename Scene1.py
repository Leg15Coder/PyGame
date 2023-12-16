from base import *
from entities import *
from blocks import *
from items import *
import random


manager = ScenesManager()

ents = [NPC('npc', (random.randint(-10000, 10000), random.randint(-10000, 10000))) for _ in range(32)]
blcks = [Wall('block', (random.randint(100, 2000), random.randint(100, 2000), random.randint(100, 2000), random.randint(100, 2000))) for _ in range(0)]
enms = [Enemy('enemy', (random.randint(-10000, 10000), random.randint(-10000, 10000)), damage=2) for _ in range(32)]
shts = [Shooter('shooter', (random.randint(-10000, 10000), random.randint(-10000, 10000)), damage=2) for _ in range(0)]
scene = Scene('test', manager)
scene.add_objects(*ents)
scene.add_objects(*blcks)
scene.add_objects(*enms)
scene.add_objects(*shts)
scene.add_objects(Weapon('sword', (500, 400), damage=8))
manager.add_scene(scene)
