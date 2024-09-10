__author__ = 'Yarden Frank'

from Client_Server.All_3D.Projection import Projection
from Client_Server.All_3D.Camera import Camera
from Client_Server.All_3D.Shapes import *
from Client_Server.All_3D.Action_Bar import ActionBar


class Renderer:
    def __init__(self):
        self.RES = self.WIDTH, self.HEIGHT = 1600 * 0.6, 900 * 0.6  # resolution
        self.HALF_WIDTH, self.HALF_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.screen = pg.display.set_mode(self.RES)
        pg.display.set_caption('3D Engine')
        self.FPS = 60

        self.objects = []
        self.object_vertex_alter = None
        self.active_button = None  # button numbers: all bar buttons, object1 buttons - axes, vertices, object2...
        self.last_object_clicked = None
        self.bar_button_handler = ActionBar(self.screen, (self.WIDTH, self.HEIGHT * 0.07), (40, 40, 40))
        self.all_buttons = list(self.bar_button_handler.bar_buttons)[3:]

        self.clock = pg.time.Clock()
        self.camera = Camera(self, [4, 4, -9, 1])  # starting position
        self.camera.camera_pitch(0.4)
        self.camera.camera_yaw(-0.4)
        self.projection = Projection(self)

        pg.font.init()
        self.font = pg.font.SysFont('Arial', int(self.WIDTH * 0.013))
        self.ready = False

        self.objects.insert(0, Axes(self))
        self.run()

    def draw(self):
        self.screen.fill((37, 31, 33))
        for model in sorted(self.objects,
                            key=self.distance_from_camera, reverse=True):  # make objects on top of each other
            model.draw()
        self.bar_button_handler.update()
        self.move_buttons()

        fps = str(int(self.clock.get_fps()))
        position = tuple(self.camera.pos)[:-1]
        position = tuple([math.floor(value * 100) / 100 for value in position])
        text = self.font.render(f'FPS: {fps}   POS: {position}', True, 'white')
        text_rect = text.get_rect()
        text_rect.topleft = (self.WIDTH * 0.02, self.HEIGHT * 0.95)
        self.screen.blit(text, text_rect)

    def get_moving_objects(self):
        moving_objects = []
        if self.ready:
            for index, model in enumerate(self.objects):
                if type(model) is Object3D:
                    if model.is_moving():
                        moving_objects.append(index)
        return moving_objects

    def move_buttons(self):
        for index, button in enumerate(self.all_buttons):
            rel_pos = self.calc_rel(index, button)
            if rel_pos:
                button_type = button.button_type

                if button_type == 'model':
                    button.rel_update_pos(rel_pos)
                elif button_type.startswith('axis'):
                    self.update_last_object(int(button_type[5:]))
                    self.move_axes(rel_pos, button_type)
                elif 'vertex' in button_type:  # example: vertex2, where 2 is the object number
                    self.move_vertices(rel_pos, button_type)
        if not self.active_button:
            self.object_vertex_alter = None

    def calc_rel(self, index, button):
        if button.on and self.active_button is None:  # if the user pressed on the button
            self.active_button = index
            pg.mouse.get_rel()  # then we call this function for pygame to remember the mouse current position

        elif index == self.active_button:  # if it's the same button that was pressed before
            if button.on:
                rel_pos = pg.mouse.get_rel()
                return rel_pos
            else:
                self.active_button = None
        return None

    def move_vertices(self, rel_pos, button_type):
        rel_pos = rel_pos[0] / 120, -rel_pos[1] / 126
        v_pos, x_pos = button_type.index('v'), button_type.index('x')

        object_number, vertex_number = int(button_type[:v_pos]), int(button_type[x_pos + 1:])
        model = self.objects[object_number]
        model.move_vertex(vertex_number, rel_pos)
        model.axes.translate(model.get_offset(model.calc_center(), model.axes.calc_center()))
        self.object_vertex_alter = [object_number, vertex_number, model.vertices[vertex_number]]

    def move_axes(self, rel_pos, button_type):
        rel_pos = rel_pos[0] / 120, -rel_pos[1] / 126
        axis_type = int(button_type[4])
        object_number = int(button_type[5:])
        if object_number < len(self.objects):
            axis = self.objects[object_number].axes
            axis.vertices = self.moving_axes_custom(axis_type, axis.vertices, rel_pos)

    def moving_axes_custom(self, index, vertices, rel_pos):
        for vertex in vertices:
            if index == 0:
                dist = rel_pos[0] * math.copysign(1, self.camera.forward[2])
            elif index == 1:
                dist = rel_pos[1]
            else:
                dist = rel_pos[0] * math.copysign(1, self.camera.pos[0])

            vertex[index] += dist
        return vertices

    def update_last_object(self, button_num):
        if self.last_object_clicked != button_num:
            if self.last_object_clicked:
                last_last_object = self.objects[self.last_object_clicked]
                last_last_object.update_color(last_last_object.color)
            self.last_object_clicked = button_num
            if self.last_object_clicked < len(self.objects):
                self.objects[self.last_object_clicked].update_color([212, 146, 25])

    def distance_from_camera(self, obj):
        if obj.axes:
            return np.linalg.norm(obj.axes.calc_center() - np.array(self.camera.pos))
        return np.linalg.norm(np.array(self.camera.pos))

    def run(self):
        while True:
            if self.ready:
                [(pg.quit(), exit()) for i in pg.event.get() if i.type == pg.QUIT or
                 (i.type == pg.KEYDOWN and i.key == pg.K_ESCAPE)]
                self.draw()
                self.camera.update()
                pg.display.flip()
                self.clock.tick(self.FPS)
