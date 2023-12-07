from entities import Sprite


class Item(Sprite):
    def __init__(self, name: str, coords=None):
        super().__init__(name, coords, False, True)
        self.coords = coords
        self.parent = None
        self.slot = None
        self.count = 1
        self.name = name
        img = pygame.image.load(rf"sprites/items/{name}/1.png")
        self.sprite = pygame.transform.scale(img, (64, 64))

    def pick(self, player):
        self.parent = player
        self.slot = player.get_empty_slot()
        if 0 <= self.slot < 33:
            self.parent.inventory[self.slot] = self
        else:
            self.slot = None


class Weapon(Item):
    pass


class Ability(Item):
    pass


class Decor(Item):
    pass
