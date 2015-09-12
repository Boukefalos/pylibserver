import asyncore
import socket
import threading
import time

class TcpServer(asyncore.dispatcher):
    clients = []

    def __init__(self, host, port, bufferSize = 1000):
        asyncore.dispatcher.__init__(self)
        self.address = (host, port)
        self.bufferSize = bufferSize

    def handle_accept(self):
        mysocket, address = self.accept()
        print 'Connected from', address
        self.clients.append(TcpServerClient(self, mysocket, self.bufferSize))

    def start(self, thread=True):
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(self.address)
        self.listen(5)
        if thread:
            self.thread = threading.Thread(target=asyncore.loop, kwargs = {'timeout': 1})
            self.thread.start()

    def stop(self):
        self.close()
        if self.thread:
            self.thread.join()


    def write(self, message):
        for client in self.clients:
            client.write(message)

    def input(self, client, data):
        pass

class TcpServerClient(asyncore.dispatcher_with_send):
    queue = []

    def __init__(self, server, socket, bufferSize = 1000):
        asyncore.dispatcher_with_send.__init__(self, socket)
        self.server = server
        self.bufferSize = bufferSize

    def handle_read(self):
        data = self.recv(self.bufferSize)
        if data:
            self.server.input(self, data)

    def handle_close(self):
        print 'Disconnected from', self.getpeername()
        self.close()
        self.server.clients.remove(self)

    def handle_write(self):
        for data in self.queue:
            self.send(data)
        self.queue = []

    def writable(self):
        return len(self.queue) > 0

    def write(self, data):
        self.queue.append(data)

def server_input(client, data):
    print 'server:', data

if __name__ == '__main__':
    server = TcpServer('', 10000)
    server.input = server_input
    server.start()

    for i in range(1, 5000):
        server.write('server #%d' % i)
        time.sleep(1)

    server.stop()