import asyncore
import collections
import logging
import socket
from threading import Thread
import time
import signal
import sys

MAX_MESSAGE_LENGTH = 8192

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

    def handle_close(self):
        self.host.remote_clients.remove(self)

    def shutdown(self):
        self.send(None)

class Host(asyncore.dispatcher):

    log = logging.getLogger('Host')

    def __init__(self, address=('0.0.0.0',58025)):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(address)
        self.listen(5)
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

    def shutdown(self):
        self.broadcast('Shutting down server.')
        self.close()
        for remote_client in self.remote_clients:
            remote_client.shutdown()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # Setup asyncore host for sending/receiving chat updates
    logging.info('Creating host')
    host = Host()
    logging.info('Listening on %s', host.getsockname())
    logging.info('Looping')
    # t = Thread(target=host.serve_forever)
    # t.start()

    # Setup asyncore host for sending/receiving client updates

    try: 
        while True:
            # Process other things
            # Calculations and stuff
            asyncore.loop(count=1)
    except KeyboardInterrupt:
        pass

    logging.info('Shutting down')
    host.shutdown()
    asyncore.loop()
