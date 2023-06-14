import random
from Settings import *
from Player import Player
from Arrow import Arrow


class NPC(Player):
    def __init__(self, image, x, y):
        Player.__init__(self, image, x, y)
        self.health = 3
        self.shot_already = False
        self.pos = (0, 0)
        self.power = 100
        self.shoot_time = 250
        self.miss_delta = 20
        self.speed = 4

        self.player = False

        self.player_animation_list = [player_image_1, player_image_2, player_image_3, player_image_4, player_image_5,
                                      player_image_6, player_image_7, player_image_8, player_image_9]

    def update(self, surface, arrow_group, pos):
        self.time += 1
        self.collision_rect.center = (pos.x, pos.y)
        self.draw(surface, pos)

        if self.health <= 0:
            self.death()

        else:
            if self.time % random.randint(3 * self.shoot_time // 4, 4 * self.shoot_time // 3) == 0:
                self.shoot()
                self.shot_already = False
            else:
                self.shot_already = True

            self.update_animation()
            self.check_collision(arrow_group, self.collision_rect)

    def get_position(self):
        if not self.shot_already:
            x = self.random_x()
            needed_power = self.exact_power(x)
            self.power = random.randint(needed_power - self.miss_delta, needed_power + self.miss_delta)
            y = x * (HEIGHT / WIDTH) / 2

            self.pos = (x, y)

        return self.pos

    def random_x(self):
        return random.randint(self.collision_rect.x + 50, self.collision_rect.x + 600)

    def create_arrow(self):
        return Arrow(self.arrow_pos[0], self.arrow_pos[1], self.power, self.angle)

    @staticmethod
    def exact_power(x):
        return round(0.0002917 * x * x - 0.3083 * x + 185)

    def get_rect(self):
        return self.rect
