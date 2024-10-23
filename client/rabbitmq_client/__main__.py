from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
from mainUI import Ui_MainWindow
from client import Client
from logger import LogHandler
import logging

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.log_handler = LogHandler(self.ui.logsPlainTextEdit)
        self.init_logs_settings()

        self.client = Client()
        self.client.response_received.connect(self.show_response)
        self.client.log_signal.connect(self.log_message)

        self.ui.sendRequesPushButton.clicked.connect(self.send_request)
        self.ui.cancelRequestPushButton.clicked.connect(self.cancel_request)
        self.ui.timeoutCheckBox.clicked.connect(self.is_enabled)

    def init_logs_settings(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(self.log_handler)
        self.logger.setLevel(logging.INFO)

    def show_response(self, response: int) -> None:
        self.ui.sendRequesPushButton.setEnabled(True)
        self.ui.cancelRequestPushButton.setEnabled(False)

        self.ui.requestResultLabel.setText(response)

    def log_message(self, message: str) -> None:
        self.logger.info(message)

    def send_request(self) -> None:
        request = self.ui.requestSpinBox.value()
        timeout = 0
        if self.ui.timeoutCheckBox.isChecked():
            timeout = self.ui.timeoutDoubleSpinBox.value()
            
        self.ui.sendRequesPushButton.setEnabled(False)
        self.ui.cancelRequestPushButton.setEnabled(True)
        self.client.call(request, timeout)

    def cancel_request(self):
        self.client.cancel_request()
        self.ui.sendRequesPushButton.setEnabled(True)
        self.ui.cancelRequestPushButton.setEnabled(False)

    def is_enabled(self) -> None:
        flag = self.ui.timeoutCheckBox.isChecked()
        self.ui.timeoutDoubleSpinBox.setEnabled(flag)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()