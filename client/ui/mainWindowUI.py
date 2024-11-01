# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(812, 651)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.requestGroupBox = QGroupBox(self.centralwidget)
        self.requestGroupBox.setObjectName(u"requestGroupBox")
        self.requestGroupBox.setGeometry(QRect(10, 20, 781, 181))
        font = QFont()
        font.setPointSize(14)
        self.requestGroupBox.setFont(font)
        self.requestGroupBox.setAutoFillBackground(True)
        self.requestSpinBox = QSpinBox(self.requestGroupBox)
        self.requestSpinBox.setObjectName(u"requestSpinBox")
        self.requestSpinBox.setGeometry(QRect(320, 50, 131, 26))
        self.requestSpinBox.setFont(font)
        self.timeoutDoubleSpinBox = QDoubleSpinBox(self.requestGroupBox)
        self.timeoutDoubleSpinBox.setObjectName(u"timeoutDoubleSpinBox")
        self.timeoutDoubleSpinBox.setEnabled(False)
        self.timeoutDoubleSpinBox.setGeometry(QRect(320, 100, 131, 26))
        self.timeoutDoubleSpinBox.setFont(font)
        self.label = QLabel(self.requestGroupBox)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(230, 50, 59, 22))
        self.label.setFont(font)
        self.label_2 = QLabel(self.requestGroupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 100, 281, 22))
        self.label_2.setFont(font)
        self.timeoutCheckBox = QCheckBox(self.requestGroupBox)
        self.timeoutCheckBox.setObjectName(u"timeoutCheckBox")
        self.timeoutCheckBox.setGeometry(QRect(470, 100, 171, 28))
        self.timeoutCheckBox.setFont(font)
        self.sendRequesPushButton = QPushButton(self.requestGroupBox)
        self.sendRequesPushButton.setObjectName(u"sendRequesPushButton")
        self.sendRequesPushButton.setGeometry(QRect(620, 140, 141, 30))
        self.sendRequesPushButton.setFont(font)
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 210, 781, 381))
        self.groupBox_2.setFont(font)
        self.groupBox_2.setAutoFillBackground(True)
        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(70, 50, 111, 22))
        self.label_3.setFont(font)
        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(40, 80, 151, 22))
        self.label_4.setFont(font)
        self.stateRequestLabel = QLabel(self.groupBox_2)
        self.stateRequestLabel.setObjectName(u"stateRequestLabel")
        self.stateRequestLabel.setGeometry(QRect(292, 50, 300, 22))
        self.stateRequestLabel.setFont(font)
        self.requestResultLabel = QLabel(self.groupBox_2)
        self.requestResultLabel.setObjectName(u"requestResultLabel")
        self.requestResultLabel.setGeometry(QRect(292, 80, 141, 22))
        self.requestResultLabel.setFont(font)
        self.cancelRequestPushButton = QPushButton(self.groupBox_2)
        self.cancelRequestPushButton.setObjectName(u"cancelRequestPushButton")
        self.cancelRequestPushButton.setGeometry(QRect(620, 50, 141, 30))
        self.cancelRequestPushButton.setFont(font)
        self.logsPlainTextEdit = QPlainTextEdit(self.groupBox_2)
        self.logsPlainTextEdit.setObjectName(u"logsPlainTextEdit")
        self.logsPlainTextEdit.setGeometry(QRect(30, 140, 721, 171))
        self.logsPlainTextEdit.setFont(font)
        self.logsPlainTextEdit.setReadOnly(True)
        self.settingsPushButton = QPushButton(self.groupBox_2)
        self.settingsPushButton.setObjectName(u"settingsPushButton")
        self.settingsPushButton.setGeometry(QRect(30, 330, 721, 31))
        self.settingsPushButton.setFont(font)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 812, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u041a\u043b\u0438\u0435\u043d\u0442", None))
        self.requestGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043f\u0440\u043e\u0441", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u0427\u0438\u0441\u043b\u043e:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0440\u0435\u043c\u044f \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0438 \u0437\u0430\u043f\u0440\u043e\u0441\u0430, \u0441\u0435\u043a:", None))
        self.timeoutCheckBox.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0434\u0435\u0439\u0441\u0442\u0432\u043e\u0432\u0430\u0442\u044c", None))
        self.sendRequesPushButton.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u044c", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u0435 \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0438 \u0437\u0430\u043f\u0440\u043e\u0441\u0430 ", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u0435:", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u0432\u0435\u0442 \u0441\u0435\u0440\u0432\u0435\u0440\u0430:", None))
        self.stateRequestLabel.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0435\u043e\u043f\u0440\u0435\u0434\u0435\u043b\u0435\u043d\u043e", None))
        self.requestResultLabel.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0435\u043e\u043f\u0440\u0435\u0434\u0435\u043b\u0435\u043d\u043e", None))
        self.cancelRequestPushButton.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
        self.settingsPushButton.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
    # retranslateUi

