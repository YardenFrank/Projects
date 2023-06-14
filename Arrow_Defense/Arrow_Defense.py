__author__ = 'Yarden'

from Game import *

pygame.init()
clock = pygame.time.Clock()
game = Game()
pygame.event.set_grab(True)

while True:  # Game Loop
    game.update()

    clock.tick(60)
    pygame.display.update()
