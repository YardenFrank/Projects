import socket
import threading
from ClientGUI import ClientGUI

MAX_MSG_LENGTH = 1024
SERVER_PORT = 5557
IP = '127.0.0.2'


class Client(socket.socket, ClientGUI):
    def __init__(self):
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_STREAM)
        thread = threading.Thread(target=self.create_gui)
        thread.start()
        self.on = True

        self.name = self.choose_name()
        self.command = '1'
        self.title(self.name)
        print('connected to server.')

        thread = threading.Thread(target=self.type)
        thread.start()  # works in parallel in order to not block the 'receive' method
        self.receive()

    def type(self):
        """send messages to the server"""
        while self.on:
            if self.message:
                self.command = str(self.gui_command)
                my_message = self.use_protocol(self.message)
                self.send(my_message.encode())
                if self.message == 'quit':
                    self.quit()
                self.message = None

    def receive(self):
        """receive messages from the server"""
        while True:
            try:
                length = self.recv(2).decode()
                message = self.recv(int(length)).decode()
            except (ConnectionAbortedError, ValueError):
                self.destroy()
                break

            self.text = message + '\n'
            self.text_widget.insert('insert', self.text)

    def use_protocol(self, message):
        """handle message and send it"""
        name_length = str(len(self.name))
        message_length = len(message)

        if message_length < 10:
            message_length = '0' + str(message_length)
        else:
            message_length = str(message_length)

        if self.command == '5':  # client is supposed to write 'name: message'
            return self.command_5(name_length, message)
        return name_length + self.name + self.command + message_length + message

    def command_5(self, name_length, message):
        user_name = message.partition(' ')[0][0:-1]
        user_name_length = str(len(user_name))
        real_message = message.partition(' ')[2]
        real_message_length = str(len(real_message))
        if len(real_message) < 10:
            real_message_length = '0' + real_message_length

        # name length - name - command - user2 name length - user2 name - message length - message
        return name_length + self.name + self.command + user_name_length + user_name + real_message_length + real_message

    def choose_name(self):
        """choose username - as stated in the protocol"""
        name = '@'
        while name[0] == '@':
            name = input('enter name (cant use @ at start): ')
        self.connect((IP, SERVER_PORT))
        self.send((str(len(name)) + name).encode())
        return name

    def create_gui(self):
        ClientGUI.__init__(self)

    def quit(self):
        self.on = False
        self.close()
        print('disconnected from the server.')


def main():
    Client()


if __name__ == '__main__':
    main()
