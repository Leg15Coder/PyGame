import pygame
from entities import *
from items import *
from blocks import Block, Wall
from ui import PlayerUI, MainMenu, GameMenu
from functions import load_image, ERROR_IMAGE, loading_progress, max_load
from datetime import datetime as dt, timedelta as dl


def iterable(obj):
    return isinstance(obj, list) or isinstance(obj, tuple)


class ScenesManager(object):
    def __init__(self, size=(800, 600), *args, **kwargs):
        pygame.init()
        self.size = self.width, self.height = size[0], size[1]
        self.clock = dt.now()
        self.indexed_scenes = list(args)
        self.main_scenes = dict(kwargs)
        self.main_scenes['MainMenu'] = MainMenu(self)
        self.main_scenes['GameMenu'] = GameMenu(self)
        self.state = 'mainmenu'
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
        if event is not None and event.type == pygame.KEYDOWN:
            if event.key == 27 and self.state == 'game':
                self.main_scenes['GameMenu'].open()
        if self.state == 'game':
            if self.current is not None:
                self.current.update(event)
                self.main.blit(self.current.scene, (0, 0))
            elif self.indexed_scenes:
                self.current = self.indexed_scenes[0]
        elif self.state == 'mainmenu':
            self.main_scenes['MainMenu'].update(event)
            self.main.blit(self.main_scenes['MainMenu'].scene, (0, 0))
        elif self.state == 'gamemenu':
            self.main_scenes['GameMenu'].update(event)
            self.main.blit(self.main_scenes['GameMenu'].scene, (0, 0))
        pygame.display.flip()

    def load(self):
        global max_load, loading_progress
        print('B')
        with open('data/last_game.txt', 'r') as f:
            lst = tuple(map(str.strip, f.readlines()))
            max_load = len(lst) - 1
            count = 0
            loading_progress = count
            _, n = lst[count].split()
            count += 1
            loading_progress = count
            n = int(n)
            for i in range(n):
                __, index = lst[count].split()
                index = int(index)
                count += 1
                loading_progress = count
                self.add_scene(Scene('test', self))
                names = ('PLAYER', 'ENTITIES', 'OTHERS')
                while lst[count]:
                    s, ____ = lst[count].split()
                    count += 1
                    loading_progress = count
                    if s in names:
                        print(s)
                        if s == names[0]:
                            abilities = dict()
                            while lst[count]:
                                s1 = lst[count]
                                name, val = s1.split(': ')
                                count += 1
                                abilities[name] = val
                            abilities['inventory'] = [None] * 33
                            player = Player(**abilities)
                            self.indexed_scenes[index].add_objects(player)
                        else:
                            ents = list()
                            while lst[count]:
                                ___, cls = lst[count].split()
                                count += 1
                                abilities = dict()
                                # print(loading_progress)
                                while lst[count]:
                                    s1 = lst[count]
                                    name, val = s1.split(': ')
                                    count += 1
                                    abilities[name] = val
                                count += 1
                                ent = eval(f'{cls}(**abilities)')
                                ents.append(ent)
                                loading_progress = count
                            self.indexed_scenes[index].add_objects(*ents)
                        count += 1
            loading_progress = count

    def save(self):
        global max_load, loading_progress
        max_load = 10
        with open('data/last_game.txt', 'w') as f:
            f.write(f'COUNT {len(self.indexed_scenes)}\n')
            count = 0
            for scene in self.indexed_scenes:
                f.write(f'SCENE {count}\n')
                f.write(scene.save())
                count += 1
                loading_progress = count
            f.write('\n')
        loading_progress += 10

    def add_scene(self, *args, **kwargs):
        self.indexed_scenes += list(args)
        for name, val in kwargs:
            self.main_scenes[name] = val


class Scene(object):
    def __init__(self, name: str, manager: ScenesManager, objects=(), *args):
        self.scene = pygame.Surface(manager.size)
        self.name = name
        self.tile_images = {
            'wall': tuple(load_image(f"sprites/blocks/walls/{i}.jpg") for i in range(4)),
            'floor': load_image("sprites/blocks/floors/1.jpg")
        }
        self.day_time = 'day'
        self.tile_width = self.tile_height = 32
        self.manager = manager
        if not iterable(objects):
            objects = (objects,)
        objects = list(objects) + list(args)
        self.objects = {'player': None, 'stative': set(), 'entities': set(), 'others': set()}
        self.coords = (0, 0)
        self.dialog = None
        self.static = pygame.Surface(manager.size)
        self.load_level(f"{name}.txt")
        self.add_objects(*objects)
        self.ui = PlayerUI(self.objects['player'])
        self.ui.set_parent(self)

    def set_tile_image(self, image: str, coords: tuple, **kwargs):
        image = self.tile_images[image]
        image = image[kwargs['index']] if 'index' in kwargs else image
        image = pygame.transform.scale(image, (self.tile_width, self.tile_height))
        self.static.blit(image, coords)

    def load_level(self, filename: str):
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            data = [line.strip() for line in mapFile]
        index = 0
        for line in data:
            index += 1
            if line != 'START':
                kwarg, val = map(str.strip, line.split(':'))
                if kwarg in self.tile_images:
                    self.tile_images[kwarg] = load_image(val)
            else:
                break
        data = data[index:]
        width, height = len(data[0]), len(data)
        self.static = pygame.transform.scale(self.static, (width * self.tile_width, height * self.tile_height))
        for y in range(height):
            for x in range(width):
                xk, yk = x * self.tile_width, y * self.tile_height
                if data[y][x] == '.':
                    self.set_tile_image('floor', (xk, yk))
                elif data[y][x] == '#':
                    i = 0
                    if data[y][x-1] == '#' and data[y][min(x+1, width-1)] == '#':
                        i = 1
                    if data[y-1][x] == '#' and data[min(height-1, y+1)][x] == '#':
                        if i == 1:
                            i = 3
                        else:
                            i = 2
                    self.set_tile_image('wall', (xk, yk), index=i)
                    self.add_objects(Wall(name='NONE', coords=(xk, yk, xk + self.tile_width, yk + self.tile_height)))
                elif data[y][x] == 'P':
                    self.set_tile_image('floor', (xk, yk))
                    self.objects['player'] = Player(name='player', coords=(xk, yk), health=200)
                    self.objects['player'].parent = self
                    self.coords = self.objects['player'].coords

    def add_objects(self, *args):
        for obj in args:
            obj.parent = self
            if obj.tangible:
                self.objects['stative'].add(obj)
            elif isinstance(obj, Player):
                self.objects['player'] = obj
                self.coords = self.objects['player'].coords
            elif isinstance(obj, Entity):
                self.objects['entities'].add(obj)
            else:
                self.objects['others'].add(obj)

    def start_dialog(self, dialog):
        self.dialog = dialog
        self.dialog.parent = self

    def save(self) -> str:
        result = str()
        for name in self.objects:
            if name == 'player':
                self.objects[name].save()
            else:
                for e in self.objects[name]:
                    e.save()
        player = self.objects['player']
        result += 'PLAYER 1\n'
        for ability in player.abilities:
            result += f'{ability}: {player.abilities[ability]}\n'
        result += '\n'
        result += f'ENTITIES {len(self.objects["entities"])}\n'
        count = 0
        for ent in self.objects['entities']:
            cls = str(ent.__class__).split("'")[1].split('.')[-1]
            result += f'{count} {cls}\n'
            for ability in ent.abilities:
                result += f'{ability}: {ent.abilities[ability]}\n'
            count += 1
            result += '\n'
        result += '\n'
        result += f'OTHERS {len(self.objects["others"])}\n'
        count = 0
        for ent in self.objects['others']:
            cls = str(ent.__class__).split("'")[1].split('.')[-1]
            result += f'{count} {cls}\n'
            for ability in ent.abilities:
                result += f'{ability}: {ent.abilities[ability]}\n'
            count += 1
            result += '\n'
        result += '\n'
        result += '\n'
        return result

    def update(self, event):
        if 'player' in self.objects and self.objects['player'] is not None:
            if dt.now() - self.manager.clock >= dl(minutes=5) * 2:
                self.manager.clock = dt.now()
            if dt.now() - self.manager.clock < dl(minutes=5):
                self.scene.fill(pygame.Color('white'))
                self.day_time = 'day'
            else:
                self.scene.fill(pygame.Color('black'))
                self.day_time = 'night'
            self.scene = pygame.transform.scale(self.scene, self.manager.size)
            self.scene.blit(self.static, (self.manager.width // 2 - self.coords[0],
                                          self.manager.height // 2 - self.coords[1]))
            for obj in self.objects['entities']:
                obj.update(event)
                if not obj.is_alive:
                    break
                coords = obj.coords[0] - self.coords[0] + self.manager.width // 2, obj.coords[1] - self.coords[
                    1] + self.manager.height // 2
                self.scene.blit(obj.sprite, coords)
            try:
                for obj in self.objects['others']:
                    obj.update(event)
                    coords = obj.coords[0] - self.coords[0] + self.manager.width // 2, obj.coords[1] - self.coords[
                        1] + self.manager.height // 2
                    self.scene.blit(obj.sprite, coords)
            except:
                pass
            if self.dialog is not None:
                self.dialog.update(event)
            self.objects['player'].update(event)
            if self.objects['player'].health <= 0:
                self.objects['player'].delete()
                del self.objects['player']
            else:
                self.coords = self.objects['player'].coords
                self.ui.update(event)
                self.scene.blit(self.objects['player'].sprite, (self.manager.width // 2, self.manager.height // 2))
        else:
            print('GAME OVER')
