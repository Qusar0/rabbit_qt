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

    def on_response(self, ch, method, props, body):
        self.response = Response()
        self.response.ParseFromString(body)
        self.log_signal.emit(f"Получен ответ для request_id '{self.response.request_id}' со значением {self.response.response}")
        self.response_received.emit(str(self.response.response))

    def call(self, value, timeout):
        request = Request(
            return_address=self.callback_queue,
            request_id=str(self.request_id),
            proccess_time_in_seconds=timeout,
            request=value
        )
        self.response = None

        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='double',
            routing_key='server_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
            ),
            body=request.SerializeToString())
        
        

        self.request_id += 1
        while self.response is None:
            self.connection.process_data_events(time_limit=timeout)
    

