import pygame
from behaviors import stay, random, to_player, dist, die, attack, dialog, to_player_and_shoot
from datetime import datetime as dt
from datetime import timedelta


class Sprite(object):
    """
        Общий родительский класс для всех объектов на сцене
    """
    def __init__(self, name, coords=(0, 0), tangible=False, visible=True, **kwargs):
        """
        self.sprite: Холст, состоящий из картинки
        self.parent: Сцена, в которой находится данный объект
        :param name: Имя объекта (по имени добавляются картинка, анимации и индивидуальная механика)
        :param coords: Координаты обекта относительно родительского холста
        :param tangible: Является ли объект непроходимым, статичным
        :param visible: Виден ли объект на экране
        """
        self.name = name
        self.coords = coords
        img = pygame.image.load(rf"sprites/{name}/1.png")
        self.sprite = pygame.transform.scale(img, (64, 64))
        self.tangible = tangible
        self.visible = visible
        self.parent = None

    def __del__(self):
        if self.parent is not None:
            for name in self.parent.objects:
                if not isinstance(self.parent.objects[name], Player):
                    for e in self.parent.objects[name]:
                        if e is self:
                            del e
                else:
                    del self.parent.objects[name]

    def set_pos(self, x: float, y: float):
        """
            Устанавливает новые координаты объекта
        :param x: Координата по длине экрана
        :param y: Координата по высоте экрана
        :return: None
        """
        self.coords = (x, y)

    def get_pos(self):
        return self.coords

    def update(self, event):
        """
            Обновляет данные об объекте и выполняет характерные объекту действия
        :param event: Обрабатываемое игровое событие
        :return: None
        """
        pass


class Entity(Sprite):
    def __init__(self, name, coords=(0, 0), visible=True, **kwargs):
        super().__init__(name, coords, False, visible, **kwargs)
        self.state = 'stay'
        self.abilities = dict(kwargs)
        self.target = None
        self.speed = self.abilities['speed'] if 'speed' in self.abilities else 2
        self.health = self.abilities['health'] if 'health' in self.abilities else 100
        self.damage = self.abilities['damage'] if 'damage' in self.abilities else 1
        self.death = self.abilities['death'] if 'death' in self.abilities else die
        cd = self.abilities['cooldown_attack'] if 'cooldown_attack' in self.abilities else 1
        self.cooldown_attack = timedelta(seconds=cd)
        self.current_cooldown_attack = dt.now()

    def check_move(self, coords: tuple):
        if self.parent is not None:
            for obj in self.parent.objects['stative']:
                if obj.collision_box(coords):
                    return False
        return True

    def check_collision(self, obj):
        return obj.collision_box(self.coords)

    def set_img(self, img: str):
        img = pygame.image.load(rf"sprites/{self.name}/{img}.png")
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


class Player(Entity):
    def __init__(self, coords=(0, 0), **kwargs):
        super().__init__('player', coords, True, **kwargs)
        self.quests = set()
        self.speed = 4
        self.walk = 4
        self.inventory = [None] * 33
        self.run = 8
        self.reputation = 0
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


class Enemy(Entity):
    def __init__(self, name, coords=(0, 0), visible=True, **kwargs):
        super().__init__(name, coords, visible, **kwargs)
        self.behaviour = to_player
        self.attack = self.abilities['attack'] if 'attack' in self.abilities else attack

    def update(self, event):
        super().update(event)
        self.attack(self, event)
        self.behaviour(self, event)
        self.goto()


class Boss(Enemy):
    pass


class Ally(Entity):
    pass


class NPC(Entity):
    def __init__(self, name, coords=(0, 0), visible=True, **kwargs):
        super().__init__(name, coords, visible, **kwargs)
        self.behaviour = random

    def update(self, event):
        super().update(event)
        if self.state != 'process':
            self.behaviour(self, event)
        self.goto()




class Shooter(Entity):
    def __init__(self, name, coords=(0, 0), visible=True, **kwargs):
        super().__init__(name, coords, visible, **kwargs)
        self.x_shooter_1 = coords[0]
        self.y_shooter_1 = coords[1]
        self.behaviour_shooter = to_player_and_shoot
        self.attack = self.abilities['attack'] if 'attack' in self.abilities else attack

    def shoot(self, x_player=None, y_player=None, x_shooter=None, y_shooter=None):
        if x_player is not None and y_player is not None:
            self.target_for_shooting = x_player, y_player
            self.coords_shooter = x_shooter, y_shooter

    def update(self, event):
        super().update(event)
        self.attack(self, event)
        self.behaviour_shooter(self, event)
        self.goto()
        self.shoot(x_shooter=self.x_shooter_1, y_shooter=self.y_shooter_1)
