import os.path
import sys
from random import randint
from datetime import datetime as dt
import pygame.image
from ui import Dialog


def stay(this, event):
    pass


def dialog(this, event):
    if 'player' in this.parent.objects and dist(this.parent.objects['player'].coords, this.coords) <= 50:
        n = 2
        this.parent.start_dialog(Dialog(this.parent.manager, randint(1, n)))


def random(this, event):
    dialog(this, event)
    this.goto(this.coords[0] + randint(-100, 100), this.coords[1] + randint(-100, 100))


def to_player(this, event):
    if 'player' in this.parent.objects:
        this.goto(*this.parent.objects['player'].coords)
    else:
        stay(this, event)


def dist(c1: tuple, c2: tuple):
    return ((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2) ** 0.5


def game_over():
    pass


def die(this, event):
    this.delete()


def attack(this, event):
    if 'player' in this.parent.objects:
        if dt.now() - this.cooldown_attack > this.current_cooldown_attack \
                and dist(this.coords, this.parent.objects['player'].coords) <= 32:
            this.current_cooldown_attack = dt.now()
            this.parent.objects['player'].health -= this.damage


def is_in_rectangle(coords: tuple, c1: tuple, c2: tuple):
    x1, y1 = c1
    x2, y2 = c2
    dx, dy = x2 - x1, y2 - y1
    if dx >= 0 and dy >= 0:
        collision = ((x1, y1), (x2, y2))
    elif dx < 0 and dy < 0:
        collision = ((x2, y2), (x1, y1))
    elif dx >= 0 and dy < 0:
        collision = ((x1, y2), (x2, y1))
    else:
        collision = ((x2, y1), (x1, y2))
    return collision[0][0] <= coords[0] <= collision[1][0] and collision[0][1] <= coords[1] <= collision[1][1]


def to_player_and_shoot(this, event):
    if 'player' in this.parent.objects:
        this.goto(*this.parent.objects['player'].coords)
        this.shoot(*this.parent.objects['player'].coords)
    else:
        stay(this, event)


def load_image(name, colorkey=None):
    if not os.path.isfile(name):
        raise ImportError(f"Файл с названием {name} не найден")
    image = pygame.image.load(name)
    if colorkey is None:
        image = image.convert_alpha()
    else:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image
