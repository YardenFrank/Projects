from NPC import *
from Enemy_Arrow import EnemyArrow


class Enemy(NPC):
    def __init__(self, image, x, y):
        super(self.__class__, self).__init__(image, x, y)
        self.arrow_image = enemy_arrow
        self.health = 1
        self.in_place = False
        self.last_enemy_x = enemy_stop - enemy_space
        self.miss_delta = 50

    def update(self, surface, arrow_group, pos):
        super(Enemy, self).update(surface, arrow_group, pos)
        if self.health > 0:
            if self.rect.x <= self.last_enemy_x + enemy_space:
                self.in_place = True
            else:
                self.in_place = False
            if not self.in_place:
                self.walk('left')

    def create_arrow(self):
        return EnemyArrow(self.arrow_pos[0], self.arrow_pos[1], self.power, self.angle)

    def random_x(self):
        return random.randint(200, 800)

    def exact_power(self, x):
        return round(0.0002917 * x * x - 0.3083 * x + 205 - (WIDTH - self.rect.x) / 100)

    @staticmethod
    def disappear_pos(sprite):
        return sprite.rect.left + 20, sprite.rect.top + 15
