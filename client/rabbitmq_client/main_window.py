from PyQt5.QtWidgets import QMainWindow
from mainUI import Ui_MainWindow
from properties_dialog import PropertiesDialog
from client import Client
from logger import LogHandler
import logging

class MainWindow(QMainWindow):
    def __init__(self, client_settings) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.log_handler = LogHandler(self.ui.logsPlainTextEdit)
        self.init_logs_settings()

        self.client = Client(client_settings)
        self.client.response_received.connect(self.show_response)
        self.client.log_signal.connect(self.log_message)

        self.ui.sendRequesPushButton.clicked.connect(self.send_request)
        self.ui.cancelRequestPushButton.clicked.connect(self.cancel_request)
        self.ui.timeoutCheckBox.clicked.connect(self.is_enabled)
        self.ui.settingsPushButton.clicked.connect(self.open_properties_dialog)

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

    def open_properties_dialog(self) -> None:
        dialog = PropertiesDialog()
        dialog.open_properties_dialog()
        