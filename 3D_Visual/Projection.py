import numpy as np


class Projection:
    def __init__(self, render):
        hw, hh = render.WIDTH//4, render.HEIGHT//4
        self.to_screen_matrix = np.array([
            [hw, 0, 0, 0],
            [0, -hw, 0, 0],
            [0, 0, 1, 0],
            [hw * 2, hh * 3, 0, 1]
        ])
