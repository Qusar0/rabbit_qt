from rabbitmq_client.client_states.base_state import ClientState
from rabbitmq_client.client_states.new_request_state import NewRequestState
from rabbitmq_client.client_states.waiting_response_state import WaitingResponseState
import pika
from uuid import uuid4
from protobuf.message_pb2 import Request


class SendingRequestState(ClientState):
    def connect(self, client):
        pass

    def on_response(self, client, ch, method, props, body):
        pass

    def run(self, client):
        if client.reconnecting:
            client.set_state(NewRequestState())
            client.state.connect(client)
            return
        
        if not hasattr(client, 'connection') or client.connection.is_closed:
            client.set_state(NewRequestState())
            client.state.connect(client)

        client.check_connection()

        client.response = None
        client.cancelled = False
        client.request_id = str(uuid4())

        request = Request(
            return_address=client.client_settings['client_uuid'],
            request_id=str(client.request_id),
            proccess_time_in_seconds=client.timeout,
            request=client.value
        )

        client.corr_id = str(uuid4())

        client.channel.basic_publish(
            exchange=client.client_settings['exchange_name'],
            routing_key=client.client_settings['queue_name'],
            properties=pika.BasicProperties(
                reply_to=client.callback_queue,
                correlation_id=client.corr_id
            ),
            body=request.SerializeToString())
        
        client.set_state(WaitingResponseState())
        client.log_signal.emit(f"Отправлен запрос для request_id '{request.request_id}' со значением {request.request}, задержка {client.timeout} сек", 'info')

        client.state.run(client)

    def cancel_request(self, client):
        pass

    def update_settings(self, client, new_settings):
        client.set_state(NewRequestState())
        client.state.update_settings(client, new_settings)

    def check_connection(self, client):
        pass

    def get_state_str(self):
        return "Отправлен запрос"