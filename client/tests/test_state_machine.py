import unittest
from unittest.mock import MagicMock
from src.rabbitmq_client.client_states.new_request_state import NewRequestState
from src.rabbitmq_client.client_states.error_sending_request_state import ErrorSendingRequestState
from src.rabbitmq_client.client_states.error_receiving_response_state import ErrorReceivingResponseState
from src.rabbitmq_client.client_states.sending_request_state import SendingRequestState
from src.rabbitmq_client.client_states.waiting_response_state import WaitingResponseState
from src.rabbitmq_client.client_states.response_received_state import ResponseReceivedState


class MockClient:
    """Mock client to simulate transitions between states."""
    def __init__(self):
        self.client_settings = {'connection_timeout': '5', 'broker_url': 'localhost', 'exchange_name': 'test_exchange', 'queue_name': 'test_queue', 'client_uuid': 'test_uuid'}
        self.state = NewRequestState()
        self.reconnecting = False
        self.log_signal = MagicMock()
        self.response_received = MagicMock()
        self.on_response = MagicMock()
        self.request_id = "test_request_id"
        self.corr_id = None
        self.response = None
        self.cancelled = False

    def start(self):
        self.state.run(self)

    def set_state(self, new_state):
        self.state = new_state

    def check_connection(self):
        pass


class TestClientStates(unittest.TestCase):
    def setUp(self):
        self.client = MockClient()

    def test_new_request_state_transition_to_sending_request(self):
        # Проверяем переход из NewRequestState в SendingRequestState
        self.client.state.run(self.client)
        self.assertIsInstance(self.client.state, SendingRequestState)
        self.client.log_signal.emit.assert_called_with("Подключение установлено успешно.", 'info')

    def test_error_sending_request_state_update_settings(self):
        # Проверяем вызов update_settings и переход в NewRequestState
        self.client.state = ErrorSendingRequestState()
        new_settings = {'connection_timeout': '10', 'broker_url': 'localhost', 'exchange_name': 'test_exchange', 'queue_name': 'test_queue', 'client_uuid': 'test_uuid'}
        self.client.state.update_settings(self.client, new_settings)
        self.assertIsInstance(self.client.state, NewRequestState)
        self.assertEqual(self.client.client_settings['connection_timeout'], '10')

    def test_waiting_response_state_on_response_correct_id(self):
        # Проверяем, что состояние изменяется на ResponseReceivedState при правильном correlation_id
        self.client.state = WaitingResponseState()
        props = MagicMock()
        props.correlation_id = "test_corr_id"
        self.client.corr_id = "test_corr_id"
        body = b'test_response'  # Пример сериализованных данных ответа
        self.client.state.on_response(self.client, None, None, props, body)
        self.assertIsInstance(self.client.state, ResponseReceivedState)
        self.client.response_received.emit.assert_called_once()

    def test_waiting_response_state_on_response_incorrect_id(self):
        # Проверяем, что состояние не меняется при неверном correlation_id
        self.client.state = WaitingResponseState()
        props = MagicMock()
        props.correlation_id = "incorrect_corr_id"
        self.client.corr_id = "test_corr_id"
        body = b'test_response'
        self.client.state.on_response(self.client, None, None, props, body)
        self.assertIsInstance(self.client.state, WaitingResponseState)
        self.client.log_signal.emit.assert_called_with("Получен ответ с неподходящим correlation_id incorrect_corr_id. Игнорирование.", 'warning')

    def test_waiting_response_state_timeout(self):
        # Проверяем, что состояние изменяется на ErrorReceivingResponseState при таймауте
        self.client.state = WaitingResponseState()
        self.client.timeout = 0  # Устанавливаем таймаут в 0, чтобы сразу вызвать ошибку
        self.client.state.run(self.client)
        self.assertIsInstance(self.client.state, ErrorReceivingResponseState)
        self.client.responce_not_recieved.emit.assert_called_once_with(True)

    def test_response_received_state(self):
        # Проверяем правильное отображение состояния
        self.client.state = ResponseReceivedState()
        self.assertEqual(self.client.state.get_state_str(), "Ответ получен")

    def test_error_receiving_response_state(self):
        # Проверяем правильное отображение состояния
        self.client.state = ErrorReceivingResponseState()
        self.assertEqual(self.client.state.get_state_str(), "Ошибка получения ответа")
