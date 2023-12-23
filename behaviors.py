import os.path
import sys
from random import randint
from datetime import datetime as dt
import pygame.image


def stay(this, event):
    pass


def dialog(this, event):
    if 'player' in this.parent.objects and dist(this.parent.objects['player'].coords, this.coords) <= 50:
        n = 2
        this.parent.start_dialog(event(this.parent.manager, randint(1, n)))


def random(this, event):
    dialog(this, this.dialog)
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
    to_player(this, event)
    if 'player' in this.parent.objects:
        if dt.now() - this.cooldown_attack > this.current_cooldown_attack \
                and dist(this.coords, this.parent.objects['player'].coords) <= 32:
            this.current_cooldown_attack = dt.now()
            this.parent.objects['player'].health -= this.damage


def to_player_and_shoot(this, event):
    if 'player' in this.parent.objects:
        pl_coords = this.parent.objects['player'].coords
        r = dist(this.coords, pl_coords)
        if dt.now() - this.cooldown_attack > this.current_cooldown_attack:
            if r < 266:
                x, y = pl_coords[0] - this.coords[0] + 32, pl_coords[1] - this.coords[1] + 32
                x, y = (x / (x ** 2 + y ** 2) ** 0.5) * 10, (y / (x ** 2 + y ** 2) ** 0.5) * 10
                shard = this.shard(this.parent, 'shard', this.coords, (x, y))
                this.parent.add_objects(shard)
                this.current_cooldown_attack = dt.now()
        if r > 300:
            this.goto(*pl_coords)
        elif r < 250:
            pos = 2 * this.coords[0] - pl_coords[0], 2 * this.coords[1] - pl_coords[1]
            this.goto(*pos)
        else:
            stay(this, event)
    else:
        stay(this, event)
