import pickle
from Client_Server.AES_Encryption import AESCipher


class Protocol:
    def __init__(self, socket, max_message_length,):
        self.socket = socket
        self.max_msg_len = max_message_length
        self.AES_cipher = None

    def private_message(self, message, socket, must_arrive=False):
        message = pickle.dumps(message)
        if self.AES_cipher:
            message = self.AES_cipher.encrypt_message(message)

        index, message_length = 0, len(message)
        if must_arrive:
            if message_length <= self.max_msg_len:
                socket.send(b'im' + message)
            else:
                socket.send(b'im' + b'on' + message[:self.max_msg_len - 4])
                index = self.max_msg_len - 4

        while index < message_length - self.max_msg_len:
            new_message = b'on' + message[index:index + self.max_msg_len - 4]
            socket.send(new_message)
            index += self.max_msg_len - 4
        socket.send(message[index:])

    def get_data(self, socket):
        data_received = []
        message = socket.recv(self.max_msg_len)
        must_arrive = message[:2] == b'im'
        if must_arrive:
            message = message[2:]

        while message[:2] == b'on':
            data_received.append(message[2:])
            message = socket.recv(self.max_msg_len)
        data_received.append(message)
        self.clear_socket(socket)

        try:
            complete_message = b''.join(data_received)
            if self.AES_cipher:
                complete_message = self.AES_cipher.decrypt_message(complete_message)
            return pickle.loads(complete_message)
        except Exception as e:
            print(f'Error: {e}, trying again')
            return self.failed_to_receive(socket, must_arrive)

    def failed_to_receive(self, socket, must_arrive=False):
        self.clear_socket(socket)
        if must_arrive:
            socket.send(pickle.dumps(['again']))
        return None

    def clear_socket(self, socket):
        socket.setblocking(False)
        try:
            while True:
                socket.recv(self.max_msg_len)
        except BlockingIOError:
            self.socket.setblocking(True)

    def client_private_message(self, message, must_arrive=False):
        self.private_message(message, self.socket, must_arrive)

    def client_clear_socket(self):
        self.clear_socket(self.socket)

    def client_get_data(self):
        return self.get_data(self.socket)

    def set_key(self, key):
        if not self.AES_cipher:
            self.AES_cipher = AESCipher(key)
        else:
            self.AES_cipher.set_key(key)
