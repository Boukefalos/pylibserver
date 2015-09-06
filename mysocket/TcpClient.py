import asyncore
import socket
import threading
import time

class TcpClient(asyncore.dispatcher):
    queue = []

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.address = (host, port)
        
    def handle_connect(self):
        print "Connected to server"

    def handle_close(self):
        self.close()
    
    def handle_read(self):
        response = self.recv(8192)
        print "Received:", response

    def writable(self):
        return (len(self.queue) > 0)

    def handle_write(self):
        for data in self.queue:
            self.send(data)
        self.queue = []

    def start(self):
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(self.address)
        self.thread = threading.Thread(target=asyncore.loop, kwargs = {'timeout': 1})
        self.thread.start()

    def stop(self):
        self.close()
        self.thread.join()

    def _send(self, data):
        self.queue.append(data)

if __name__ == '__main__':
    client = TcpClient('localhost', 10000)
    client.start()
    
    for i in range(1, 50):
        client.send('client #%d' % i)
        time.sleep(1)
    
    client.stop()