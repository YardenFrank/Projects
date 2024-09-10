from Client_Server.All_3D.Button import Button
import pygame as pg

IMAGES_PATH = r'Client_Server\Project1\Assets\Images\\'


class ActionBar:
    def __init__(self, screen, size, color):
        self.width, self.length = size
        self.color = color
        self.screen = screen
        self.num_up_buttons, self.num_side_buttons = 0, 0

        self.button_size = (self.length, self.length)
        self.line_color = (105, 105, 105)
        self.up_start, self.side_start = (0, 0), (self.width * 0.91, self.length * 2)
        self.line_positions_up, self.line_positions_side = [], []
        self.bar_buttons = self.create_buttons_up(screen) + self.create_buttons_side(screen)
        self.line_positions_side = self.line_positions_side[:-1]

        self.bounding_rect_up = pg.Rect(self.up_start, (self.width, self.length))
        self.bounding_rect_side = pg.Rect(self.side_start,
                                          (self.length, self.button_size[0] * (self.num_side_buttons + 3.2)))

    def update(self):
        pg.draw.rect(self.screen, self.color, self.bounding_rect_up)
        pg.draw.rect(self.screen, self.color, self.bounding_rect_side)
        for button in self.bar_buttons:
            button.update(True)
        for pos in self.line_positions_up:
            pg.draw.line(self.screen, self.line_color, (pos, 0), (pos, self.length - 1))
        for pos in self.line_positions_side:
            pg.draw.line(self.screen, self.line_color, (self.side_start[0], pos),
                         (self.side_start[0] + self.length - 1, pos))

    def create_buttons_up(self, screen):
        edit_button = Button(screen, (0, 0),
                             image=IMAGES_PATH + 'edit.png',
                             size=(self.button_size[0] * 1.2, self.button_size[1] * 1.2), buttontype='edit')
        save_button = Button(screen, (0, 0), image=IMAGES_PATH + 'save.png',
                             size=(self.button_size[0] * 0.9, self.button_size[1] * 0.9), drag=True, buttontype='save')
        fill_button = Button(screen, (0, 0), image=IMAGES_PATH + 'fill.png',
                             size=self.button_size, drag=True, buttontype='fill')
        plus_button = Button(screen, (0, 0), image=IMAGES_PATH + 'plus.png',
                             size=self.button_size, drag=True, buttontype='plus')
        minus_button = Button(screen, (0, 0), image=IMAGES_PATH + 'minus.png',
                              size=self.button_size, drag=True, buttontype='plus')
        rotate_x_button = Button(screen, (0, 0), image=IMAGES_PATH + 'rotate.png',
                                 size=self.button_size, drag=True, buttontype='rotate',
                                 color=((225, 0, 0), (237, 175, 2)))
        rotate_y_button = Button(screen, (0, 0), image=IMAGES_PATH + 'rotate.png',
                                 size=self.button_size, drag=True, buttontype='rotate',
                                 color=((0, 225, 0), (237, 175, 2)))
        rotate_z_button = Button(screen, (0, 0), image=IMAGES_PATH + 'rotate.png',
                                 size=self.button_size, drag=True, buttontype='rotate',
                                 color=((0, 0, 225), (237, 175, 2)))
        cut_button = Button(screen, (0, 0), image=IMAGES_PATH + 'cut.png',
                            size=(self.button_size[0] * 0.7, self.button_size[1] * 0.7), drag=True, buttontype='cut')

        button_list = [edit_button, save_button, fill_button, plus_button, minus_button, rotate_x_button,
                       rotate_y_button, rotate_z_button, cut_button]
        self.num_up_buttons = len(button_list)
        self.set_pos(button_list, self.up_start, self.length, 0, self.line_positions_up, self.button_size)
        return button_list

    def create_buttons_side(self, screen):
        line_button = Button(screen, (0, 0), image=IMAGES_PATH + 'line.png', size=self.button_size, drag=True,
                             buttontype='model')
        square_button = Button(screen, (0, 0), image=IMAGES_PATH + 'square.png', size=self.button_size, drag=True,
                               buttontype='model')
        triangle_button = Button(screen, (0, 0), image=IMAGES_PATH + 'triangle.png', size=self.button_size, drag=True,
                                 buttontype='model')
        cube_button = Button(screen, (0, 0), image=IMAGES_PATH + 'cube.png', size=self.button_size, drag=True,
                             buttontype='model')
        pyramid_button = Button(screen, (0, 0), image=IMAGES_PATH + 'pyramid.png', size=self.button_size, drag=True,
                                buttontype='model')
        circle_button = Button(screen, (0, 0), image=IMAGES_PATH + 'circle.png', size=self.button_size, drag=True,
                               buttontype='model')
        sphere_button = Button(screen, (0, 0), image=IMAGES_PATH + 'sphere.png', size=self.button_size, drag=True,
                               buttontype='model')

        button_list = [line_button, square_button, triangle_button, cube_button, pyramid_button, circle_button,
                       sphere_button]
        self.num_side_buttons = len(button_list)
        self.set_pos(button_list, self.side_start, self.length, 1, self.line_positions_side, self.button_size)
        return button_list

    @staticmethod
    def set_pos(button_list, pos_0, length, side, line_positions, button_size):  # side: 0 = up, 1 = right
        pos = [pos_0[0] + length // 2, pos_0[1] + length // 2]
        increment = button_size[side] * 1.5
        for button in button_list:
            button.update_pos(pos)
            button.pos_0 = tuple(pos)
            line_positions.append(pos[side] + increment // 2)
            pos[side] += increment
