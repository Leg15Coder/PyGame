from base import Sprite
import pygame


class Entity(Sprite):
    def __init__(self, scene, coords=(0, 0), tangible=False, visible=True, health=100, **kwargs):
        super().__init__(scene, coords, tangible, visible)
        self.health = health
        self.abilities = dict(kwargs)


class Player(Entity):
    def __init__(self, scene, coords=(0, 0), health=100, **kwargs):
        super().__init__(scene, coords, False, True, health, **kwargs)
        self.events = {'w': False, 's': False, 'a': False, 'd': False}

    def event_check(self, event):
        if event.type == pygame.KEYDOWN:
            symb = event.unicode
            self.events[symb] = True
        if event.type == pygame.KEYUP:
            symb = event.unicode
            self.events[symb] = False

    def walking(self):
        k = 4
        if self.events['w']:
            self.coords = (self.coords[0], self.coords[1] - k)
        if self.events['s']:
            self.coords = (self.coords[0], self.coords[1] + k)
        if self.events['d']:
            self.coords = (self.coords[0] + k, self.coords[1])
        if self.events['a']:
            self.coords = (self.coords[0] - k, self.coords[1])
        self.set_pos(*self.coords)


class Enemy(Entity):
    pass


class Boss(Enemy):
    pass


class Ally(Entity):
    pass


class NPC(Entity):
    pass
