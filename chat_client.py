import asyncore
import logging
import socket
import sys
from threading import Thread
import time
from collections import deque
import sfml as sf

class ChatClient(asyncore.dispatcher):
    MAX_MESSAGE_LENGTH = 8192

    def __init__(self, name, ui):
        asyncore.dispatcher.__init__(self)
        self.log = logging.getLogger('Client (%7s)' % name)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = name
        self.log.info('Connecting to host at %s', ('107.22.168.57',58025))
        self.connect(('107.22.168.57',58025))
        self.capturing_text = False
        self.buffer = ''
        self.outbox = deque()
        self.chat_log = deque()
        self.ui = ui

    def say(self, message):
        self.outbox.append(message)
        #self.log.info('Enqueued message: %s', message)

    def handle_write(self):
        if not self.outbox:
            return
        message = self.outbox.popleft()
        if len(message) > ChatClient.MAX_MESSAGE_LENGTH:
            raise ValueError('Message too long')
        self.send('[%s] %s ' % (self.name, message))

    def handle_read(self):
        message = self.recv(ChatClient.MAX_MESSAGE_LENGTH)
        self.ui.chat_log.drawable.string = message
        self.log.info('Received message: %s', message)

    def tick(self, events):
        asyncore.loop(count=1)
