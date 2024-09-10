import pygame as pg
from Client_Server.All_3D.PreObject3D import PreObject3D
from Client_Server.All_3D.Button import Button
from Client_Server.All_3D.MatrixFunctions import *
import numpy as np
OBJECTS_FOLDER = r'Client_Server/Project1/'

# shapes' coordinates (homogenous)
CUBE_VERTICES = [(0, 0, 0, 1), (0, 1, 0, 1), (1, 1, 0, 1), (1, 0, 0, 1),
                 (0, 0, 1, 1), (0, 1, 1, 1), (1, 1, 1, 1), (1, 0, 1, 1)]
CUBE_FACES = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 4, 5, 1), (2, 3, 7, 6), (1, 2, 6, 5), (0, 3, 7, 4)]
PYRAMID_VERTICES = [(1, 0, 1, 1), (1, 0, -1, 1), (-1, 0, -1, 1), (-1, 0, 1, 1), (0, 1.6, 0, 1)]
PYRAMID_FACES = [[0, 1, 2, 3], [0, 3, 4], [0, 1, 4], [1, 2, 4], [2, 3, 4]]
POINT_VERTICES = [(0, 0, 0, 1)]
POINT_LINES = []
LINE_VERTICES = [(1, 0, 0, 1), (-1, 0.001, 0, 1)]
LINE_LINES = [(0, 1)]
AXES_VERTICES = [(0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)]
AXES_FACES = [(0, 1), (0, 2), (0, 3)]


class Object3D(PreObject3D):
    def __init__(self, renderer, vertices=None, faces=None, filename=None, pos=None, scaler=1.0, number=0):
        axes = Axes(renderer, number)
        axes.label = None
        axes.scale(0.5)
        if pos:
            axes.translate(pos)
        super().__init__(renderer, vertices, faces, filename, axes, number)
        super().scale(scaler)

    def draw(self):
        super(Object3D, self).draw()
        self.axes.draw()
        self.translate(self.get_offset(self.axes.calc_center(), self.calc_center()))

    def scale(self, times):
        self.vertices = self.vertices @ scale(times)
        pos = self.axes.calc_center()
        self.axes.scale(times)
        rel_pos = self.get_offset(pos, self.axes.calc_center())
        self.axes.translate(rel_pos)

    def get_all_buttons(self):
        return self.axes.buttons + self.object_vertices

    def lower_number(self):
        self.axes.lower_number()
        super().lower_number()


class Cube(Object3D):
    def __init__(self, renderer):
        super().__init__(renderer)


class Pyramid(Object3D):
    def __init__(self, renderer):
        super().__init__(renderer, np.array(PYRAMID_VERTICES), np.array(PYRAMID_FACES, dtype="object"))


class Axes(PreObject3D):
    def __init__(self, renderer, number=0):
        super().__init__(renderer, np.array(AXES_VERTICES), np.array(AXES_FACES))
        self.colors = [pg.Color('red'), pg.Color('green'), pg.Color('blue')]
        self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
        self.label = 'XYZ'
        self.draw_vertices = False

        self.buttons = [Button(self.screen, (0, 0), (0, 0), drag=True, buttontype=f'axis{i}{number}') for i in range(3)]

    def draw(self):
        super().draw()
        self.update_buttons()
        for index, button in enumerate(self.buttons):
            button.draw(True)

    def update_buttons(self):
        for index, button in enumerate(self.buttons):
            width_height, center = self.calc_button_rect(self.object_vertices[0].get_pos(),
                                                         self.object_vertices[index + 1].get_pos())
            button.rect.width, button.rect.height = width_height
            button.rect.center = center

    @staticmethod
    def moving_buttons_func(index, vertices, rel_pos):
        index = -index-1
        for vertex in vertices:
            if index == 1:
                dist = -rel_pos[1]
            else:
                dist = rel_pos[0]
            vertex[index] += dist
        return vertices

    @staticmethod
    def calc_button_rect(pos1, pos2):
        width_height = abs(pos1[0] - pos2[0]) + 10, abs(pos1[1] - pos2[1]) + 10
        center = (pos1[0] + pos2[0]) / 2, (pos1[1] + pos2[1]) / 2
        return width_height, center

    def calc_center(self):
        return np.array(self.vertices[0])

    def get_axis_length(self):
        return self.vertices[1][0] - self.vertices[0][0]

    def lower_number(self):
        super().lower_number()
        for button in self.buttons:
            number = int(button.button_type[5:])
            button.button_type = button.button_type[:5] + str(number - 1)


class Line(PreObject3D):
    def __init__(self, renderer):
        super().__init__(renderer, np.array(LINE_VERTICES), np.array(LINE_LINES))


class Point(PreObject3D):
    def __init__(self, renderer):
        super().__init__(renderer, np.array(POINT_VERTICES), np.array(POINT_LINES))


class Circle(PreObject3D):
    def __init__(self, renderer, vertices_number=36):
        vertices, faces = self.calc_vertices(vertices_number)
        super().__init__(renderer, np.array(vertices), np.array(faces))

    @staticmethod
    def calc_vertices(n):  # n = number of vertices
        angle = 2 * math.pi / n
        vertices = [(math.cos(angle * i), math.sin(angle * i), 0, 1) for i in range(n)]
        faces = [[i for i in range(n)]]
        return vertices, faces


class Deer(Object3D):
    def __init__(self, renderer):
        super().__init__(renderer, filename=OBJECTS_FOLDER + 'Assets/deer.obj', scaler=0.01)


class Tank(Object3D):
    def __init__(self, renderer):
        super().__init__(renderer, filename=OBJECTS_FOLDER + 'Assets/tank.obj', scaler=0.1)


class Sphere(Object3D):
    def __init__(self, renderer):
        super().__init__(renderer, filename=OBJECTS_FOLDER + 'Assets/sphere.obj')
