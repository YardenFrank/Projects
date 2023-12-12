import socket
import select
from datetime import datetime

MAX_MSG_LENGTH = 1024
SERVER_PORT = 5557
SERVER_IP = '0.0.0.0'
managers = ['liguy', 'yarden', 'amit', 'harel', 'yahav']


class Server(socket.socket):
    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((SERVER_IP, SERVER_PORT))
        self.listen()
        print("Listening for clients...")

        self.client_sockets = []  # stores the client's connection
        self.client_names = []  # stores the client's name (same order)
        self.messages_to_send = []  # stores all the messages that need to be sent as a tuple
        self.muted_clients = []

        while True:
            self.update()

    def update(self):
        """this is the main loop of the server"""
        rlist, wlist, xlist = select.select([self] + self.client_sockets, self.client_sockets, [])

        for current_socket in rlist:
            if current_socket is self:  # if a client wants to connect
                self.client_joined(current_socket)

            else:
                if len(self.client_names) < len(self.client_sockets):  # adding name to the list
                    name_length = int(current_socket.recv(1).decode())
                    self.client_names.append(current_socket.recv(name_length).decode())
                else:
                    self.decrypt_message(current_socket, wlist)  # main function that handles the protocol
        self.send_messages(self.messages_to_send, wlist)

    def client_joined(self, client):
        """adds client to the client list"""
        connection, client_address = client.accept()
        print("New client joined!", client_address)
        self.client_sockets.append(connection)

    def decrypt_message(self, user, write_list):
        """this works by the protocol of 12.6"""

        length = int(user.recv(1).decode())
        name = user.recv(length).decode()

        if name not in self.muted_clients:
            if name in managers:
                name = '@' + name

            command = int(user.recv(1).decode())

            if command == 1:
                self.send_all(user, name, write_list)
            elif command == 2:
                self.make_manager(user, name.replace('@', ''))
            elif command == 3:
                self.kick(user, name.replace('@', ''), write_list)
            elif command == 4:
                self.mute(user, name.replace('@', ''))
            else:
                self.private_message(user, name)

        else:
            user.recv(1).decode()
            length = int(user.recv(2).decode())
            message = user.recv(length).decode()

            if message == 'quit':
                self.user_quit(user, name, write_list, f"{name} has left the chat.")
            else:
                self.send_to_user(user, "You cannot speak here.")
                user.recv(MAX_MSG_LENGTH)

    @staticmethod
    def send_messages(messages_to_send, write_list):
        """managers and sends all the different messages that
           need to be sent to the clients"""

        for message in messages_to_send:
            current_socket, data = message
            current_time = "(" + datetime.now().strftime("%H:%M") + ") "
            data = current_time + data
            if len(data) < 10:
                data = '0' + str(len(data)) + data
            else:
                data = str(len(data)) + data

            for user in write_list:
                if user is not current_socket:
                    user.send(data.encode())
            messages_to_send.remove(message)

    def send_all(self, user, name, write_list):
        """send to all users - this is used if the command is 1"""

        length = int(user.recv(2).decode())
        message = user.recv(length).decode()

        if message == 'quit':
            self.user_quit(user, name, write_list, f"{name} has left the chat.")
        elif message == 'view-managers':
            message = 'managers: ' + ', '.join(managers)
            self.send_to_user(user, message)
        else:
            self.messages_to_send.append((user, f"{name}: {message}"))

    @staticmethod
    def send_to_user(user, data):
        """send data to a single user"""
        if len(data) < 10:
            data = '0' + str(len(data)) + data
        else:
            data = str(len(data)) + data
        user.send(data.encode())

    def user_quit(self, client, name, write_list, quitting_message):
        """closes the client's socket if he is kicked or quits."""

        print(quitting_message)
        self.client_names.remove(name)
        self.client_sockets.remove(client)

        if client in write_list:
            write_list.remove(client)

        client.close()

        self.messages_to_send.append((self, quitting_message))

    def make_manager(self, user, name):
        """appoints a member as a manager and updates the managers list - if the command is 2"""

        length = int(user.recv(2).decode())
        new_user = user.recv(length).decode()

        if name in managers:
            if new_user in managers:
                self.send_to_user(user, f"{new_user} is already a manager")
            elif new_user not in self.client_names:
                self.send_to_user(user, f"{new_user} is not connected to the server")
            else:
                managers.append(new_user)
                self.messages_to_send.append((self, f"{new_user} is now a manager"))
        else:
            self.send_to_user(user, "you have to be a manager to do that")

    def kick(self, manager, manager_name, write_list):
        """kicks a user out of the chat - if the command is 3"""

        member_name = manager.recv(int(manager.recv(2).decode())).decode()
        if member_name in self.client_names:
            member = self.client_sockets[self.client_names.index(member_name)]

            if manager_name in managers:
                message = f"{member_name} has been kicked from the chat by {manager_name}."
                self.user_quit(member, member_name, write_list, message)
            else:
                self.send_to_user(manager, "you have to be a manager to do that")
        else:
            self.send_to_user(manager, f"{member_name} is not connected to the server")

    def mute(self, manager, manager_name):
        member_name = manager.recv(int(manager.recv(2).decode())).decode()

        if member_name in self.client_names:
            if manager_name in managers:
                self.muted_clients.append(member_name)
                message = f"{member_name} is muted by {manager_name}."
                self.messages_to_send.append((self, message))
            else:
                self.send_to_user(manager, "you have to be a manager to do that")
        else:
            self.send_to_user(manager, f"{member_name} is not connected to the server")

    def private_message(self, user, name):
        length = int(user.recv(1).decode())
        new_user = user.recv(length).decode()
        message_length = int(user.recv(2).decode())
        message = user.recv(message_length).decode()

        current_time = "(" + datetime.now().strftime("%H:%M") + ") "
        name = "!" + name

        message = f"{current_time}{name}: {message}"
        self.send_to_user(self.client_sockets[self.client_names.index(new_user)], message)


def main():
    Server()


if __name__ == '__main__':
    main()
