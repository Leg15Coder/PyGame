import os
import pygame
from PIL import Image


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
        raise ImportError(f"Файл с названием {filename} не найден")
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
