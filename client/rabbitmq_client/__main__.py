from protobuf.message_pb2 import Response, Request
import pika
import uuid
from PyQt5.QtCore import pyqtSignal, QThread, QTimer, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QPlainTextEdit, QDialog, QVBoxLayout
import sys
from mainUI import Ui_MainWindow
import logging

class LogHandler(logging.Handler, QObject):
    log_signal = pyqtSignal(str)

    def __init__(self, log_widget):
        QObject.__init__(self)
        logging.Handler.__init__(self)
        self.log_widget = log_widget
        self.log_signal.connect(self.update_log)

    def update_log(self, log_entry):
        self.log_widget.appendPlainText(log_entry)

    def emit(self, record):
        log_entry = self.format(record)
        self.log_widget.appendPlainText(log_entry)


class LogWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Logs")
        self.setGeometry(100, 100, 600, 400)

        self.log_widget = QPlainTextEdit(self)
        self.log_widget.setReadOnly(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.log_widget)
        self.setLayout(layout)

class Client(QThread):
    response_received = pyqtSignal(str)

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
        self.corr_id = None
        self.timeout = 0
        self.request = 0

    def on_response(self, ch, method, props, body):
        self.response = Response()
        self.response.ParseFromString(body)
        # logging.info(f"Получен ответ для request_id '{self.response.request_id}' со значением {self.response.response}")
        self.response_received.emit(str(self.response.response))

    def call(self, request, timeout):
        print(self.timeout, self.request)
        self.timeout = timeout
        self.request = request
        self.start()
    
    def run(self):
        request = Request(
            return_address=self.callback_queue,
            request_id=str(self.request_id),
            proccess_time_in_seconds=self.timeout,
            request=self.request
        )

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='double',
            routing_key='server_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=request.SerializeToString())
        
        self.request_id += 1
        
        logging.info(f"Отправлен запрос для request_id '{request.request_id}' со значением {request.request}")

        while self.response is None:
            self.connection.process_data_events(time_limit=None)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.client = Client()
        self.client.response_received.connect(self.show_response)

        self.init_logging()

        send_request_btn = self.ui.sendRequesPushButton
        send_request_btn.clicked.connect(self.send_request)

        self.ui.timeoutCheckBox.clicked.connect(self.is_enabled)

        self.ui.rquestProgressBar.setVisible(False)

        self.progress_timer = QTimer(self)
        self.progress_timer.timeout.connect(self.update_progress_bar)
        self.time_elapsed = 0
        self.timeout = 0

    def init_logging(self):
        log_handler = LogHandler(self.ui.logsPlainTextEdit)
        log_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s - %(asctime)s'))

        logger = logging.getLogger()
        logger.addHandler(log_handler)
        logger.setLevel(logging.INFO)

    def show_logs(self):
        self.log_window.show()

    def send_request(self):
        try:
            request = self.ui.requestSpinBox.value()
            timeout = self.ui.timeoutDoubleSpinBox.value()
            if  timeout > 0:
                self.timeout = int(timeout)
                self.ui.rquestProgressBar.setValue(0)

                self.time_elapsed = 0
                self.progress_timer.start(100)
                self.ui.rquestProgressBar.setVisible(True)


            self.client.call(request, self.timeout)
        except ValueError:
            self.show_error_message()
            
    def show_error_message(self):
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Ошибка")
            msg_box.setText("Введён неверный формат данных")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()

    def update_progress_bar(self):
        self.time_elapsed += 0.1
        progress = int((self.time_elapsed / self.timeout) * 100)
        self.ui.rquestProgressBar.setValue(progress)

        if self.time_elapsed >= self.timeout:
            self.progress_timer.stop()

    def show_response(self, response):
        self.ui.requestResultLabel.setText(response)
        print(response)
        self.ui.cancelRequestPushButton.setVisible(False)

    def is_enabled(self):
        flag = self.ui.timeoutCheckBox.isChecked()
        self.ui.timeoutDoubleSpinBox.setEnabled(flag)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()