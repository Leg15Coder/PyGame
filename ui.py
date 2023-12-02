import pygame
from entities import Player
from behaviors import is_in_rectangle


class UI(object):
    pass


class MainMenu(UI):
    def __init__(self, manager):
        self.manager = manager
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
