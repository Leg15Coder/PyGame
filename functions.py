import os
import pygame


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


def load_image(name, colorkey=None):
    if not os.path.isfile(name):
        raise ImportError(f"Файл с названием {name} не найден")
    image = pygame.image.load(name)
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
    return image
