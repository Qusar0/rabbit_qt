from abc import ABC, abstractmethod
import pika.adapters.blocking_connection
import pika
from uuid import uuid4
import pika.exceptions
from protobuf.message_pb2 import Response, Request
from time import time, sleep


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

class NewRequestState(ClientState):
    def connect(self, client):
        start_time = time()
        connection_timeout = float(client.client_settings['connection_timeout'])

        while time() - start_time < connection_timeout:
            try:
                client.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=client.client_settings['broker_url'])
                )
                client.channel = client.connection.channel()

                client.channel.exchange_declare(client.client_settings['exchange_name'], 'direct', durable=True)
                client.channel.queue_declare(client.client_settings['queue_name'], durable=True)

                result = client.channel.queue_declare(queue='', exclusive=True)
                client.callback_queue = result.method.queue

                client.channel.basic_consume(
                    queue=client.callback_queue,
                    on_message_callback=client.on_response,
                    auto_ack=True
                )
                client.log_signal.emit("Подключение установлено успешно.", 'info')
                
                if client.reconnecting:
                    client.reconnecting = False
                
                return
            
            except pika.exceptions.AMQPConnectionError as e:
                client.log_signal.emit("Попытка подключения...", 'warning')
                sleep(5)
        
        client.log_signal.emit(f"Не удалось подключиться за {connection_timeout} секунд.", 'error')

    def on_response(self, client, ch, method, props, body):
        pass

    def run(self, client):
        if not client.reconnecting:
            client.set_state(SendingRequestState())
            client.state.run(client)
        else:
            client.state.connect(client)

    def cancel_request(self, client):
        pass

    def update_settings(self, client, new_settings):
        client.client_settings = new_settings
        client.reconnecting = True
        client.start()

    def check_connection(self, client):
        try:
            client.connection.process_data_events(time_limit=0.1)
        except pika.exceptions.StreamLostError:
            print("Потеря соединения с сервером RabbitMQ. Переподключение...")
            client.set_state(NewRequestState())
            client.state.connect(client)
        except pika.exceptions.ConnectionClosed:
            print("Соединение закрыто сервером RabbitMQ.")
            client.set_state(NewRequestState())
            client.state.connect(client)
        except Exception as e:
            print(f"Ошибка: {e}")

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

        client.log_signal.emit(f"Отправлен запрос для request_id '{request.request_id}' со значением {request.request}, задержка {client.timeout} сек", 'info')

        client.set_state(WaitingResponseState())
        client.state.run(client)

    def cancel_request(self, client):
        pass

    def update_settings(self, client, new_settings):
        client.set_state(NewRequestState())
        client.state.update_settings(client, new_settings)

    def check_connection(self, client):
        pass

class WaitingResponseState(ClientState):
    def connect(self, client):
        pass

    def on_response(self, client, ch, method, props, body):
        if props.correlation_id == client.corr_id: 
            client.response = Response()
            client.response.ParseFromString(body)
            client.log_signal.emit(f"Получен ответ для request_id '{client.response.request_id}' со значением {client.response.response}", 'info')
            client.response_received.emit(str(client.response.response))
            client.set_state(ResponseReceivedState())
        else:
            client.log_signal.emit(f"Получен ответ с неподходящим correlation_id {props.correlation_id}. Игнорирование.", 'warning')

    def run(self, client):
        wait_interval = 0.1
        elapsed_time = 0

        while client.response is None and elapsed_time <= client.timeout:
            if client.cancelled:
                client.log_signal.emit(f"Запрос request_id '{client.request_id}' отменён", 'info')
                client.set_state(WaitingResponseCanceledState())
                return
            client.connection.process_data_events(time_limit=wait_interval)
            elapsed_time += wait_interval

        if client.response is None:
            client.log_signal.emit(f"Ответ для request_id '{client.request_id}' не получен в течении {client.timeout} сек.", 'warning')
            client.responce_not_recieved.emit(True)
            client.set_state(ErrorReceivingResponseState())

    def cancel_request(self, client):
        client.cancelled = True

    def update_settings(self, client, new_settings):
        pass

    def check_connection(self, client):
        pass

class ResponseReceivedState(ClientState):
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

class ErrorSendingRequestState(ClientState):
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

class WaitingResponseCanceledState(ClientState):
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