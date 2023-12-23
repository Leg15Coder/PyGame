import os
import sys
import pygame
from PIL import Image
from datetime import timedelta as dl
from behaviors import *


ERROR_IMAGE = "sprites/err.jpg"


def nothing(*args, **kwargs) -> None:
    pass


def end(manager) -> None:
    manager.save()
    pygame.quit()
    sys.exit()


def from_str_to_type(val, cls=None):
    if not isinstance(val, str):
        return val
    if cls in (str, int, float):
        cls = str(cls)[1:-1].split()[1]
        return eval(f'{cls}({val})')
    elif cls is dl:
        h, m, s = map(int, val.split(':'))
        return dl(hours=h, minutes=m, seconds=s)
    elif cls is None:
        if val[0] == '<' and val[-1] == '>':
            try:
                return eval(val[1:-1].replace("'", '').split()[1].split('.')[-1])
            except NameError:
                return val[1:-1].replace("'", '').split()[1].split('.')[-1]
        elif val in ('True', 'False'):
            return True if val == 'True' else False
        elif val.isnumeric():
            return int(val)
        elif val.count('.') == 1:
            i = val.index('.')
            if ('0' + val[:i] + val[i+1:] + '0').isnumeric():
                return float(val)
    elif cls in (tuple, list):
        cls = str(cls)[1:-1].split()[1][1:-1]
        return eval(f"{cls}({val})")
    elif cls is bool:
        return True if val == 'True' else False
    else:
        return None


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


def focus(filename: str) -> None:
    img = Image.open(filename)
    x, y = img.size
    pixels = img.load()
    back = pixels[0, 0]
    mnx, mny, mxx, mxy = x, y, 0, 0
    for i in range(y):
        for j in range(x):
            if pixels[j, i] != back:
                mnx, mny, mxx, mxy = min(mnx, j), min(mny, i), max(mxx, j), max(mxy, i)
    mxx = mxy = max(mxx, mxy)
    img = img.crop((mnx, mny, mxx + 1, mxy + 1))
    k = filename.rfind('.')
    filename = filename[:k] + '-croped' + filename[k:]
    img.save(filename)


def load_image(filename, colorkey=None, crop=False):
    if not os.path.isfile(filename):
        filename = ERROR_IMAGE
    if crop:
        focus(filename)
        k = filename.rfind('.')
        filename = filename[:k] + '-croped' + filename[k:]
    image = pygame.image.load(filename)
    if colorkey is None:
        try:
            image = image.convert_alpha()
        except Exception as ex:
            print(ex)
    else:
        try:
            image = image.convert()
        except Exception as ex:
            print(ex)
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    if crop:
        os.remove(filename)
    return image
