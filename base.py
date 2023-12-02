import pygame
from entities import Player, Entity
from blocks import Block
from ui import PlayerUI, MainMenu


def iterable(obj):
    return isinstance(obj, list) or isinstance(obj, tuple)


class ScenesManager(object):
    def __init__(self, size=(800, 600), *args, **kwargs):
        pygame.init()
        self.size = self.width, self.height = size[0], size[1]
        self.clock = pygame.time.Clock()
        self.indexed_scenes = list(args)
        self.main_scenes = dict(kwargs)
        self.main_scenes['MainMenu'] = MainMenu(self)
        self.start = False
        self.main = pygame.display.set_mode(size, pygame.RESIZABLE)
        self.current = None
        self.main.fill((0, 0, 0))
        pygame.display.set_caption('TEST')

    def set_scene(self, scene):
        pass

    def get_scene(self):
        return self.current

    def show(self, event):
        self.size = self.width, self.height = self.main.get_size()
        if self.start:
            if self.current is not None:
                self.current.update(event)
                self.main.blit(self.current.scene, (0, 0))
            elif self.indexed_scenes:
                self.current = self.indexed_scenes[0]
        else:
            self.main_scenes['MainMenu'].update(event)
            self.main.blit(self.main_scenes['MainMenu'].scene, (0, 0))
        pygame.display.flip()

    def add_scene(self, *args, **kwargs):
        self.indexed_scenes += list(args)
        # self.main_scenes |= dict(kwargs)


class Scene(object):
    def __init__(self, manager: ScenesManager, objects=(), *args):
        self.scene = pygame.Surface(manager.size)
        self.manager = manager
        if not iterable(objects):
            objects = (objects,)
        self.objects = {'player': None, 'stative': set(), 'entities': set(), 'others': set()}
        self.coords = (0, 0)
        for obj in list(objects) + list(args):
            obj.parent = self
            if isinstance(obj, Player):
                self.objects['player'] = obj
                self.coords = obj.coords
            elif obj.tangible:
                self.objects['stative'].add(obj)
            elif isinstance(obj, Entity):
                self.objects['entities'].add(obj)
            else:
                self.objects['others'].add(obj)
        self.ui = PlayerUI(self.objects['player'])
        self.ui.set_parent(self)

    def add_objects(self, *args):
        self.objects += list(args)

    def update(self, event):
        if 'player' in self.objects and self.objects['player'] is not None:
            self.scene.fill(pygame.Color('black'))
            self.scene = pygame.transform.scale(self.scene, self.manager.size)
            for obj in self.objects['others']:
                coords = obj.coords[0] - self.coords[0] + self.manager.width // 2, obj.coords[1] - self.coords[
                    1] + self.manager.height // 2
                self.scene.blit(obj.sprite, coords)
            for obj in self.objects['stative']:
                coords = obj.coords[0] - self.coords[0] + self.manager.width // 2, obj.coords[1] - self.coords[
                    1] + self.manager.height // 2
                self.scene.blit(obj.sprite, coords)
            for obj in self.objects['entities']:
                obj.update(event)
                if obj.health <= 0:
                    del obj
                else:
                    coords = obj.coords[0] - self.coords[0] + self.manager.width // 2, obj.coords[1] - self.coords[
                        1] + self.manager.height // 2
                    self.scene.blit(obj.sprite, coords)
            self.objects['player'].update(event)
            if self.objects['player'].health <= 0:
                del self.objects['player']
            else:
                self.coords = self.objects['player'].coords
                self.ui.update()
                self.scene.blit(self.objects['player'].sprite, (self.manager.width // 2, self.manager.height // 2))
        else:
            print('GAME OVER')
