from entities import Sprite, Enemy
from behaviors import dist
from functions import load_image, nothing
import pygame
from datetime import datetime as dt
from datetime import timedelta


class Item(Sprite):
    def __init__(self, name: str, coords=None):
        super().__init__(name, coords, False, True)
        self.coords = coords
        self.player = None
        self.slot = None
        self.count = 1
        self.name = name
        img = load_image(rf"sprites/items/{name}/1.jpg")
        self.sprite = pygame.transform.scale(img, (24, 24))

    def pick(self, player):
        self.player = player
        self.slot = player.get_empty_slot()
        if 0 <= self.slot < 33:
            self.visible = False
            self.player.inventory[self.slot] = self
        else:
            self.slot = None

    def update(self, event):
        super().update(event)
        if self.player is None:
            objs = self.parent.objects
            if 'player' in objs:
                if dist(self.coords, objs['player'].coords) <= 40:
                    self.pick(objs['player'])


class Weapon(Item):
    def __init__(self, name: str, coords=None, **kwargs):
        super().__init__(name, coords)
        self.attack = kwargs['attack'] if 'attack' in kwargs else nothing
        self.damage = kwargs['damage'] if 'damage' in kwargs else 1
        cd = kwargs['cooldown_attack'] if 'cooldown_attack' in kwargs else 1
        self.cooldown_attack = timedelta(seconds=cd)
        self.current_cooldown_attack = dt.now()

    def use(self, coords: tuple):
        if dt.now() - self.cooldown_attack > self.current_cooldown_attack:
            enems = list(filter(lambda x: isinstance(x, Enemy) and dist(coords, x.coords) <= 100,
                                self.parent.objects['entities']))
            for enem in enems:
                enem.health -= self.damage
            self.current_cooldown_attack = dt.now()

    def update(self, event):
        super().update(event)
        if self.player is not None and self.slot == 33:
            self.set_pos(*self.player.coords)


class Ability(Item):
    pass


class Decor(Item):
    pass
