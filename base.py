import pygame


class Sprite(object):
    def __init__(self, scene, coords=(0, 0), tangible=False, visible=True):
        self.parent = scene
        self.coords = coords
        self.scene = pygame.Surface(scene.get_size())
        self.tangible = tangible
        self.visible = visible
        self.set_pos(*self.coords)

    def set_pos(self, x: float, y: float):
        self.scene.fill(pygame.Color("black"))
        self.coords = (x, y)
        if self.visible:
            pygame.draw.circle(self.scene, (0, 100, 0), self.coords, 20)
        self.parent.blit(self.scene, (0, 0))

    def get_pos(self):
        return self.coords


class ScenesManager(object):
    def __init__(self, current, *args, **kwargs):
        self.indexed_scenes = list(args)
        self.main_scenes = dict(kwargs)
        self.current = current

    def set_scene(self, scene):
        pass

    def get_scene(self):
        return self.current
