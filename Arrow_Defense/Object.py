from Settings import *


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super(Platform, self).__init__()
        self.image = platform
        self.rect = self.image.get_rect()
        self.rect.center = (0, int(HEIGHT / 1.94 - (HEIGHT - ground_y)))

    def update(self, surface, offset):
        surface.blit(self.image, offset)


class Castle(pygame.sprite.Sprite):
    def __init__(self):
        super(Castle, self).__init__()
        self.image = castle_image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH + 100, HEIGHT // 1.75)

    def update(self, surface, offset):
        surface.blit(self.image, offset)
