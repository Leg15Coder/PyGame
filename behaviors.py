from random import randint
from datetime import datetime as dt
from ui import Dialog


def stay(this, event):
    pass


def dialog(this, event):
    if 'player' in this.parent.objects and dist(this.parent.objects['player'].coords, this.coords) <= 32:
        this.parent.start_dialog(Dialog(this.parent.manager, 1))


def random(this, event):
    dialog(this, event)
    this.goto(this.coords[0] + randint(-64, 64), this.coords[1] + randint(-64, 64))


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
    del this


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
    elif dx < 0 and dy >= 0:
        collision = ((x2, y2), (x1, y1))
    elif dx >= 0 and dy < 0:
        collision = ((x1, y1 + dy), (x2, y2 - dy))
    else:
        collision = ((x1 - dx, y1), (x2 + dx, y2))
    return collision[0][0] <= coords[0] <= collision[1][0] and collision[0][1] <= coords[1] <= collision[1][1]
