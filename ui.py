import pygame
from random import choice
# from behaviors import is_in_rectangle
from db import db


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


class UI(object):
    def __init__(self, manager):
        self.manager = manager
        self.parent = None
        self.size = self.width, self.height = 100, 100
        self.ui = None

    def set_parent(self, scene):
        self.parent = scene
        self.ui = self.parent.scene

    def update(self, event):
        if self.parent is not None:
            self.ui = self.parent.scene
            self.size = self.width, self.height = self.parent.scene.get_size()


class MainMenu(UI):
    def __init__(self, manager):
        super().__init__(manager)
        self.scene = pygame.Surface(manager.size)
        font = pygame.font.Font(None, 50)
        self.start_button = font.render("ИГРАТЬ", True, (100, 255, 100))
        font = pygame.font.Font(None, 50)
        self.settings_button = font.render("НАСТРОЙКИ", True, (100, 255, 100))
        font = pygame.font.Font(None, 50)
        self.quit_button = font.render("ВЫЙТИ", True, (100, 255, 100))

    def start(self):
        self.manager.start = True

    def settings(self):
        pass

    def quit(self):
        pygame.quit()
        del self

    def update(self, event):
        super().update(event)
        self.scene = pygame.transform.scale(self.scene, self.manager.size)
        self.scene.fill(pygame.Color('black'))
        size = width, height = self.manager.size
        start_button_pos = (width // 3, height * 3 // 6)
        settings_button_pos = (width // 3, height * 4 // 6)
        quit_button_pos = (width // 3, height * 5 // 6)
        wid_hei = (self.settings_button.get_width(), self.settings_button.get_height())
        self.scene.blit(self.start_button, start_button_pos)
        pygame.draw.rect(self.scene, (0, 255, 0), (*start_button_pos, *wid_hei), 1)
        self.scene.blit(self.settings_button, settings_button_pos)
        pygame.draw.rect(self.scene, (0, 255, 0), (*settings_button_pos, *wid_hei), 1)
        self.scene.blit(self.quit_button, quit_button_pos)
        pygame.draw.rect(self.scene, (0, 255, 0), (*quit_button_pos, *wid_hei), 1)
        if event is not None:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                start_hv = (start_button_pos[0] + wid_hei[0], start_button_pos[1] + wid_hei[1])
                setting_hv = (settings_button_pos[0] + wid_hei[0], settings_button_pos[1] + wid_hei[1])
                quit_hv = (quit_button_pos[0] + wid_hei[0], quit_button_pos[1] + wid_hei[1])
                if is_in_rectangle(pos, start_button_pos, start_hv):
                    self.start()
                elif is_in_rectangle(pos, settings_button_pos, setting_hv):
                    self.settings()
                elif is_in_rectangle(pos, quit_button_pos, quit_hv):
                    self.quit()


class PlayerUI(UI):
    def __init__(self, player):
        super().__init__(player.parent.manager)
        self.player = player

    def clear(self):
        self.ui.fill(pygame.Color('black'))
        self.ui.set_alpha(100)

    def update(self, event):
        super().update(event)
        x = self.width * self.player.health // 250
        pygame.draw.rect(self.ui, (200, 0, 0), ((33, self.height - 60), (x, 48)), 0)


class Dialog(UI):
    def __init__(self, manager, dialog: int):
        super().__init__(manager)
        self.start = True
        self.step = 0
        self.script = db.get_dialog(dialog)
        self.cur = None
        self.text = str()
        self.chooses = dict()
        self.image = None
        self.background = None
        self.set_next()

    def set_next(self, s=None):
        if s is None:
            cur = choice([x for x in self.script if x['start']])
        else:
            s = int(s)
            cur = choice([x for x in self.script if x['id'] == s])
        self.cur = cur['id']
        self.text = cur['text']
        steps = cur['next_step'].split(', ')
        self.chooses = {ord(x.split(':')[0]): x.split(':')[1:] for x in steps}
        self.step += 1

    def quit(self):
        self.start = False
        self.parent.dialog = None
        del self

    def draw(self):
        pygame.draw.rect(self.ui, (0, 0, 100), ((0, 0), (self.width, 100)), 0)
        font = pygame.font.Font(None, 32)
        text = font.render(self.text, True, (255, 100, 100))
        self.ui.blit(text, (40, 20))
        k = 0
        for i in self.chooses:
            font = pygame.font.Font(None, 24)
            text = font.render(f'{chr(i)}: ' + self.chooses[i][1], True, (255, 100, 100))
            self.ui.blit(text, (40, 100 + k))
            k += 30

    def update(self, event):
        super().update(event)
        self.draw()
        if event is not None:
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key in self.chooses:
                    if self.chooses[key][0] == '0':
                        self.quit()
                    else:
                        self.set_next(self.chooses[key][0])
