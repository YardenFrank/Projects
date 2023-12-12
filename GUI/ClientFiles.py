import socket
import threading
from ClientFilesGUI import ClientFilesGUI
from os.path import basename

MAX_MSG_LENGTH = 1024
SERVER_PORT = 5557
IP = '127.0.0.2'


class Client(socket.socket, ClientFilesGUI):
    def __init__(self):
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_STREAM)
        thread = threading.Thread(target=self.create_gui)
        thread.start()

        self.connect((IP, SERVER_PORT))

        self.title('File manager')
        print('connected to server.')

        while True:
            self.run_client()

    def run_client(self):
        if self.file_name:  # if the user chose a file to upload
            self.upload()
        if self.to_download:  # if the user chose a file to download
            self.send('b'.encode())
            self.download()

    def upload(self):
        """upload files to the server"""
        actual_file_name = basename(self.file_name)  # find the name of the file from the path
        file_name_length = str(len(actual_file_name)).zfill(2)
        self.send((self.gui_command + file_name_length + actual_file_name).encode())

        with open(self.file_name, 'rb') as file:
            file_data = file.read(MAX_MSG_LENGTH)

            while file_data:  # sends 1024 bytes of the file to the server each iteration
                file_length = str(len(file_data)).zfill(4)
                self.send(file_length.encode())
                self.send(file_data)
                file_data = file.read(MAX_MSG_LENGTH)
            self.send('end.'.encode())  # to tell the server that it sent it all the data

        self.file_name = None
        print('file saved')

    def download(self):
        new_file_path = basename(self.file_downloaded)
        new_file_path_length = str(len(new_file_path)).zfill(2)
        self.send(new_file_path_length.encode())
        self.send(new_file_path.encode())

        file_data_length = int(self.recv(4).decode())
        print(self.file_downloaded)
        with open((self.directory + '/' + basename(self.file_downloaded)), 'wb') as file:  # saving the data in the file
            while file_data_length:  # receives 1024 bytes of the file to the server each iteration
                file_data = self.recv(file_data_length)  # actual data of the file
                file.write(file_data)
                length = self.recv(4).decode()
                if length == 'end.':  # if the file is fully downloaded
                    break
                file_data_length = int(length)

        print('file downloaded')
        self.to_download = False

    def view_file(self):
        """add button that allows to download the files"""

    def create_gui(self):
        ClientFilesGUI.__init__(self)


def main():
    Client()


if __name__ == '__main__':
    main()
