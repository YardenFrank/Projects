import socket
import select
from datetime import datetime

MAX_MSG_LENGTH = 1024
SERVER_PORT = 5556
SERVER_IP = '0.0.0.0'


print("Setting up server...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()
print("Listening for clients...")
client_sockets = []
messages_to_send = []

while True:
    rlist, wlist, xlist = select.select([server_socket] + client_sockets, client_sockets, [])

    for current_socket in rlist:
        if current_socket is server_socket:
            connection, client_address = current_socket.accept()
            print("New client joined!", client_address)
            client_sockets.append(connection)

        else:
            try:
                data = current_socket.recv(MAX_MSG_LENGTH).decode()
            except ConnectionResetError:
                data = "quit"

            client_name = data
            current_time = "(" + datetime.now().strftime("%H:%M") + ") "

            if data == "quit":
                quitting_message = f"{current_time}{client_name} has left the chat."
                print(quitting_message)
                client_sockets.remove(current_socket)

                if current_socket in wlist:
                    wlist.remove(current_socket)
                current_socket.close()

                messages_to_send.append((server_socket, quitting_message))

            else:
                messages_to_send.append((current_socket, f"{current_time} {client_name}: {data}"))

    for message in messages_to_send:
        current_socket, data = message
        for socket in wlist:
            if socket is not current_socket:
                socket.send(data.encode())
        messages_to_send.remove(message)
