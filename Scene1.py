from base import *
from entities import *
from blocks import *
from items import *
from behaviors import *
import random


manager = ScenesManager()

if False:
    ents = [NPC(name='npc', coords=(random.randint(-1, 1000), random.randint(-1, 1000))) for _ in range(10)]
    enms = [Enemy(name='enemy', coords=(random.randint(-1, 1000), random.randint(-1, 1000)), damage=2) for _ in range(8)]
    shts = [Enemy(name='shooter', coords=(random.randint(-1, 1000), random.randint(-1, 1000)), damage=2, attack=to_player_and_shoot) for _ in range(5)]
    scene = Scene('test', manager)
    scene.add_objects(*ents)
    scene.add_objects(*enms)
    scene.add_objects(*shts)
    scene.add_objects(Weapon(name='sword', coords=(500, 400), damage=8), Weapon(name='bow', coords=(800, 600)))
    manager.add_scene(scene)
else:
    manager.load()
