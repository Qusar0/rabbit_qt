from PyQt5.QtWidgets import QApplication
import sys
from ui.main_window import MainWindow
import configparser


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('../configs/client_config.ini')
    client_settings = config['Client']

    app = QApplication(sys.argv)
    window = MainWindow(client_settings)
    window.show()

    app.exec()