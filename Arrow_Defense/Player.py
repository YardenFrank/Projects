import pygame.sprite

from Settings import *
from Arrow import Arrow
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.health = 3
        self.time = 0
        self.arrow_image = arrow_image
        self.bow_image = bow1

        self.player = True

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.collision_rect = self.image.get_rect()

        self.angle = 0
        self.power = start_power
        self.arrow_pos = self.rect.center

        self.arrow_group = pygame.sprite.Group()

        self.player_frame_index = 0
        self.player_animation_list = [pl1, pl2, pl3, pl4, pl5, pl6]

        self.bow_frame_index = 0
        self.bow_animation_list = [bow1, bow2, bow3, bow4, bow5, bow6]
        self.animation_time = 4

        self.speed = 6
        self.y_velocity = 0
        self.ladder_x = [0, WIDTH // 17]
        self.height = y
        self.range = [0, WIDTH // 9.4]

        self.dead = False
        self.dead_time = 50
        self.current_color = (255, 255, 255)

        self.bow_draw_played = False

        self.offset = pygame.Vector2()

    def shoot(self):
        if self.time > 10:
            pos = self.get_position()
            self.angle = self.find_angle(pos, self.get_rect())

            arrow = self.create_arrow()

            self.arrow_group.add(arrow)
            self.time = 0
            self.power = start_power
            self.bow_frame_index = 0

            shot_sound.play()

    def update(self, surface, arrow_group, pos):
        self.time += 1
        self.collision_rect.center = (pos.x, pos.y)
        self.draw(surface, pos)
        self.gravity()

        if self.dead:
            self.death()

        else:
            self.update_animation()
            self.check_collision(arrow_group, self.collision_rect)

            if self.power < max_power:
                if pygame.mouse.get_pressed()[0]:
                    if not self.bow_draw_played:
                        bow_draw.play()
                        self.bow_draw_played = True
                    self.power += 2

    @staticmethod
    def find_angle(pos, rect):  # pos = mouse position
        x = rect.center[0]  # arrow x position
        y = rect.center[1]  # arrow y position

        try:
            arrow_angle = math.atan((y - pos[1]) / (x - pos[0]))
        except ZeroDivisionError:
            arrow_angle = math.pi / 2

        if pos[1] < y and pos[0] > x:
            arrow_angle = abs(arrow_angle)
        elif pos[1] < y and pos[0] < x:
            arrow_angle = math.pi - arrow_angle
        elif pos[1] > y and pos[0] < x:
            arrow_angle = math.pi + abs(arrow_angle)
        elif pos[1] > y and pos[0] > x:
            arrow_angle = (math.pi * 2) - arrow_angle

        return arrow_angle

    def draw(self, surface, position):
        surface.blit(self.image, self.collision_rect)

        orig_center = position
        pos = self.get_position()
        arrow = self.rotate_center(self.arrow_image,
                                   int(self.find_angle(pos, self.get_rect()) * 180 / math.pi)).convert_alpha()
        rect = arrow.get_rect(center=orig_center)

        bow_new = pygame.transform.scale(self.bow_image, (
            self.bow_image.get_width() // 3, self.bow_image.get_height() // 3)).convert_alpha()
        bow_new = self.rotate_center(bow_new,
                                     int(self.find_angle(pos, self.get_rect()) * 180 / math.pi)).convert_alpha()
        bow_rect = bow_new.get_rect(center=orig_center)

        self.arrow_pos = pygame.Vector2(orig_center) + self.offset

        surface.blit(bow_new, bow_rect)
        surface.blit(arrow, rect)

    @staticmethod
    def rotate_center(image, angle):
        """rotate an image while keeping its center and size"""
        rot_image = pygame.transform.rotate(image, angle)
        return rot_image

    def update_animation(self):

        # update bow animation
        if self.power != start_power:

            if self.bow_frame_index < 6 and self.time % 4 == 0:
                # update image depending on current frame
                self.bow_image = self.bow_animation_list[self.bow_frame_index]
                # check if enough time has passed since the last update
                self.bow_frame_index += 1

        else:
            self.bow_image = self.bow_animation_list[0]

    def walk(self, direction):
        # update player animation
        if self.player_frame_index < len(self.player_animation_list) and self.time % self.animation_time == 0:
            image = self.player_animation_list[self.player_frame_index]
            # update image depending on current frame
            if direction == 'right':
                if self.rect.y == self.height:
                    self.image = image
                self.rect.x += self.speed
            else:
                if self.rect.y == self.height:
                    self.image = pygame.transform.flip(image, True, False)
                self.rect.x -= self.speed

            self.player_frame_index += 1

        if self.player_frame_index >= len(self.player_animation_list):
            self.player_frame_index = 0

    def gravity(self):
        self.update_height()
        self.y_velocity += 0.7
        self.rect.y += self.y_velocity
        if self.on_ladder():
            self.y_velocity = 0
        elif self.rect.y >= self.height:
            self.rect.y = self.height
            self.y_velocity = 0

    def update_height(self):
        if ground_y - self.height < WIDTH // 7.5 // 2:
            self.height = ground_y

        elif self.collision_rect.x > self.range[1] - self.offset.x \
                or self.collision_rect.x < self.range[0] - self.offset.x:
            self.change_heights('+')

    def on_ladder(self):
        if self.is_on_ladder():
            if self.collision_rect.y > self.height + 1:
                return False
            if self.collision_rect.y == self.height - HEIGHT // 7.5:
                self.change_heights('-')
                return False

            return True

        elif self.ladder_x[1] * 1.07 > self.collision_rect.x + self.offset.x > self.ladder_x[1] * 0.93:
            if self.collision_rect.y <= self.height - 1:
                return False
            if self.collision_rect.y == self.height + HEIGHT // 7.5:
                self.change_heights('+')
                return False

            return True

        return False

    def is_on_ladder(self):
        return self.ladder_x[0] * 1.07 > self.collision_rect.x + self.offset.x > self.ladder_x[0] * 0.93

    def change_heights(self, sign):
        if sign == '+':
            self.range[1] += WIDTH // 15
            self.range[0] += WIDTH // 20
            self.height += HEIGHT // 7.5
            self.ladder_x[1] += WIDTH // 17
            self.ladder_x[0] += WIDTH // 17
        elif sign == '-':
            self.range[1] -= WIDTH // 15
            self.range[0] -= WIDTH // 20
            self.height -= HEIGHT // 7.5
            self.ladder_x[1] -= WIDTH // 17
            self.ladder_x[0] -= WIDTH // 17
            if self.height == HEIGHT // 1.4:
                self.height -= HEIGHT // 33

    @staticmethod
    def get_position():
        return pygame.mouse.get_pos()

    def create_arrow(self):
        return Arrow(self.arrow_pos[0], self.arrow_pos[1], self.power, self.angle)

    def check_collision(self, arrow_group, rect):
        for sprite in arrow_group.sprites():
            if sprite.rect.colliderect(rect):
                hit_sound.play()
                sprite.disappear = True
                sprite.disappear_pos = self.disappear_pos(sprite)
                sprite.rect.center = ((-100), (-100))
                self.health -= 1
                if self.health <= 0:
                    self.dead = True
                if self.player:
                    hurt_sound.play()

    def get_rect(self):
        return self.collision_rect

    @staticmethod
    def disappear_pos(sprite):
        return sprite.rect.left - 10, sprite.rect.top + 15

    def death(self):
        self.dead_time -= 1

        if self.dead_time >= 0:
            if self.dead_time % 6 == 0:
                if self.current_color != (255, 255, 255):
                    self.current_color = (255, 255, 255)
                else:
                    self.current_color = (255, 0, 0)

            self.image = fill(self.image, self.current_color)

        else:
            self.kill()
