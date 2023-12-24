from entities import Sprite
import pygame
from behaviors import dist
from PIL import Image
from os import path, remove


class Node(Sprite):
    def __init__(self, name, coords=(0, 0)):
        super().__init__(name, coords, False, False)


class Block(Sprite):
    def __init__(self, name, coords=(0, 0), tangible=True, visible=True):
        super().__init__(name, coords, tangible, visible)

    def collision_box(self, coords: tuple):
        return dist(coords, self.coords) <= 64


class Wall(Block):
    def __init__(self, name, coords=(0, 0, 0, 0), visible=True):
        x1, y1, x2, y2 = coords
        dx, dy = x2 - x1, y2 - y1
        if dx >= 0 and dy >= 0:
            self.collision = ((x1, y1), (x2, y2))
        elif dx < 0 and dy < 0:
            self.collision = ((x2, y2), (x1, y1))
        elif dx >= 0 and dy < 0:
            self.collision = ((x1, y2), (x2, y1))
        else:
            self.collision = ((x2, y1), (x1, y2))
        super().__init__(name, self.collision[0], True, visible)
        self.name = name

    def collision_box(self, coords: tuple):
        return self.collision[0][0] - 64 <= coords[0] <= self.collision[1][0] and\
               self.collision[0][1] - 64 <= coords[1] <= self.collision[1][1]


class Floor(Block):
    def __init__(self, name, coords=(0, 0, 0, 0)):
        self.collosion = (coords[:2], coords[2:4])
        super().__init__(name, self.collision[0], False, True)
        self.name = name


class Usable(Block, Node):
    pass


class Fragile(Block):
    pass
