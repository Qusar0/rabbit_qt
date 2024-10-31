from abc import ABC, abstractmethod

class ClientState(ABC):
    @abstractmethod
    def call(self, client):
        pass


class NewRequestState(ClientState):
    def connect(self, client):
        client.connect()

    def call(self, client):
        client.set_state(SendingRequestState())

    def update_settings(self, client, new_settings):
        client.client_settings = new_settings
        client.log_signal.emit("Настройки обновлены.", 'info')


class SendingRequestState(ClientState):
    def call(self, client):
        client.set_state(WaitingResponseState)


class WaitingResponseState(ClientState):
    def call(self, client):
        client.cancel_request()
        client.set_state(WaitingResponseCanceledState())


class ResponseReceivedState(ClientState):
    def call(self, client):
        client.set_state(SendingRequestState())


class ErrorSendingRequestState(ClientState):
    def call(self, client):
        client.set_state(SendingRequestState())


class ErrorReceivingResponseState(ClientState):
    def call(self, client):
        client.set_state(SendingRequestState())


class WaitingResponseCanceledState(ClientState):
    def call(self, client):
        client.set_state(SendingRequestState())
