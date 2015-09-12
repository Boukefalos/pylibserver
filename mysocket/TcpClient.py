import asyncore
import socket
import threading
import time

class TcpClient(asyncore.dispatcher):
    queue = []

    def __init__(self, host, port, bufferSize = 1000):
        asyncore.dispatcher.__init__(self)
        self.address = (host, port)
        self.bufferSize = bufferSize

    def handle_connect(self):
        print "Connected to server"

    def handle_close(self):
        self.close()

    def handle_read(self):
        self.input(self.recv(self.bufferSize))

    def writable(self):
        return (len(self.queue) > 0)

    def handle_write(self):
        for data in self.queue:
            self.send(data)
        self.queue = []

    def start(self, thread=True):
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(self.address)
        if thread:
            self.thread = threading.Thread(target=asyncore.loop, kwargs = {'timeout': 1})
            self.thread.start()

    def stop(self):
        self.close()
        if self.thread:
            self.thread.join()

    def write(self, data):
        self.queue.append(data)

    def input(self, data):
        pass

def client_input(data):
    print 'client:', data

if __name__ == '__main__':
    client = TcpClient('localhost', 10000)
    client.input = client_input
    client.start()

    for i in range(1, 5000):
        client.write('client #%d' % i)
        time.sleep(1)

    client.stop()