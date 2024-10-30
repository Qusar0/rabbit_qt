import logging
from PyQt5.QtCore import QObject, pyqtSignal

class QtLogHandler(logging.Handler, QObject):
    appendPlainText = pyqtSignal(str)

    def __init__(self, log_widget):
        super(QtLogHandler, self).__init__()
        QObject.__init__(self)
        self.log_widget = log_widget
        self.log_widget.setReadOnly(True)
        self.appendPlainText.connect(self.log_widget.appendPlainText)

    def emit(self, record):
        log_entry = self.format(record)
        self.log_widget.appendPlainText(log_entry)


class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',
        'INFO': '\033[92m',
        'WARNING': '\033[93m',
        'ERROR': '\033[91m',
        'CRITICAL': '\033[1;101m'
    }

    def format(self, record):
        formatter = logging.Formatter(f"{self.COLORS.get(record.levelname, '')}%(levelname)s %(asctime)s %(message)s")
        return formatter.format(record)


def setup_logger(log_widget):
    logger = logging.getLogger('colored_logger')
    logger.setLevel(logging.INFO)

    log_handler = QtLogHandler(log_widget)
    formatter = logging.Formatter("%(levelname)s %(asctime)s %(message)s")
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(ColoredFormatter())
    logger.addHandler(console_handler)

    return logger
