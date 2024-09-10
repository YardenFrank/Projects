import pygame as pg
from Client_Server.All_3D.MatrixFunctions import *


class Camera:
    def __init__(self, renderer, pos):
        self.renderer = renderer
        self.pos = pos  # camera position
        self.reset_pos = [0.001, 2, -9, 1]

        self.up = np.array([0, 1, 0, 1])  # vectors that define the camera's direction
        self.right = np.array([1, 0, 0, 1])
        self.forward = np.array([0, 0, 1, 1])

        self.h_fov = math.pi / 3  # horizontal and vertical fields of view
        self.v_fov = self.h_fov * (renderer.HEIGHT / renderer.WIDTH)

        self.near_plane = 0.1  # clipping planes for the camera
        self.far_plane = 100

        self.movement_speed = 0.07
        self.rotation_speed = 0.015

        self.angle_pitch = 0
        self.angle_yaw = 0

    def update(self):
        self.move()
        self.update_axis()

    def move(self):
        key = pg.key.get_pressed()
        if key[pg.K_w]:  # movement
            self.pos += self.movement_speed * self.forward
        if key[pg.K_s]:
            self.pos -= self.movement_speed * self.forward
        if key[pg.K_d]:
            self.pos += self.movement_speed * self.right
        if key[pg.K_a]:
            self.pos -= self.movement_speed * self.right
        if key[pg.K_q]:
            self.pos += self.movement_speed * self.up
        if key[pg.K_e]:
            self.pos -= self.movement_speed * self.up

        if key[pg.K_LEFT]:
            self.camera_yaw(-self.rotation_speed)
        if key[pg.K_RIGHT]:
            self.camera_yaw(self.rotation_speed)
        if key[pg.K_UP]:
            if self.angle_pitch > -1.5:
                self.camera_pitch(-self.rotation_speed)
        if key[pg.K_DOWN]:
            if self.angle_pitch < 1.5:
                self.camera_pitch(self.rotation_speed)

        if key[pg.K_r]:  # reset
            self.reset_all()

    def translate_matrix(self):
        x, y, z, w = self.pos
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])

    def rotate_matrix(self):
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])

    def camera_yaw(self, angle):
        self.angle_yaw += angle

    def camera_pitch(self, angle):
        self.angle_pitch += angle

    def reset_axis(self):
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])
        self.forward = np.array([0, 0, 1, 1])

    def reset_all(self):
        self.pos = self.reset_pos
        self.reset_axis()
        self.angle_pitch = 0
        self.angle_yaw = 0

    def is_reset(self):
        return list(self.pos) == self.reset_pos and self.angle_yaw == 0 and self.angle_pitch == 0

    def update_axis(self):
        self.reset_axis()
        rotate = rotate_x(self.angle_pitch) @ rotate_y(self.angle_yaw)

        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def camera_matrix(self):
        # the product of the two matrices above gives the matrix that will allow to make
        # the world's coordinates coincide with the camera's coordinates
        return self.translate_matrix() @ self.rotate_matrix()
