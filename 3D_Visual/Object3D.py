import pygame as pg
from MatrixFunctions import *
import numpy as np
from Shapes import *


class Object3D:
    def __init__(self, renderer, name='cube'):
        self.renderer = renderer
        self.vertices, self.lines = self.choose_type(name)  # arrays of vertices and lines
        self.rotate_x(0.4)
        self.angle = 0.003

        self.color = [100, 170, 200]
        self.up_red = True
        self.up_green = False
        self.up_blue = True

    def draw(self):
        vertices = self.vertices @ self.renderer.projection.to_screen_matrix

        projected_vertices = []
        for vertex in vertices:  # drawing the vertices
            x = vertex[0]
            y = vertex[1]
            projected_vertices.append((x, y))
            pg.draw.circle(self.renderer.screen, self.color, (x, y), 4)

        for line in self.lines:  # drawing the edges
            pg.draw.line(self.renderer.screen, self.color, projected_vertices[line[0]], projected_vertices[line[1]])

        self.color[0], self.up_red = self.change_color(self.color[0], self.up_red)  # colors
        self.color[1], self.up_green = self.change_color(self.color[1], self.up_green)
        self.color[2], self.up_blue = self.change_color(self.color[2], self.up_blue)

    def translate(self, pos):
        self.vertices = self.vertices @ translate(pos)

    def scale(self, times):
        self.vertices = self.vertices @ scale(times)

    def rotate_x(self, angle):
        self.vertices = self.vertices @ rotate_x(angle)

    def rotate_y(self, angle):
        self.vertices = self.vertices @ rotate_y(angle)

    def rotate_z(self, angle):
        self.vertices = self.vertices @ rotate_z(angle)

    @staticmethod
    def change_color(color, up):
        if up:
            color += 1
            if color == 255:
                up = False
        else:
            color -= 1
            if color == 0:
                up = True
        return color, up

    @staticmethod
    def choose_type(object_name):
        if not isinstance(object_name, str) or object_name.lower() == 'cube':
            return np.array(CUBE_VERTICES), np.array(CUBE_LINES)
        if object_name.lower() == 'pyramid':
            return np.array(PYRAMID_VERTICES), np.array(PYRAMID_LINES)
        if object_name.lower() == 'line':
            return np.array(LINE_VERTICES), np.array(LINE_LINES)
        else:
            return np.array(POINT_VERTICES), np.array(POINT_LINES)
