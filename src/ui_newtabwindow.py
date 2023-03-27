# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'newtab.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_NewtabWindow(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(222, 119)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelSubcomp = QLabel(Form)
        self.labelSubcomp.setObjectName(u"labelSubcomp")
        font = QFont()
        font.setPointSize(10)
        self.labelSubcomp.setFont(font)
        self.labelSubcomp.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.labelSubcomp, 0, 0, 1, 2)

        self.comboSubcomp = QComboBox(Form)
        self.comboSubcomp.setObjectName(u"comboSubcomp")

        self.gridLayout.addWidget(self.comboSubcomp, 0, 2, 1, 1)

        self.labelTabName = QLabel(Form)
        self.labelTabName.setObjectName(u"labelTabName")
        self.labelTabName.setFont(font)
        self.labelTabName.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.labelTabName, 1, 0, 1, 1)

        self.lineTabName = QLineEdit(Form)
        self.lineTabName.setObjectName(u"lineTabName")

        self.gridLayout.addWidget(self.lineTabName, 1, 2, 1, 1)

        self.pushOk = QPushButton(Form)
        self.pushOk.setObjectName(u"pushOk")

        self.gridLayout.addWidget(self.pushOk, 2, 0, 1, 2)

        self.pushCancel = QPushButton(Form)
        self.pushCancel.setObjectName(u"pushCancel")

        self.gridLayout.addWidget(self.pushCancel, 2, 2, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.labelSubcomp.setText(QCoreApplication.translate("Form", u"Subcomponent", None))
        self.labelTabName.setText(QCoreApplication.translate("Form", u"Tab name", None))
        self.pushOk.setText(QCoreApplication.translate("Form", u"Ok", None))
        self.pushCancel.setText(QCoreApplication.translate("Form", u"Cancel", None))
    # retranslateUi

