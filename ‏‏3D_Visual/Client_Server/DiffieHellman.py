import random


class DiffieHellman:
    def __init__(self, prime, base):
        if type(prime) is not int or prime % 2 == 0:
            raise ValueError('prime is not an integer, or is not even')
        if type(base) is not int or not 1 < base < prime:
            raise ValueError('base is not an integer, or is not less than prime and bigger than 1')

        self.prime, self.base = prime, base
        self._private_key = 0
        self.public_key = 0

    def generate_keys(self):
        self.generate_private_key()
        self.generate_public_key()

    def generate_private_key(self):
        self._private_key = random.randint(1, self.prime - 1)

    def get_private_key(self):
        return self._private_key

    def generate_public_key(self):
        self.public_key = pow(self.base, self._private_key) % self.prime

    def get_public_key(self):
        return self.public_key

    def generate_shared_key(self, key):
        return (pow(key, self._private_key) % self.prime).to_bytes(16, byteorder='big')
