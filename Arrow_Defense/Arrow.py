import math

import pygame.draw

from Settings import *


class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, power, angle):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(arrow_image, (WIDTH // 20, WIDTH // 20)).convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.image = pygame.transform.rotate(self.image, int(angle * 180 / math.pi))
        self.width = self.rect.width // 1.4
        self.height = self.rect.height // 1.55

        self.time = 0
        self.x_start = self.x
        self.y_start = self.y

        self.power = power
        self.angle = angle

        self.disappear = False
        self.kill_time = 50
        self.alpha = 150
        self.disappear_pos = (0, 0)
        self.offset = pygame.Vector2()

    def update(self, surface, offset):
        if not self.disappear:

            # check if arrow has gone off the screen
            if abs(self.rect.left) < (-abs(offset.x)) or self.rect.left > WIDTH or self.rect.top > HEIGHT:
                self.kill()

            self.move(self.power, self.angle)
            self.draw(surface)

            center = self.rect.center
            self.rect.width = self.width
            self.rect.height = self.height
            self.rect.center = center

            if self.rect.y > ground_y:
                self.disappear = True
                hit_sound.play()
                self.disappear_pos = self.rect.topleft
                self.rect.center = ((-100), (-100))

        else:
            self.vanish(surface)

    def move(self, power, angle):
        self.time += 0.25
        arrow_pos = self.path(self.x_start, self.y_start, power, angle, self.time)
        self.x = arrow_pos[0]
        self.y = arrow_pos[1]

    def draw(self, surface):
        x_velocity = math.cos(self.angle) * self.power
        y_velocity = math.sin(self.angle) * self.power - 9.8 * self.time
        rotation = math.atan2(y_velocity, x_velocity) * 180 / math.pi

        if self.time * 4 % 2 == 0:  # every 8 frames update rotation
            image = self.get_right_image()

            self.rotate_center(image, rotation)

        self.rect = self.image.get_rect(center=(self.x - self.offset.x, self.y - self.offset.y))
        self.rect.width = self.width
        self.rect.height = self.height
        surface.blit(self.image, self.rect)

    @staticmethod
    def get_right_image():
        return arrow_image

    def rotate_center(self, image,  angle):
        rot_image = pygame.transform.rotate(image, angle)
        self.image = rot_image.convert_alpha()

    @staticmethod
    def path(start_x, start_y, power, angle, time):
        # x and y vectors
        x_velocity = math.cos(angle) * power
        y_velocity = math.sin(angle) * power

        # x(t) = vx * t
        x_distance = x_velocity * time
        # y(t) = vy * t + 0.5 * g * t^2
        y_distance = (y_velocity * time) + ((-9.8 * time ** 2) / 2)

        new_x = round(x_distance + start_x)
        new_y = round(start_y - y_distance)

        return new_x, new_y

    def vanish(self, surface):
        self.kill_time -= 1
        if self.alpha >= 0:
            self.alpha -= 2

        self.image.set_alpha(self.alpha)
        surface.blit(self.image, self.disappear_pos)

        if self.kill_time <= 0:
            self.kill()
