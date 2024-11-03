from src.rabbitmq_client.client_states.base_state import ClientState
from src.rabbitmq_client.client_states.new_request_state import NewRequestState


class ErrorReceivingResponseState(ClientState):
    def connect(self, client):
        pass

    def on_response(self, client, ch, method, props, body):
        pass

    def run(self, client):
        pass

    def cancel_request(self, client):
        pass

    def update_settings(self, client, new_settings):
        client.set_state(NewRequestState())
        client.state.update_settings(client, new_settings)

    def check_connection(self, client):
        pass

    def get_state_str(self):
        return "Ошибка получения ответа"