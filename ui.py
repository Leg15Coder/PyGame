import pygame
from entities import Player


class UI(object):
    pass


class PlayerUI(UI):
    def __init__(self, player: Player):
        self.parent = None
        self.player = player
        self.size = self.width, self.height = 100, 100
        self.ui = None

    def set_parent(self, scene):
        self.parent = scene
        self.ui = self.parent.scene

    def clear(self):
        self.ui.fill(pygame.Color('black'))
        self.ui.set_alpha(100)

    def update(self):
        self.ui = self.parent.scene
        self.size = self.width, self.height = self.parent.scene.get_size()
        x = self.width * self.player.health // 250
        pygame.draw.rect(self.ui, (200, 0, 0), ((33, self.height - 60), (x, 48)), 0)
