# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'properties.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(455, 290)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(60, 231, 341, 32))
        font = QFont()
        font.setPointSize(14)
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.brokerAddresTextEdit = QTextEdit(Dialog)
        self.brokerAddresTextEdit.setObjectName(u"brokerAddresTextEdit")
        self.brokerAddresTextEdit.setGeometry(QRect(230, 30, 201, 21))
        self.brokerAddresTextEdit.setFont(font)
        self.brokerAddresTextEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.brokerAddresTextEdit.setAcceptRichText(True)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(21, 22, 201, 31))
        self.label.setFont(font)
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(93, 66, 131, 21))
        self.label_2.setFont(font)
        self.exchangeNameTextEdit = QTextEdit(Dialog)
        self.exchangeNameTextEdit.setObjectName(u"exchangeNameTextEdit")
        self.exchangeNameTextEdit.setGeometry(QRect(230, 70, 201, 21))
        self.exchangeNameTextEdit.setFont(font)
        self.exchangeNameTextEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.clientUuidTextEdit = QTextEdit(Dialog)
        self.clientUuidTextEdit.setObjectName(u"clientUuidTextEdit")
        self.clientUuidTextEdit.setGeometry(QRect(230, 141, 201, 21))
        self.clientUuidTextEdit.setFont(font)
        self.clientUuidTextEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(95, 139, 131, 17))
        self.label_3.setFont(font)
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(18, 182, 211, 21))
        self.label_4.setFont(font)
        self.connectionTimeoutDoubleSpinBox = QDoubleSpinBox(Dialog)
        self.connectionTimeoutDoubleSpinBox.setObjectName(u"connectionTimeoutDoubleSpinBox")
        self.connectionTimeoutDoubleSpinBox.setGeometry(QRect(230, 181, 201, 26))
        self.connectionTimeoutDoubleSpinBox.setFont(font)
        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(120, 101, 101, 21))
        self.label_5.setFont(font)
        self.queueNameTextEdit = QTextEdit(Dialog)
        self.queueNameTextEdit.setObjectName(u"queueNameTextEdit")
        self.queueNameTextEdit.setGeometry(QRect(230, 105, 201, 21))
        self.queueNameTextEdit.setFont(font)
        self.queueNameTextEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u043a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u0410\u0434\u0440\u0435\u0441 \u0438 \u043f\u043e\u0440\u0442 \u0431\u0440\u043e\u043a\u0435\u0440\u0430", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"\u0418\u043c\u044f exchange", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"UUID \u043a\u043b\u0438\u0435\u043d\u0442\u0430", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"\u0422\u0430\u0439\u043c\u0430\u0443\u0442 \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u044f", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"\u0418\u043c\u044f queue", None))
    # retranslateUi

