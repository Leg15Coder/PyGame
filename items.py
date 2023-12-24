from entities import Sprite, Enemy
from behaviors import dist
from functions import load_image, nothing, from_str_to_type
import pygame
from datetime import datetime as dt
from datetime import timedelta as dl


class Item(Sprite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = self.abilities['player'] if 'player' in self.abilities and self.abilities['player'] != 'None' \
            else self.add_ability('player', None)
        self.slot = from_str_to_type(self.abilities['slot']) if 'slot' in self.abilities \
            else self.add_ability('slot', None)
        self.count = from_str_to_type(self.abilities['count'], int) if 'count' in self.abilities \
            else self.add_ability('count', 1)
        img = load_image(rf"sprites/items/{self.name}/1.jpg")
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
        if isinstance(self.player, str) and self.parent is not None:
            self.add_ability('player', self.parent.objects['player'])
            self.player = self.abilities['player']
            self.player.inventory[self.slot] = self
        if self.player is None:
            objs = self.parent.objects
            if 'player' in objs:
                if dist(self.coords, objs['player'].coords) <= 40:
                    self.pick(objs['player'])


class Weapon(Item):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.attack = from_str_to_type(self.abilities['attack']) if 'attack' in self.abilities \
            else self.add_ability('attack', nothing)
        self.damage = from_str_to_type(self.abilities['damage']) if 'damage' in self.abilities \
            else self.add_ability('damage', 1)
        self.cooldown_attack = from_str_to_type(self.abilities['cooldown_attack'], dl) \
            if 'cooldown_attack' in self.abilities else self.add_ability('cooldown_attack', dl(seconds=1))
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
