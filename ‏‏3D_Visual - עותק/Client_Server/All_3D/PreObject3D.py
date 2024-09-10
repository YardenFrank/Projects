import pygame as pg
from Client_Server.All_3D.MatrixFunctions import *
from Client_Server.All_3D.Button import Button
import numpy as np
from numba import njit


@njit(fastmath=True)
def any_func(arr, a, b):
    return np.any((arr == a) | (arr == b))


CUBE_VERTICES = [(0, 0, 0, 1), (0, 1, 0, 1), (1, 1, 0, 1), (1, 0, 0, 1), (0, 0, 1, 1), (0, 1, 1, 1), (1, 1, 1, 1), (1, 0, 1, 1)]
CUBE_FACES = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 4, 5, 1),
              (2, 3, 7, 6), (1, 2, 6, 5), (0, 3, 7, 4)]


class PreObject3D:
    def __init__(self, renderer, vertices=None, faces=None, filename=None, axes=None, object_number=0):
        self.renderer = renderer
        self.screen = renderer.screen

        if filename:
            self.vertices, self.faces = self.get_object_from_file(filename)
        elif vertices is None or faces is None:
            self.vertices, self.faces = np.array(CUBE_VERTICES), np.array(CUBE_FACES)  # arrays of vertices and lines
        else:
            self.vertices, self.faces = vertices, faces

        self.draw_vertices = False
        self.active_button = None
        self.object_vertices = [Vertex(self.screen, (0, 0), object_number=object_number, number=i) for i in range(len(self.vertices))]

        self.fill = False

        self.axes = axes
        self.color = [100, 170, 200]
        self.color_faces = [(pg.Color(self.color), face) for face in self.faces]

        self.font = pg.font.SysFont('Arial', 20, bold=True)
        self.label = ''

    def draw(self):
        """main function that displays the object"""
        vertices = self.transform_vertices()  # transforming the vertices to display on 2D
        self.draw_polygon(vertices)
        self.update_vertices(vertices)

    def draw_polygon(self, vertices):
        for index, color_face in enumerate(self.color_faces):  # drawing the faces
            color, face = color_face
            polygon = vertices[face]  # get vertices
            if not any_func(polygon, self.renderer.HALF_WIDTH, self.renderer.HALF_HEIGHT):  # if the polygon didn't exit the screen
                if self.fill and len(polygon) >= 3:  # if it's a shape that can be shaded
                    line_thickness = 0  # (fill the polygon)
                else:
                    line_thickness = 2
                pg.draw.polygon(self.screen, color, polygon, line_thickness)  # drawing the face

                if self.label:  # drawing a label if exists
                    text = self.font.render(self.label[index], True, 'white')
                    self.screen.blit(text, polygon[-1])

    def update_vertices(self, vertices):
        for index, vertex in enumerate(vertices):
            object_vertex = self.object_vertices[index]
            object_vertex.set_pos(vertex)
            if self.draw_vertices:
                self.vertices_to_screen(vertex, object_vertex)

    def vertices_to_screen(self, vertex, object_vertex):
        if not any_func(vertex, self.renderer.HALF_WIDTH, self.renderer.HALF_HEIGHT):  # if the vertex didn't exit the screen
            object_vertex.update(not bool(self.active_button))

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

    def transform_vertices(self):
        vertices = self.vertices @ self.renderer.camera.camera_matrix()  # transfer vertices to fit in the camera's coordinate system
        vertices = vertices @ self.renderer.projection.projection_matrix  # transfer vertices to clip space
        vertices /= vertices[:, -1].reshape(-1, 1)  # normalize the value of the vertices (divide by  w)
        vertices[(vertices > 1.5) | (vertices < -1.5)] = 0  # remove te vertices that don't fit into the screen
        vertices = vertices @ self.renderer.projection.to_screen_matrix  # transforming the vertices to the screen's width and height
        vertices = vertices[:, :2]  # considering only the x and y coordinates
        return vertices

    @staticmethod
    def get_object_from_file(file_path):
        vertices, faces = [], []

        with open(file_path, 'r') as object_file:
            for line in object_file:
                if line.startswith('v '):
                    vertices.append([float(i) for i in line.split()[1:]] + [1])
                elif line.startswith('f'):
                    faces_ = line.split()[1:]
                    faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])

        return vertices, faces

    def move_vertex(self, index, rel_pos):
        self.vertices[index][0] += rel_pos[0]
        self.vertices[index][1] += rel_pos[1]

    def is_moving(self):
        if self.axes:
            offset = self.get_offset(self.axes.calc_center(), self.calc_center())
            for value in offset:
                if abs(value) > 0.03:
                    return True
        return False

    def calc_center(self):
        return np.mean(self.vertices, axis=0)

    def update_color(self, color):
        color = list(color)
        self.color_faces = [(pg.Color(color), face) for face in self.faces]

    @staticmethod
    def get_offset(center1, center2):
        return list(np.subtract(center1, center2))[:3]

    def lower_number(self):
        for vertex in self.object_vertices:
            end_number_index = vertex.button_type.index('v')
            number = int(vertex.button_type[:end_number_index])
            vertex.button_type = str(number - 1) + vertex.button_type[end_number_index:]


class Vertex(Button):
    def __init__(self, screen, pos, vertex_size=4, number=0, object_number=0):
        self.vertex_size = vertex_size
        super().__init__(screen, pos, size=(vertex_size * 2, vertex_size * 2), drag=True, buttontype=f'{object_number}vertex{number}')

    def set_pos(self, pos):
        self.rect.center = pos

    def update(self, allowed):
        self.draw(allowed)
        pg.draw.circle(self.screen, 'white', self.rect.center, self.vertex_size)
