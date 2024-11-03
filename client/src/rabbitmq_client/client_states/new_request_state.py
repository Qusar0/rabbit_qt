from time import time, sleep
from src.rabbitmq_client.client_states.base_state import ClientState
import pika


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

    def get_state_str(self):
        return "Новый запрос"