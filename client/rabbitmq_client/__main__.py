from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
from mainUI import Ui_MainWindow
from client import Client
from logger import LogHandler
import logging

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.log_handler = LogHandler(self.ui.logsPlainTextEdit)
        self.init_logs_settings()

        self.client = Client()
        self.client.response_received.connect(self.show_response)
        self.client.log_signal.connect(self.log_message)

        send_request_btn = self.ui.sendRequesPushButton
        send_request_btn.clicked.connect(self.send_request)

        self.ui.timeoutCheckBox.clicked.connect(self.is_enabled)

    def log_message(self, message):
        self.logger.info(message)

    def init_logs_settings(self):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(self.log_handler)
        self.logger.setLevel(logging.INFO)

    def send_request(self):
        request = self.ui.requestSpinBox.value()
        timeout = self.ui.timeoutDoubleSpinBox.value()
        self.logger.info(f"Отправлен запрос для request_id '{request}' со значением {request}, задержка {timeout} сек")
        self.client.call(request, timeout)
            

    def show_response(self, response):
        self.ui.requestResultLabel.setText(response)
        self.ui.cancelRequestPushButton.setVisible(False)

    def is_enabled(self):
        flag = self.ui.timeoutCheckBox.isChecked()
        self.ui.timeoutDoubleSpinBox.setEnabled(flag)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()