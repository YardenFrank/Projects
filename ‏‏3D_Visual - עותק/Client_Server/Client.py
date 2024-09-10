import socket
import time
from threading import Thread
from Client_Server.All_3D.Renderer import Renderer
from Client_Server.All_3D.Shapes import *
from Client_Server.Protocol import Protocol
from pathlib import Path
from Client_Server.DiffieHellman import DiffieHellman


MAX_MSG_LENGTH = 10004
SERVER_PORT = 5544
IP = '127.0.0.2'

# Diffie-Hellman parameters
DH_PRIME = 23
DH_BASE = 5


class Client(socket.socket, Renderer):
    def __init__(self):
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_STREAM)
        Thread(target=lambda: Renderer.__init__(self)).start()
        self.connect((IP, SERVER_PORT))
        self.protocol = Protocol(self, MAX_MSG_LENGTH)
        self.diffie_hellman = DiffieHellman(DH_PRIME, DH_BASE)
        self.diffie_hellman.generate_keys()
        self.protocol.client_private_message(['public_key', self.diffie_hellman.get_public_key()])

        self.messages_to_send = []
        print('connected to server.')

        self.download_object = 1
        time.sleep(0.7)

        thread = Thread(target=self.receive)
        thread.start()
        self.send_data()

    def receive(self):
        while True:
            message = None
            while not message:
                message = self.protocol.client_get_data()  # message: [action, [actual data]]

            if message[0] == 'download':  # ['download', [vertices, faces]]
                if message[1][0] == 'last':
                    self.download(message[1][1], message[1][2], True)
                elif self.download_object == message[1][0]:
                    self.download(message[1][1], message[1][2])

            elif message[0] == 'alter_all_number':  # ['alter_all_number', [object number, new position]]
                self.alter_all(message[1][0], message[1][1])
            elif message[0] == 'alter_one':
                self.alter_one(message[1])
            elif message[0] == 'public_key':
                shared_key = self.diffie_hellman.generate_shared_key(message[1])
                self.protocol.set_key(shared_key)
                self.ask_object_to_download(1)
                print('downloading objects...')

            elif message[0] == 'add':
                self.add(message[1])
            elif message[0] == 'cut':
                self.cut_object(message[1])
            elif message[0] == 'scale':
                current_object = self.objects[message[1][0]]
                size_difference = message[1][1] / current_object.axes.get_axis_length()
                current_object.scale(size_difference)
            elif 'rotate' in message[0]:
                axis = message[0][-1]
                self.rotate_object(message[1][0], axis, message[1][1])

    def send_data(self):
        while True:
            self.check_edit_button()
            self.check_save_button()
            self.check_model_buttons()
            self.send_alter_all()
            self.check_fill_button()
            self.check_plus_minus_buttons()
            self.check_rotation_buttons()
            self.check_cut_button()

            if len(self.messages_to_send) > 0:
                if self.messages_to_send[0][0] == 'important':
                    self.protocol.client_private_message(self.messages_to_send[0][1:], True)
                else:
                    self.protocol.client_private_message(self.messages_to_send[0])
                self.messages_to_send = self.messages_to_send[1:]

    def send_alter_all(self):
        try:
            print('', end='')
            if self.object_vertex_alter:
                self.messages_to_send.append(['alter_one', self.object_vertex_alter])
            else:
                for model_index in self.get_moving_objects():
                    message = ['alter_all_number', [model_index, self.objects[model_index].axes.calc_center()]]
                    self.messages_to_send.append(message)
        except AttributeError:
            pass

    def ask_object_to_download(self, number):
        self.messages_to_send.append(['download', number])

    def download(self, data, pos, last=False):
        if not self.ready:
            if data:
                new_object = Object3D(self, data[0], data[1], number=self.download_object, pos=pos)
            else:
                new_object = Object3D(self, number=1)
                last = True

            self.all_buttons += new_object.get_all_buttons()
            self.objects.append(new_object)
            if not last:
                self.download_object += 1
                self.ask_object_to_download(self.download_object)
            else:
                print('finished downloading')
                self.ready = True

    def add(self, data):
        if data[0] == self.download_object:
            self.download_object += 1
            new_object = Object3D(self, data[1][0], data[1][1], number=self.download_object)
            self.objects.append(new_object)
            self.all_buttons += new_object.get_all_buttons()
            print('object added')

    def alter_all(self, object_num, new_center):
        try:
            model = self.objects[object_num]
            axes = model.axes
            axes.translate(axes.get_offset(new_center, axes.calc_center()))
        except IndexError:
            pass

    def alter_one(self, object_vertex_alter):
        object_number, vertex_number, new_pos = object_vertex_alter

        if len(self.objects) > object_number:
            current_object = self.objects[object_number]
            current_object.vertices[vertex_number] = new_pos
            rel_pos = current_object.get_offset(current_object.calc_center(), current_object.axes.calc_center())
            current_object.axes.translate(rel_pos)

    def check_edit_button(self):
        edit_button = self.bar_button_handler.bar_buttons[0]

        if edit_button.clicked:
            edit = False
            if edit_button.on:
                edit = True
            for model in self.objects[1:]:
                model.draw_vertices = edit

    def check_save_button(self):
        try:
            button = self.bar_button_handler.bar_buttons[1]
            if button.let_go:  # save project
                button.let_go = False
                for index, model in enumerate(self.objects[1:]):
                    self.messages_to_send.append(['save', [index + 1, (model.vertices, model.faces),
                                                           list(model.axes.calc_center())[:3]]])

        except AttributeError:
            pass

    def check_model_buttons(self):
        for button in self.bar_button_handler.bar_buttons[self.bar_button_handler.num_up_buttons:]:
            if button.let_go:
                model_name = Path(button.image_path).stem
                self.messages_to_send.append(['important', 'add', model_name])
                button.update_pos(button.pos_0)
                button.let_go = False

    def check_fill_button(self):
        button = self.bar_button_handler.bar_buttons[2]
        if self.last_object_clicked:
            if button.let_go:
                current_object = self.objects[self.last_object_clicked]
                current_object.fill = not current_object.fill
                button.let_go = False

    def check_plus_minus_buttons(self):
        scale_parameter = 0.0001

        if self.last_object_clicked:
            plus_button, minus_button = self.bar_button_handler.bar_buttons[3:5]

            if plus_button.on or minus_button.on:
                current_object = self.objects[self.last_object_clicked]
                if plus_button.on:
                    current_object.scale(1 + scale_parameter)
                else:
                    current_object.scale(1 - scale_parameter)

                current_size = current_object.axes.get_axis_length()
                self.protocol.client_private_message(['scale', [self.last_object_clicked, current_size]])

    def check_rotation_buttons(self):
        rotation_angle = 0.0003

        if self.last_object_clicked:
            rotate_x_button, rotate_y_button, rotate_z_button = self.bar_button_handler.bar_buttons[5:8]

            if rotate_x_button.on:
                self.rotate_object(self.last_object_clicked, 'x', rotation_angle)
                self.protocol.client_private_message(['rotatex', [self.last_object_clicked, rotation_angle * 20]])
            if rotate_y_button.on:
                self.rotate_object(self.last_object_clicked, 'y', rotation_angle)
                self.protocol.client_private_message(['rotatey', [self.last_object_clicked, rotation_angle * 20]])
            if rotate_z_button.on:
                self.rotate_object(self.last_object_clicked, 'z', rotation_angle)
                self.protocol.client_private_message(['rotatez', [self.last_object_clicked, rotation_angle * 20]])

    def rotate_object(self, object_num, axis, angle):
        if axis == 'x':
            self.objects[object_num].rotate_x(angle)
        elif axis == 'y':
            self.objects[object_num].rotate_y(angle)
        else:
            self.objects[object_num].rotate_z(angle)

    def check_cut_button(self):
        button = self.bar_button_handler.bar_buttons[8]
        if self.last_object_clicked:
            if button.let_go:
                self.messages_to_send.append(['cut', self.last_object_clicked])
                self.cut_object(self.last_object_clicked)
                button.let_go = False

    def cut_object(self, number):
        if len(self.objects) > number:
            self.last_object_clicked = None
            self.object_vertex_alter = None
            self.download_object -= 1
            del self.objects[number]
            for obj in self.objects[number:]:
                obj.lower_number()

    def arrange_positions(self, positions):
        for index, obj in enumerate(self.objects[1:]):
            if type(obj) is Object3D:
                if index < len(positions):
                    obj.axes.translate(positions[index])
