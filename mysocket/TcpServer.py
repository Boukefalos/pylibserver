import asyncore
import socket
import threading
import time

class TcpServer(asyncore.dispatcher):
    clients = []

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.address = (host, port)

    def handle_accept(self):
        mysocket, address = self.accept()
        print 'Connected from', address
        self.clients.append(TcpServerClient(self, mysocket))

    def start(self):
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(self.address)
        self.listen(5)
        self.thread = threading.Thread(target=asyncore.loop, kwargs = {'timeout': 0.5})
        self.thread.start()
    
    def stop(self):
        self.close()
        self.thread.join()

    def send(self, message):
        for client in self.clients:
            client._send(message)

    def input(self, client, data):
        print 'input from ', client.getpeername(), ': ', data

class TcpServerClient(asyncore.dispatcher_with_send):
    queue = []

    def __init__(self, server, mysocket):
        asyncore.dispatcher_with_send.__init__(self, mysocket)
        self.server = server

    def handle_read(self):
        data = self.recv(8192)
        if data:
            self.server.input(self, data)

    def handle_close(self):
        print 'Disconnected from', self.getpeername()

    def handle_write(self):
        for data in self.queue:
            self.send(data)
        self.queue = []

    def writable(self):
        return len(self.queue) > 0

    def _send(self, data):
        self.queue.append(data)

if __name__ == '__main__':
    server = TcpServer('', 10000)
    server.start()
    
    for i in range(1, 50):
        server.send('server #%d' % i)
        time.sleep(1)
    
    server.stop()