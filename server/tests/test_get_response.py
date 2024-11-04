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

    def test_get_response_with_valid_integer(self):
        """Тест на корректные целочисленные значения."""
        request_id = "123"
        request_value = 10
        response = self.server.get_response(request_id, request_value)
        self.assertEqual(response.request_id, request_id)
        self.assertEqual(response.response, request_value * 2)

    def test_get_response_with_zero(self):
        """Тест на значение 0."""
        request_id = "124"
        request_value = 0
        response = self.server.get_response(request_id, request_value)
        self.assertEqual(response.request_id, request_id)
        self.assertEqual(response.response, 0)

    def test_get_response_with_negative_integer(self):
        """Тест на отрицательные значения."""
        request_id = "125"
        request_value = -5
        response = self.server.get_response(request_id, request_value)
        self.assertEqual(response.request_id, request_id)
        self.assertEqual(response.response, request_value * 2)

    def test_get_response_with_float(self):
        """Тест на float значение - должен вернуть None."""
        request_id = "126"
        request_value = 5.5
        response = self.server.get_response(request_id, request_value)
        self.assertIsNone(response)

    def test_get_response_with_none(self):
        request_id = "128"
        request_value = None
        response = self.server.get_response(request_id, request_value)
        self.assertIsNone(response)