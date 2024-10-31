from PyQt5.QtWidgets import QMainWindow, QDialog
from UI.mainUI import Ui_MainWindow
from properties_dialog import PropertiesDialog
from client import Client
from log_configs.logger import setup_logger
from configparser import SectionProxy


class MainWindow(QMainWindow):
    def __init__(self, client_settings: SectionProxy) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.client_settings = client_settings
        self.is_properties_edditable = True
        
        self.logger = setup_logger(self.ui.logsPlainTextEdit)

        self.client = Client(self.client_settings)
        self.client.response_received.connect(self.show_response)
        self.client.responce_not_recieved.connect(self.change_buttons)
        self.client.log_signal.connect(self.log_message)

        self.ui.sendRequesPushButton.clicked.connect(self.send_request)
        self.ui.cancelRequestPushButton.clicked.connect(self.cancel_request)
        self.ui.timeoutCheckBox.clicked.connect(self.is_enabled)
        self.ui.settingsPushButton.clicked.connect(self.open_properties_dialog)

    def show_response(self, response: int) -> None:
        self.ui.requestResultLabel.setText(response)
        self.set_buttons_enabled(True, False)
        self.is_properties_edditable = True

    def change_buttons(self) -> None:
        self.set_buttons_enabled(True, False)
        self.is_properties_edditable = True

    def log_message(self, message: str, log_level: str) -> None:
        if log_level == 'debug':
            self.logger.debug(message)
        if log_level == 'info':
            self.logger.info(message)
        if log_level == 'warning':
            self.logger.warning(message)
        if log_level == 'error':
            self.logger.error(message)

    def send_request(self) -> None:
        request = self.ui.requestSpinBox.value()
        timeout = 0
        if self.ui.timeoutCheckBox.isChecked():
            timeout = self.ui.timeoutDoubleSpinBox.value()
            
        self.set_buttons_enabled(False, True)
        self.client.call(request, timeout)
        self.is_properties_edditable = False

    def cancel_request(self) -> None:
        self.client.cancel_request()
        self.set_buttons_enabled(True, False)
        self.is_properties_edditable = True

    def is_enabled(self) -> None:
        flag = self.ui.timeoutCheckBox.isChecked()
        self.ui.timeoutDoubleSpinBox.setEnabled(flag)

    def open_properties_dialog(self) -> None:
        dialog = PropertiesDialog(self.client_settings)
        dialog.set_editable(self.is_properties_edditable)
        if dialog.exec_() == QDialog.Accepted:
            self.client_settings = dialog.get_client_settings()
            self.client.update_settings(self.client_settings)

    def set_buttons_enabled(self, send_enabled: bool, cancel_enabled: bool) -> None:
        self.ui.sendRequesPushButton.setEnabled(send_enabled)
        self.ui.cancelRequestPushButton.setEnabled(cancel_enabled)
