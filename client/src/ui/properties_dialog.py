from PyQt5.QtWidgets import QDialog
from ui.propertiesUI import Ui_Dialog

class PropertiesDialog(QDialog):
    def __init__(self, client_settings):
        super().__init__()
        self.ui = Ui_Dialog()  
        self.ui.setupUi(self)
        
        self.client_settings = client_settings
        
        self.load_client_settings()

    def load_client_settings(self):
        self.ui.brokerAddresTextEdit.setPlainText(self.client_settings.get('broker_url', ''))
        self.ui.exchangeNameTextEdit.setPlainText(self.client_settings.get('exchange_name', ''))
        self.ui.queueNameTextEdit.setPlainText(self.client_settings.get('queue_name', ''))
        self.ui.clientUuidTextEdit.setPlainText(self.client_settings.get('client_uuid', ''))
        self.ui.connectionTimeoutDoubleSpinBox.setValue(float(self.client_settings.get('connection_timeout', 0.0)))

    def get_client_settings(self):
        return {
            'broker_url': self.ui.brokerAddresTextEdit.toPlainText(),
            'exchange_name': self.ui.exchangeNameTextEdit.toPlainText(),
            'queue_name': self.ui.queueNameTextEdit.toPlainText(),
            'client_uuid': self.ui.clientUuidTextEdit.toPlainText(),
            'connection_timeout': self.ui.connectionTimeoutDoubleSpinBox.value()
        }
    
    def set_editable(self, is_editable: bool):
        self.ui.brokerAddresTextEdit.setReadOnly(not is_editable)
        self.ui.exchangeNameTextEdit.setReadOnly(not is_editable)
        self.ui.queueNameTextEdit.setReadOnly(not is_editable)
        self.ui.clientUuidTextEdit.setReadOnly(not is_editable)
        self.ui.connectionTimeoutDoubleSpinBox.setReadOnly(not is_editable)
        self.ui.buttonBox.setDisabled(not is_editable)