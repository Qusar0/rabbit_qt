from rabbitmq_client.client_states.base_state import ClientState
from rabbitmq_client.client_states.response_received_state import ResponseReceivedState
from rabbitmq_client.client_states.waiting_response_calceled_state import WaitingResponseCanceledState
from protobuf.message_pb2 import Response


class WaitingResponseState(ClientState):
    def connect(self, client):
        pass

    def on_response(self, client, ch, method, props, body):
        if props.correlation_id == client.corr_id: 
            client.response = Response()
            client.response.ParseFromString(body)

            client.set_state(ResponseReceivedState())
            client.log_signal.emit(f"Получен ответ для request_id '{client.response.request_id}' со значением {client.response.response}", 'info')
            client.response_received.emit(str(client.response.response))
        else:
            client.log_signal.emit(f"Получен ответ с неподходящим correlation_id {props.correlation_id}. Игнорирование.", 'warning')

    def run(self, client):
        wait_interval = 0.1
        elapsed_time = 0

        while client.response is None and elapsed_time <= client.timeout + wait_interval:
            if client.cancelled:
                client.set_state(WaitingResponseCanceledState())
                client.log_signal.emit(f"Запрос request_id '{client.request_id}' отменён", 'info')
                return
            client.connection.process_data_events(time_limit=wait_interval)
            elapsed_time += wait_interval

        if client.response is None:
            client.set_state(ErrorReceivingResponseState())
            client.log_signal.emit(f"Ответ для request_id '{client.request_id}' не получен в течении {client.timeout} сек.", 'warning')
            client.responce_not_recieved.emit(True)

    def cancel_request(self, client):
        client.cancelled = True

    def update_settings(self, client, new_settings):
        pass

    def check_connection(self, client):
        pass

    def get_state_str(self):
        return "Ожидание ответа"