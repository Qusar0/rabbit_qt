from PyQt5.QtCore import QThread, pyqtSignal
import pika
import uuid
from protobuf.message_pb2 import Response, Request


class Client(QThread):
    response_received = pyqtSignal(str)
    log_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.request_id = 1
        self.response = None
        self.cancelled = False

    def on_response(self, ch, method, props, body):
        print(props)
        if props.correlation_id == self.corr_id: 
            self.response = Response()
            self.response.ParseFromString(body)
            if int(self.response.request_id) == self.request_id:
                self.log_signal.emit(f"Получен ответ для request_id '{self.response.request_id}' со значением {self.response.response}")
                self.response_received.emit(str(self.response.response))
            else:
                self.log_signal.emit(f"Получен ответ для прошлого request_id '{self.response.request_id}'. Игнорирование.")
        else:
            self.log_signal.emit(f"Получен ответ с неподходящим correlation_id. Игнорирование.")

    def call(self, value, timeout):
        self.value = value
        self.timeout = timeout
        self.start()

    def run(self):
        self.response = None
        self.cancelled = False

        request = Request(
            return_address=self.callback_queue,
            request_id=str(self.request_id),
            proccess_time_in_seconds=self.timeout,
            request=self.value
        )

        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(
            exchange='double',
            routing_key='server_queue',
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
                self.request_id += 1
                return

            self.connection.process_data_events(time_limit=wait_interval)
            elapsed_time += wait_interval

        if self.response is None:
            self.log_signal.emit(f"Ответ для request_id '{request.request_id}' не получен в течении {self.timeout} сек.")

        self.request_id += 1
            
    def cancel_request(self):
        self.cancelled = True
