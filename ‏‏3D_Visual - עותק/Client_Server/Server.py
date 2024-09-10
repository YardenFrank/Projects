import socket

import select
from Client_Server.FileHandler import FileHandler
from Client_Server.Protocol import Protocol
from Client_Server.DiffieHellman import DiffieHellman
from os import listdir

MAX_MSG_LENGTH = 10000
SERVER_PORT = 5544
SERVER_IP = '127.0.0.2'
PROJECT_FOLDER = r'Client_Server\Project1\\'
OBJECT_FOLDER = PROJECT_FOLDER + 'Objects\\'
objects_num = len(listdir(OBJECT_FOLDER))

# Diffie-Hellman parameters
DH_PRIME = 23
DH_BASE = 5


class Server(socket.socket):
    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((SERVER_IP, SERVER_PORT))
        self.listen()
        self.protocol = Protocol(self, MAX_MSG_LENGTH)
        print("Listening for clients...")

        self.client_sockets = []  # stores the client's connection
        self.message_to_send = None
        self.file_handler = FileHandler(PROJECT_FOLDER)

        self.diffie_hellman = DiffieHellman(DH_PRIME, DH_BASE)
        self.diffie_hellman.generate_keys()

        self.update()

    def update(self):
        """this is the main loop of the server"""

        while True:
            rlist, wlist, xlist = select.select([self] + self.client_sockets, self.client_sockets, [])
            for index, current_socket in enumerate(rlist):
                if current_socket is self:  # if a client wants to connect
                    self.client_joined(current_socket)

                else:  # if client already joined
                    message = self.protocol.get_data(current_socket)
                    if message:
                        self.receive(current_socket, message)
                self.send_message(current_socket, wlist)

    def receive(self, client, message):
        """this method is the main method for receiving data from clients"""

        if message[0] == 'download':
            current_number = message[1]
            self.file_handler.write_line_to_file(message, self.client_sockets.index(client))
            new_message = ['download', [message[1], self.file_handler.get_object(current_number),
                                        self.file_handler.get_position(current_number - 1)]]
            if new_message[1][0] == objects_num:
                new_message[1][0] = 'last'
            self.protocol.private_message(new_message, client, True)

        elif message[0] == 'again':
            last_request = self.file_handler.get_request(self.client_sockets.index(client))
            self.receive(client, last_request)

        elif message[0] == 'public_key':
            self.arrange_keys(client, message[1])

        elif message[0] == 'alter_all_number':
            self.message_to_send = ['alter_all_number', message[1]]  # data: [object number, new pos]
        elif message[0] == 'alter_one' or message[0] == 'scale' or 'rotate' in message[0]:
            self.message_to_send = message

        elif message[0] == 'add':
            self.add_object(client, message[1])
        elif message[0] == 'save':
            object_num = message[1][0]
            self.file_handler.set_object(object_num, message[1][1])
            self.file_handler.write_line_to_file(message[1][2], object_num - 1, request=False)
            print('saved')

        elif message[0] == 'cut':
            self.file_handler.erase_object(message[1])
            self.message_to_send = message

    def send_message(self, current_client, write_list):
        """sends a message for every client, except for the current one"""

        if self.message_to_send:
            for client in write_list:
                if client is not current_client:
                    self.protocol.private_message(self.message_to_send, client)
            self.message_to_send = None

    def add_object(self, client, data):
        """adds an object on the scene"""

        object_data = self.file_handler.get_object(object_name=data)
        object_number = self.file_handler.get_number_of_objects()
        message = ['add', [object_number, object_data]]  # data: [vertices, faces]
        self.message_to_send = message
        self.file_handler.set_object(object_number + 1, object_data)
        self.protocol.private_message(message, client)

    def arrange_keys(self, client, client_public_key):
        """arranges shared key, using the Diffie-Hellman protocol, and sends the client the public key"""

        self.protocol.private_message(['public_key', self.diffie_hellman.get_public_key()], client)
        shared_key = self.diffie_hellman.generate_shared_key(client_public_key)
        self.protocol.set_key(shared_key)

    def client_joined(self, client):
        """adds client to the client list"""

        connection, client_address = client.accept()

        if len(self.client_sockets) < 7:
            print("New client joined!", client_address)
            self.client_sockets.append(connection)
            self.file_handler.add_new_line()

        else:
            message = ['sorry, the server is full']
            self.protocol.private_message(message, connection)
            connection.close()
