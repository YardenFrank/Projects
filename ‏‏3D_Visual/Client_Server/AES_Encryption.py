from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
codes = [b'again', b'alter', b'public_key', b'download', b'add', b'save', b'rotate', b'scale', b'cut', b'get_pos']


class AESCipher:
    def __init__(self, key):
        self._key = key

    def encrypt_message(self, message):
        if self.valid_message(message):
            cipher = AES.new(self._key, AES.MODE_ECB)
            padded_message = pad(message, AES.block_size)
            return cipher.encrypt(padded_message)
        return message

    def decrypt_message(self, encrypted_message):
        if self.valid_message(encrypted_message):
            cipher = AES.new(self._key, AES.MODE_ECB)
            return unpad(cipher.decrypt(encrypted_message), AES.block_size)
        return encrypted_message

    @staticmethod
    def valid_message(message):
        for code in codes:
            if code in message:
                return False
        return True

    def get_key(self):
        return self._key

    def set_key(self, key):
        self._key = key
