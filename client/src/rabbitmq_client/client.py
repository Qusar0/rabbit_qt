from PyQt5.QtCore import QThread, pyqtSignal
from src.rabbitmq_client.client_states.new_request_state import NewRequestState
from src.rabbitmq_client.client_states.sending_request_state import SendingRequestState


class Client(QThread):
    response_received = pyqtSignal(str)
    log_signal = pyqtSignal(str, str)
    state_status = pyqtSignal(str)
    responce_not_recieved = pyqtSignal(bool)

    def __init__(self, client_settings):
        super().__init__()

        self.client_settings = client_settings
        self.request_id = None
        self.response = None
        self.cancelled = False
        self.reconnecting = False
        self.set_state(NewRequestState())

    def set_state(self, new_state):
        self.state = new_state
        self.log_signal.emit(f"Состояние изменилось на {self.state.__class__.__name__}", 'debug')
        self.state_status.emit(f"{self.state.get_state_str()}")

    def call(self, value, timeout):
        self.set_state(SendingRequestState())
        self.value = value
        self.timeout = timeout
        self.start()

    def connect(self):
        self.state.connect(self)

    def on_response(self, ch, method, props, body):
        self.state.on_response(self, ch, method, props, body)

    def run(self):
        self.state.run(self)

    def cancel_request(self):
        self.state.cancel_request(self)

    def update_settings(self, new_settings):
        self.state.update_settings(self, new_settings)

    def check_connection(self):
        self.state.check_connection(self)