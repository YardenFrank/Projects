__author__ = 'Yarden Frank'
from Client_Server.Client import Client
from Client_Server.Server import Server
from threading import Thread


def main():
    Thread(target=lambda: Server()).start()
    Client()


if __name__ == '__main__':
    main()
