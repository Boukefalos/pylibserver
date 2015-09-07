from mysocket import TcpClient, TcpServer
import time
import unittest

class TestTcpCommunication(unittest.TestCase):
    def setUp(self):        
        self.server = TcpServer('', 10000)
        self.client = TcpClient('localhost', 10000)

        self.server.start()
        self.client.start()
        pass

    def tearDown(self):
        self.client.stop()
        self.server.stop()

    def test_tcp_communication(self):
        for i in range(1, 50):
            self.server.write('server #%d' % i)
            time.sleep(1)

        for i in range(1, 50):
            self.client.write('client #%d' % i)
            time.sleep(1)

if __name__ == '__main__':
    testList = [TestTcpCommunication]
    suite = unittest.TestLoader().loadTestsFromTestCase(unittest.TestCase)
    for testCase in testList:
        suite.addTest(unittest.makeSuite(testCase))
    result = unittest.TestResult()
    suite.run(result)
    print result