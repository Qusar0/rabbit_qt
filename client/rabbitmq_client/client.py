from PyQt5.QtCore import QThread, pyqtSignal
import pika
from uuid import uuid4
from protobuf.message_pb2 import Response, Request


class Client(QThread):
    response_received = pyqtSignal(str)
    log_signal = pyqtSignal(str)

    def __init__(self, client_settings):
        super().__init__()

        self.client_settings = client_settings
        
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.client_settings['broker_url']))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.request_id = None
        self.response = None
        self.cancelled = False

    def on_response(self, ch, method, props, body):
        print(props.correlation_id)
        if props.correlation_id == self.corr_id: 
            self.response = Response()
            self.response.ParseFromString(body)
            self.log_signal.emit(f"Получен ответ для request_id '{self.response.request_id}' со значением {self.response.response}")
            self.response_received.emit(str(self.response.response))
        else:
            self.log_signal.emit(f"Получен ответ с неподходящим correlation_id {props.correlation_id}. Игнорирование.")

    def call(self, value, timeout):
        self.value = value
        self.timeout = timeout
        self.start()

    def run(self):
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

        self.channel.basic_publish(
            exchange=self.client_settings['exchange_name'],
            routing_key=self.client_settings['queue_name'],
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id
            ),
            body=request.SerializeToString())
        
        self.log_signal.emit(f"Отправлен запрос для request_id '{request.request_id}' со значением {request.request}, задержка {self.timeout} сек")
        
        wait_interval = 0.1
        elapsed_time = 0
        
        while self.response is None and elapsed_time <= self.timeout:
            if self.cancelled:
                self.log_signal.emit(f"Запрос request_id '{request.request_id}' отменён")
                return

            self.connection.process_data_events(time_limit=wait_interval)
            elapsed_time += wait_interval

        if self.response is None:
            self.log_signal.emit(f"Ответ для request_id '{request.request_id}' не получен в течении {self.timeout} сек.")

    def cancel_request(self):
        self.cancelled = True
