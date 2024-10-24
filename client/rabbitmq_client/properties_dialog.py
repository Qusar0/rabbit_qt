from PyQt5.QtWidgets import QDialog
from dialogPropertiesUI import Ui_Dialog

class PropertiesDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()  
        self.ui.setupUi(self)

    def open_properties_dialog(self) -> None:
        dialog = PropertiesDialog()
        dialog.exec_()

