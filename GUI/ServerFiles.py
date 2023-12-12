import socket
import select
import os
from os.path import basename

MAX_MSG_LENGTH = 1024
SERVER_PORT = 5557
SERVER_IP = '0.0.0.0'


class Server(socket.socket):
    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((SERVER_IP, SERVER_PORT))
        self.listen()
        print("Listening for clients...")

        # create folder to save files in
        self.server_path = r'C:\Server_Files'
        if not os.path.exists(self.server_path):
            os.mkdir(self.server_path)

        self.client_sockets = []  # stores the client's connection

        self.update()

    def client_joined(self, client):
        """adds client to the client list"""
        connection, client_address = client.accept()
        print("New client joined!", client_address)
        self.client_sockets.append(connection)

    def update(self):
        """this is the main loop of the server"""

        while True:
            rlist, wlist, xlist = select.select([self] + self.client_sockets, self.client_sockets, [])

            for current_socket in rlist:
                if current_socket is self:  # if a client wants to connect
                    self.client_joined(current_socket)

                else:  # if client already joined
                    try:
                        command = current_socket.recv(1).decode()
                    except UnicodeDecodeError:
                        current_socket.recv(MAX_MSG_LENGTH)
                    # main functions that handles the client's requests
                    else:
                        if command == 'a':
                            self.upload(current_socket)
                        else:
                            self.download(current_socket)

    @staticmethod
    def upload(user):
        # the client socket needs to send:
        # file name length(1) - file name - data length(3) - data

        file_name_length = int(user.recv(2).decode())
        file_name = user.recv(file_name_length).decode()

        new_file_path = rf'C:\Server_Files\{file_name}'
        if not os.path.exists(new_file_path):
            open(new_file_path, 'x')  # create a new file

        file_data_length = int(user.recv(4).decode())
        with open(new_file_path, 'wb') as file:  # saving the data in the file
            while file_data_length:  # receives 1024 bytes of the file to the server each iteration
                file_data = user.recv(file_data_length)  # actual data of the file
                file.write(file_data)
                length = user.recv(4).decode()
                if length == 'end.':
                    break
                file_data_length = int(length)

        print('file saved')

    @staticmethod
    def download(user):
        # sends to client:
        # 1. length (1024 bytes until the last one), 2. actual data
        file_name_length = int(user.recv(2).decode())
        file_name = user.recv(file_name_length).decode()

        for file in os.listdir(r'C:\Server_Files'):
            if basename(file) == basename(file_name):
                file_name = file

        with open('C:\Server_Files\/' + file_name, 'rb') as file:
            file_data = file.read(MAX_MSG_LENGTH)

            while file_data:  # sends 1024 bytes of the file to the server each iteration
                file_length = str(len(file_data)).zfill(4)
                user.send(file_length.encode())
                user.send(file_data)
                file_data = file.read(MAX_MSG_LENGTH)
            user.send('end.'.encode())  # to tell the client that it sent it all the data

        print('file downloaded')


def main():
    Server()


if __name__ == '__main__':
    main()
