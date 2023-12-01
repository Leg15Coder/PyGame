from random import randint
from datetime import datetime as dt


def stay(this, event):
    pass


def random(this, event):
    this.goto(this.coords[0] + randint(-64, 64), this.coords[1] + randint(-64, 64))


def to_player(this, event):
    this.goto(*this.parent.objects['player'].coords)


def dist(c1: tuple, c2: tuple):
    return ((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2) ** 0.5
