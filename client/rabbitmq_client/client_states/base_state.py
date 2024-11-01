from abc import ABC, abstractmethod


class ClientState(ABC):
    @abstractmethod
    def connect(self, client):
        pass

    @abstractmethod
    def on_response(self, client, ch, method, props, body):
        pass

    @abstractmethod
    def run(self, client):
        pass

    @abstractmethod
    def cancel_request(self, client):
        pass

    @abstractmethod
    def update_settings(self, client, new_settings):
        pass

    @abstractmethod
    def check_connection(self, client):
        pass

    @abstractmethod
    def get_state_str(self):
        pass