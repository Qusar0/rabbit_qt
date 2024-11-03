import unittest
from protobuf.message_pb2 import Request, Response
from rabbitmq_server.server import Server

class TestServer(unittest.TestCase):
    def setUp(self):
        self.server = Server(server_settings=None)

    def test_get_response(self):
        response = self.server.get_response(request_id='1', request=10)
        self.assertEqual(response.request_id, '1')
        self.assertEqual(response.response, 20)

    def test_corrupted_response(self):
        response = self.server.get_response(request_id=1, request='10')
        self.assertEqual(response, None)