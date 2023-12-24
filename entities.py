import pygame
from behaviors import stay, random, to_player, dist, die, attack, dialog, to_player_and_shoot
from functions import load_image, from_str_to_type
from datetime import datetime as dt
from datetime import timedelta as dl
from ui import Dialog


class Sprite(object):
    def __init__(self, name='', coords=(0, 0), tangible=False, visible=True, **kwargs):
        self.name = name
        self.abilities = dict(kwargs)
        self.sprite = None
        self.coords = from_str_to_type(coords, tuple)
        self.tangible = from_str_to_type(tangible, bool)
        self.visible = from_str_to_type(visible, bool)
        self.parent = self.abilities['parent'] if 'parent' in self.abilities else None

    def __del__(self):
        self.delete()

    def save(self):
        for name in self.abilities:
            self.abilities[name] = eval(f"self.{name}")
        self.abilities['name'] = self.name
        self.abilities['sprite'] = self.sprite
        self.abilities['coords'] = self.coords
        self.abilities['tangible'] = self.tangible
        self.abilities['visible'] = self.visible
        return self

    def add_ability(self, name: str, val, cls=None):
        self.abilities[name] = from_str_to_type(val, cls)
        return val

    def delete(self):
        flag = False
        to_del = None
        if self.parent is not None:
            for name in self.parent.objects:
                if not isinstance(self.parent.objects[name], Player):
                    for e in self.parent.objects[name]:
                        if e is self:
                            to_del = (name, e)
                            flag = True
                            break
                if flag:
                    break
        if to_del is not None:
            self.parent.objects[to_del[0]].remove(to_del[1])
        del self

    def set_pos(self, x: float, y: float):
        self.coords = (x, y)

    def get_pos(self):
        return self.coords

    def set_visible(self, visible: bool):
        self.visible = visible

    def update(self, event):
        pass


class Shard(Sprite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.moving = from_str_to_type(self.abilities['moving'], tuple) if 'moving' in self.abilities \
            else self.add_ability('moving', (0, 0))
        self.sprite = pygame.surface.Surface((8, 8))
        pygame.draw.circle(self.sprite, (200, 10, 10), (4, 4), 4, 4)

    def check_move(self, coords: tuple):
        if self.parent is not None:
            x, y = self.parent.objects['player'].coords
            if dist((x + 32, y + 32), coords) <= 33:
                self.parent.objects['player'].health -= 1
                return False
            for obj in self.parent.objects['stative']:
                if obj.collision_box(coords):
                    return False
        return True

    def update(self, event):
        super().update(event)
        pos = self.coords[0] + self.moving[0], self.coords[1] + self.moving[1]
        self.set_pos(*pos)
        if not self.check_move(self.coords):
            self.delete()


class Entity(Sprite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        name = kwargs['name'] if 'name' in kwargs else ''
        img = load_image(rf"sprites/{name}/1.png", -1, True)
        self.sprite = pygame.transform.scale(img, (64, 64))
        self.state = self.abilities['state'] if 'state' in self.abilities else self.add_ability('state', 'stay')
        self.target = None
        self.speed = from_str_to_type(self.abilities['speed']) if 'speed' in self.abilities \
            else self.add_ability('speed', 2)
        self.max_health = from_str_to_type(self.abilities['max_health']) if 'max_health' in self.abilities \
            else self.add_ability('max_health', 100)
        self.health = from_str_to_type(self.abilities['health']) if 'health' in self.abilities \
            else self.add_ability('health', 100)
        self.damage = from_str_to_type(self.abilities['damage']) if 'damage' in self.abilities \
            else self.add_ability('damage', 0)
        self.death = from_str_to_type(self.abilities['death']) if 'death' in self.abilities \
            else self.add_ability('death', die)
        self.cooldown_attack = from_str_to_type(self.abilities['cooldown_attack'], dl) \
            if 'cooldown_attack' in self.abilities else self.add_ability('cooldown_attack', dl(seconds=1))
        self.current_cooldown_attack = dt.now()
        self.is_alive = True

    def check_move(self, coords: tuple):
        if self.parent is not None:
            for obj in self.parent.objects['stative']:
                if obj.collision_box(coords):
                    return False
        return True

    def check_collision(self, obj):
        return obj.collision_box(self.coords)

    def set_img(self, img: str):
        img = load_image(rf"sprites/{self.name}/{img}.png", -1)
        self.sprite = pygame.transform.scale(img, (64, 64))

    def goto(self, x=None, y=None):
        if x is not None and y is not None:
            self.target = x, y
        elif self.coords != self.target and self.target is not None:
            self.state = 'process'
            x, y = self.target
            coords = self.coords
            if y < self.coords[1]:
                coords = (coords[0], coords[1] - min(self.speed, self.coords[1] - y))
            elif y > self.coords[1]:
                coords = (coords[0], coords[1] + min(self.speed, y - self.coords[1]))
            if self.check_move(coords):
                self.coords = coords
                self.set_pos(*self.coords)
            else:
                coords = self.coords
            if x > self.coords[0]:
                coords = (coords[0] + min(self.speed, x - self.coords[0]), coords[1])
            elif x < self.coords[0]:
                coords = (coords[0] - min(self.speed, self.coords[0] - x), coords[1])
            if self.check_move(coords):
                self.coords = coords
                self.set_pos(*self.coords)
            else:
                self.target = None
                self.state = 'stay'
        else:
            self.target = None
            self.state = 'stay'

    def update(self, event):
        super().update(event)
        if self.health <= 0:
            self.death(self, event)
            self.is_alive = False


class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.quests = set()
        self.walk = from_str_to_type(self.abilities['walk']) if 'walk' in self.abilities \
            else self.add_ability('walk', 4)
        self.inventory = from_str_to_type(self.abilities['inventory'], list) if 'inventory' in self.abilities \
            else self.add_ability('inventory', [None] * 33)
        self.run = from_str_to_type(self.abilities['run']) if 'run' in self.abilities else self.add_ability('run', 8)
        self.reputation = from_str_to_type(self.abilities['reputation']) if 'reputation' in self.abilities \
            else self.add_ability('reputation', 0)
        self.events = {119: False, 115: False, 97: False, 100: False, 1073742048: False}

    def get_empty_slot(self):
        return self.inventory.index(None)

    def event_check(self, event):
        if event is not None:
            if event.type == pygame.KEYDOWN:
                symb = event.key
                print(symb)
                self.events[symb] = True
            if event.type == pygame.KEYUP:
                symb = event.key
                self.events[symb] = False

    def walking(self):
        coords = self.coords
        flag = False
        if self.events[119]:
            coords = (coords[0], coords[1] - self.speed)
            flag = True
        if self.events[115]:
            coords = (coords[0], coords[1] + self.speed)
            flag = True
        if self.events[100]:
            coords = (coords[0] + self.speed, coords[1])
            flag = True
        if self.events[97]:
            coords = (coords[0] - self.speed, coords[1])
            flag = True
        if self.check_move(coords):
            self.coords = coords
            self.set_pos(*self.coords)
        if flag and self.parent is not None:
            if self.events[1073742048]:
                self.speed = self.run
                self.state = 'running'
            else:
                self.speed = self.walk
                self.state = 'walking'
        else:
            self.state = 'stay'

    def update(self, event):
        super().update(event)
        self.event_check(event)
        self.walking()
        if self.state == 'stay':
            self.set_img(f"{1}")
        elif self.state == 'walking':
            self.set_img(f"{dt.now().microsecond // 1000 % 1000 // 334 + 1}")
        elif self.state == 'running':
            self.set_img(f"{dt.now().microsecond // 500 % 500 // 167 + 1}")
        if any(self.inventory):
            for e in self.inventory:
                if e is not None:
                    e.use(self.coords)

    def delete(self):
        for e in self.inventory:
            if e is not None:
                e.delete()
        super().delete()


class Enemy(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.attack = from_str_to_type(self.abilities['attack']) if 'attack' in self.abilities \
            else self.add_ability('attack', attack)
        self.shard = from_str_to_type(self.abilities['shard']) if 'shard' in self.abilities \
            else self.add_ability('shard', Shard)
        if isinstance(self.shard, str):
            self.shard = eval(self.shard)

    def update(self, event):
        super().update(event)
        self.attack(self, event)
        self.goto()


class Boss(Enemy):
    pass


class Ally(Entity):
    pass


class NPC(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.behaviour = from_str_to_type(self.abilities['behaviour']) if 'behaviour' in self.abilities \
            else self.add_ability('behaviour', random)
        self.dialog = Dialog

    def update(self, event):
        super().update(event)
        if self.state != 'process':
            self.behaviour(self, event)
        self.goto()
