import asyncore
import collections
import logging
import socket
import sys
from threading import Thread
import time

MAX_MESSAGE_LENGTH = 1024

class Client(asyncore.dispatcher):

    def __init__(self, host_address, name):
        asyncore.dispatcher.__init__(self)
        self.log = logging.getLogger('Client (%7s)' % name)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = name
        self.log.info('Connecting to host at %s', host_address)
        self.connect(host_address)
        self.outbox = collections.deque()

    def say(self, message):
        self.outbox.append(message)
        #self.log.info('Enqueued message: %s', message)

    def handle_write(self):
        if not self.outbox:
            return
        message = self.outbox.popleft()
        if len(message) > MAX_MESSAGE_LENGTH:
            raise ValueError('Message too long')
        self.send('[%s] %s ' % (self.name, message)

    def serve_forever(self):
        asyncore.loop()

    def handle_read(self):
        message = self.recv(MAX_MESSAGE_LENGTH)
        self.log.info('Received message: %s', message)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    name = sys.argv[1]
    c = Client(('127.0.0.1', 9999), name)
    message = ' '.join(sys.argv[2:])
    t = Thread(target=c.serve_forever)
    t.start()
    while True:
        c.say(message)
        time.sleep(10)
