import asyncore
import collections
import logging
import socket
from threading import Thread
import time

MAX_MESSAGE_LENGTH = 1024

class RemoteClient(asyncore.dispatcher):
    
    def __init__(self, host, socket, address):
        asyncore.dispatcher.__init__(self, socket)
        self.host = host
        self.outbox = collections.deque()

    def say(self, message):
        self.outbox.append(message)

    def handle_read(self):
        client_message = self.recv(MAX_MESSAGE_LENGTH)
        self.host.broadcast(client_message)

    def handle_write(self):
        if not self.outbox:
            return
        message = self.outbox.popleft()
        if len(message) > MAX_MESSAGE_LENGTH:
            raise ValueError('Message too long')
        self.send(message)

class Host(asyncore.dispatcher):

    log = logging.getLogger('Host')

    def __init__(self, address=('localhost',9999)):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(address)
        self.listen(1)
        self.remote_clients = []

    def serve_forever(self):
        asyncore.loop()

    def handle_accept(self):
        socket, addr = self.accept()
        self.log.info('Accepted client at %s', addr)
        self.remote_clients.append(RemoteClient(self, socket, addr))

    def handle_read(self):
        self.log.info('Received message: %s', self.read())

    def broadcast(self, message):
        self.log.info('Broadcasting message: %s', message)
        for remote_client in self.remote_clients:
            remote_client.say(message)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('Creating host')
    host = Host()
    logging.info('Listening on %s', host.getsockname())
    logging.info('Looping')
    t = Thread(target=host.serve_forever)
    t.start()
    while True:
        time.sleep(10)
        logging.info('Still alive')
