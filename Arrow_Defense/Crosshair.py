
from Settings import *


class Crosshair:
    def __init__(self, scale):
        image = pygame.image.load('assets/crosshair.png').convert_alpha()
        image = fill(image, (0, 0, 0))
        width = image.get_width()
        height = image.get_height()

        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()

    def draw(self, surface):
        mx, my = pygame.mouse.get_pos()
        self.rect.center = (mx, my)
        surface.blit(self.image, self.rect)
