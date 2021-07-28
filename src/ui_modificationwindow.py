# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'modification.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_ModificationWindow(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(393, 98)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(393, 98))
        Form.setMaximumSize(QSize(393, 98))
        self.pushOk = QPushButton(Form)
        self.pushOk.setObjectName(u"pushOk")
        self.pushOk.setGeometry(QRect(90, 70, 80, 23))
        self.lineName = QLineEdit(Form)
        self.lineName.setObjectName(u"lineName")
        self.lineName.setGeometry(QRect(50, 10, 330, 23))
        self.labelName = QLabel(Form)
        self.labelName.setObjectName(u"labelName")
        self.labelName.setGeometry(QRect(10, 10, 44, 16))
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.labelName.sizePolicy().hasHeightForWidth())
        self.labelName.setSizePolicy(sizePolicy1)
        self.pushCancel = QPushButton(Form)
        self.pushCancel.setObjectName(u"pushCancel")
        self.pushCancel.setGeometry(QRect(230, 70, 80, 23))
        self.labelValue = QLabel(Form)
        self.labelValue.setObjectName(u"labelValue")
        self.labelValue.setGeometry(QRect(10, 40, 42, 16))
        sizePolicy1.setHeightForWidth(self.labelValue.sizePolicy().hasHeightForWidth())
        self.labelValue.setSizePolicy(sizePolicy1)
        self.lineValue = QLineEdit(Form)
        self.lineValue.setObjectName(u"lineValue")
        self.lineValue.setGeometry(QRect(50, 40, 330, 23))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Parameter Modification", None))
        self.pushOk.setText(QCoreApplication.translate("Form", u"Ok", None))
        self.labelName.setText(QCoreApplication.translate("Form", u"Name: ", None))
        self.pushCancel.setText(QCoreApplication.translate("Form", u"Cancel", None))
        self.labelValue.setText(QCoreApplication.translate("Form", u"Value: ", None))
    # retranslateUi

