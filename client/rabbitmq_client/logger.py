import logging
from PyQt5.QtCore import QObject, pyqtSignal


class LogHandler(logging.Handler, QObject):
    appendPlainText = pyqtSignal(str)

    def __init__(self, log_widget):
        super(LogHandler, self).__init__()
        QObject.__init__(self)
        self.log_widget = log_widget
        self.log_widget.setReadOnly(True)
        self.appendPlainText.connect(self.log_widget.appendPlainText)

    def emit(self, record):
        log_entry = self.format(record)
        self.log_widget.appendPlainText(log_entry)