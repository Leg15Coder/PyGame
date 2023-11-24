import pygame
from entities import Player

FPS = 60


def init():
    global screen, width, height
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    pygame.display.set_caption('TEST')


if __name__ == '__main__':
    screen, running = None, True
    init()
    clock = pygame.time.Clock()
    player = Player(screen, (50, 50))
    while running:
        player.walking()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            player.event_check(event)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
