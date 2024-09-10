import math
import numpy as np


class Projection:
    def __init__(self, renderer):
        near = renderer.camera.near_plane
        far = renderer.camera.far_plane
        right = math.tan(renderer.camera.h_fov / 2)
        left = -right
        top = math.tan(renderer.camera.v_fov / 2)
        bottom = -top

        m00 = 2 / (right - left)
        m11 = 2 / (top - bottom)
        m22 = (far + near) / (far - near)
        m32 = -2 * near * far / (far - near)
        self.projection_matrix = np.array([
            [m00, 0, 0, 0],
            [0, m11, 0, 0],
            [0, 0, m22, 1],
            [0, 0, m32, 0]
        ])

        # transforming the vertices to the screen's width and height
        hw, hh = renderer.HALF_WIDTH, renderer.HALF_HEIGHT
        self.to_screen_matrix = np.array([
            [hw, 0, 0, 0],
            [0, -hh, 0, 0],
            [0, 0, 1, 0],
            [hw, hh, 0, 1]
        ])
