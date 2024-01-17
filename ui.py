import pygame
from random import choice
from functions import is_in_rectangle, load_image, nothing, end
from db import db


class Button(object):
    def __init__(self, parent: object, position: tuple, text: str, function=nothing):
        self.parent = parent
        self.coords = (0, 0)
        self.position = position
        self.width, self.height = 1, 1
        self.function = function
        self.font = pygame.font.SysFont('Impact', 50)
        self.text = self.font.render(text, True, pygame.color.Color('black'))
        self.image = pygame.transform.scale(load_image('sprites/menu/start_button.png', -1), (self.width, self.height))

    def click(self, coords: tuple):
        if is_in_rectangle(coords, self.coords, (self.coords[0] + self.width, self.coords[1] + self.height)):
            self.function()

    def show(self):
        self.coords = self.position[0] * self.parent.width, self.position[1] * self.parent.height
        self.width = self.parent.width // 3
        self.height = self.width // 3
        self.image = pygame.transform.scale(load_image('sprites/menu/start_button.png', -1), (self.width, self.height))
        text_pos = self.coords[0] + self.width // 10, self.coords[1] + self.height // 10
        self.parent.scene.blit(self.image, self.coords)
        self.parent.scene.blit(self.text, text_pos)


class UI(object):
    def __init__(self, manager):
        self.manager = manager
        self.parent = None
        self.size = self.width, self.height = 100, 100
        self.ui = None

    def set_parent(self, scene):
        self.parent = scene
        self.ui = self.parent.scene

    def clear(self):
        self.ui.fill(pygame.Color('black'))
        self.ui.set_alpha(100)

    def update(self, event):
        if self.parent is not None:
            self.ui = self.parent.scene
        if self.manager is not None:
            self.size = self.width, self.height = self.manager.main.get_size()


class Menu(UI):
    pass


class MainMenu(Menu):
    def __init__(self, manager):
        super().__init__(manager)
        self.scene = pygame.Surface(manager.size)
        self.icon = load_image('sprites/menu/icon.png')
        pygame.display.set_icon(self.icon)
        self.start_button = Button(self, (1/3, 3/8), "ИГРАТЬ", function=self.start)
        self.settings_button = Button(self, (1/3, 1/2), "НАСТРОЙКИ", function=self.settings)
        self.quit_button = Button(self, (1/3, 5/8), "ВЫЙТИ", function=self.quit)
        self.main_background = load_image('sprites/menu/1.jpg')

    def start(self):
        self.manager.state = 'game'

    def settings(self):
        pass

    def quit(self):
        end(self.manager)
        del self

    def update(self, event):
        super().update(event)
        self.scene = pygame.transform.scale(self.scene, self.manager.size)
        img = load_image('sprites/menu/1.jpg')
        w, h = img.get_size()
        h = self.width * h // w
        self.main_background = pygame.transform.scale(img, (self.width, h))
        self.scene.blit(self.main_background, (0, -h//3))
        self.start_button.show()
        self.settings_button.show()
        self.quit_button.show()
        if event is not None:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                self.start_button.click(pos)
                self.settings_button.click(pos)
                self.quit_button.click(pos)


class GameMenu(Menu):
    def __init__(self, manager):
        super().__init__(manager)
        self.scene = pygame.Surface(manager.size)
        self.continue_button = Button(self, (1/3, 1/3), "ВЕРНУТЬСЯ В ИГРУ", function=self.close)
        self.menu_button = Button(self, (1/3, 2/3), "ГЛАВНОЕ МЕНЮ", function=self.to_menu)

    def open(self):
        self.manager.state = 'gamemenu'

    def close(self):
        self.manager.state = 'game'

    def to_menu(self):
        self.manager.state = 'mainmenu'

    def update(self, event):
        super().update(event)
        self.scene = pygame.transform.scale(self.scene, self.manager.size)
        self.scene.fill(pygame.Color('white'))
        self.menu_button.show()
        self.continue_button.show()
        if event is not None:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                self.menu_button.click(pos)
                self.continue_button.click(pos)


class Settings(Menu):
    pass


class PlayerUI(UI):
    def __init__(self, player):
        super().__init__(player.parent.manager)
        self.player = player
        self.state = 'game'

    def show_game_ui(self):
        x = self.width * 100 * self.player.health / 250 / self.player.max_health
        pygame.draw.rect(self.ui, (200, 0, 0), ((33, self.height - 60), (x, 48)), 0)
        for k in range(1, 9):
            pos = (32 * k, self.height - 120)
            pygame.draw.rect(self.ui, (0, 100, 10), (pos, (32, 32)), 3)
            item = self.player.inventory[k - 1]
            if item is not None:
                item.sprite = pygame.transform.scale(item.sprite, (32, 32))
                pos = pos[0] + self.player.coords[0] - self.width // 2, pos[1] + self.player.coords[
                    1] - self.height // 2
                item.set_pos(*pos)

    def show_death(self):
        pass

    def show_inventory(self):
        for j in range(4):
            for k in range(1, 9):
                pos = (64 * k + self.width // 10, self.height // 8 + 64 * (j + 1))
                pygame.draw.rect(self.ui, (0, 100, 10), (pos, (64, 64)), 3)
                item = self.player.inventory[8 * j + k - 1]
                if item is not None:
                    item.sprite = pygame.transform.scale(item.sprite, (64, 64))
                    pos = pos[0] + self.player.coords[0] - self.width // 2, pos[1] + self.player.coords[
                        1] - self.height // 2
                    item.set_pos(*pos)

    def update(self, event):
        super().update(event)
        if self.player.parent.objects['player'] != self.player:
            self.player = self.player.parent.objects['player']
        if event is not None:
            if event.type == pygame.KEYDOWN:
                if event.key == 101:
                    self.state = 'inventory' if self.state == 'game' else 'game'
        if self.state == 'game':
            self.show_game_ui()
        elif self.state == 'inventory':
            self.show_inventory()


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