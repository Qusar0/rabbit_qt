import pika.adapters.blocking_connection
from PyQt5.QtCore import QThread, pyqtSignal
import pika
from uuid import uuid4
import pika.exceptions
from protobuf.message_pb2 import Response, Request
from time import time, sleep
from client_states import *


class Client(QThread):
    response_received = pyqtSignal(str)
    log_signal = pyqtSignal(str, str)
    responce_not_recieved = pyqtSignal()

    def __init__(self, client_settings):
        super().__init__()

        self.client_settings = client_settings
        self.request_id = None
        self.response = None
        self.cancelled = False
        self.reconnecting = False
        self.state = None

    def set_state(self, new_state):
        self.state = new_state
        self.log_signal.emit(f"Состояние изменилось на {self.state.__class__.__name__}", 'debug')

    def call(self):
        self.state.call(self)

    def connect(self):
        self.state = NewRequestState()
        start_time = time()
        connection_timeout = float(self.client_settings['connection_timeout'])
        
        while time() - start_time < connection_timeout:
            try:
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=self.client_settings['broker_url'])
                )
                self.channel = self.connection.channel()

                self.channel.exchange_declare(self.client_settings['exchange_name'], 'direct', durable=True)
                self.channel.queue_declare(self.client_settings['queue_name'], durable=True)

                result = self.channel.queue_declare(queue='', exclusive=True)
                self.callback_queue = result.method.queue

                self.channel.basic_consume(
                    queue=self.callback_queue,
                    on_message_callback=self.on_response,
                    auto_ack=True
                )
                self.log_signal.emit("Подключение установлено успешно.", 'info')
                
                if self.reconnecting:
                    self.reconnecting = False
                
                return
            
            except pika.exceptions.AMQPConnectionError as e:
                self.log_signal.emit("Попытка подключения...", 'warning')
                sleep(5)
        
        self.log_signal.emit(f"Не удалось подключиться за {connection_timeout} секунд.", 'error')

    def on_response(self, ch, method, props, body):
        if props.correlation_id == self.corr_id: 
            self.response = Response()
            self.response.ParseFromString(body)
            self.log_signal.emit(f"Получен ответ для request_id '{self.response.request_id}' со значением {self.response.response}", 'info')
            self.response_received.emit(str(self.response.response))
        else:
            self.log_signal.emit(f"Получен ответ с неподходящим correlation_id {props.correlation_id}. Игнорирование.", 'warning')

    def send_request(self, value, timeout):
        self.value = value
        self.timeout = timeout
        self.start()

    def run(self):
        if self.reconnecting:
            self.connect()
            return
        
        if not hasattr(self, 'connection') or self.connection.is_closed:
            self.connect()

        self.check_connection()

        self.response = None
        self.cancelled = False
        self.request_id = str(uuid4())

        request = Request(
            return_address=self.client_settings['client_uuid'],
            request_id=str(self.request_id),
            proccess_time_in_seconds=self.timeout,
            request=self.value
        )

        self.corr_id = str(uuid4())

        try:
            self.channel.basic_publish(
                exchange=self.client_settings['exchange_name'],
                routing_key=self.client_settings['queue_name'],
                properties=pika.BasicProperties(
                    reply_to=self.callback_queue,
                    correlation_id=self.corr_id
                ),
                body=request.SerializeToString())
            self.call()
            self.log_signal.emit(f"Отправлен запрос для request_id '{request.request_id}' со значением {request.request}, задержка {self.timeout} сек", 'info')
            self.call()
            
        except Exception as e:
            self.log_signal.emit(f"Ошибка при отправке запроса request_id {request.request_id}: {str(e)}", 'error')
            return
        
        wait_interval = 0.1
        elapsed_time = 0
        while self.response is None and elapsed_time <= self.timeout:
            if self.cancelled:
                self.log_signal.emit(f"Запрос request_id '{request.request_id}' отменён", 'info')
                return
            self.connection.process_data_events(time_limit=wait_interval)
            elapsed_time += wait_interval

        if self.response is None:
            self.log_signal.emit(f"Ответ для request_id '{request.request_id}' не получен в течении {self.timeout} сек.", 'warning')
            self.responce_not_recieved.emit()

    def cancel_request(self):
        self.cancelled = True

    def update_settings(self, new_settings):
        self.client_settings = new_settings
        self.reconnecting = True
        self.connect()

    def check_connection(self):
        try:
            self.connection.process_data_events(time_limit=0.1)
        except pika.exceptions.StreamLostError:
            print("Потеря соединения с сервером RabbitMQ. Переподключение...")
            self.connect()
        except pika.exceptions.ConnectionClosed:
            print("Соединение закрыто сервером RabbitMQ.")
            self.connect()
        except Exception as e:
            print(f"Ошибка: {e}")