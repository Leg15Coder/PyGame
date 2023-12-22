from base import *
from entities import *
from blocks import *
from items import *
from behaviors import *
import random


manager = ScenesManager()

ents = [NPC('npc', (random.randint(-1, 1000), random.randint(-1, 1000))) for _ in range(10)]
blcks = [Wall('block', (random.randint(100, 2000), random.randint(100, 2000), random.randint(100, 2000), random.randint(100, 2000))) for _ in range(0)]
enms = [Enemy('enemy', (random.randint(-1, 1000), random.randint(-1, 1000)), damage=2) for _ in range(8)]
shts = [Enemy('shooter', (random.randint(-1, 1000), random.randint(-1, 1000)), damage=2, attack=to_player_and_shoot) for _ in range(5)]
scene = Scene('test', manager)
scene.add_objects(*ents)
scene.add_objects(*blcks)
scene.add_objects(*enms)
scene.add_objects(*shts)
scene.add_objects(Weapon('sword', (500, 400), damage=8))
manager.add_scene(scene)
