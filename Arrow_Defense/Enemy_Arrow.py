from Settings import *
from Arrow import Arrow


class EnemyArrow(Arrow):
    def __init__(self, x, y, power, angle):
        super(self.__class__, self).__init__(x, y, power, angle)
        self.image = enemy_arrow

    @staticmethod
    def get_right_image():
        return enemy_arrow
