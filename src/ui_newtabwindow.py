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
    def setupUi(self, Newtab):
        if not Newtab.objectName():
            Newtab.setObjectName(u"Newtab")
        Newtab.setWindowModality(Qt.ApplicationModal)
        Newtab.resize(216, 123)
        self.gridLayout = QGridLayout(Newtab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushCancel = QPushButton(Newtab)
        self.pushCancel.setObjectName(u"pushCancel")

        self.gridLayout.addWidget(self.pushCancel, 3, 3, 1, 1)

        self.labelTabName = QLabel(Newtab)
        self.labelTabName.setObjectName(u"labelTabName")
        font = QFont()
        font.setPointSize(10)
        self.labelTabName.setFont(font)
        self.labelTabName.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.labelTabName, 2, 0, 1, 2)

        self.labelPreset = QLabel(Newtab)
        self.labelPreset.setObjectName(u"labelPreset")
        self.labelPreset.setFont(font)
        self.labelPreset.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.labelPreset, 0, 0, 1, 2)

        self.pushOk = QPushButton(Newtab)
        self.pushOk.setObjectName(u"pushOk")

        self.gridLayout.addWidget(self.pushOk, 3, 2, 1, 1)

        self.lineTabName = QLineEdit(Newtab)
        self.lineTabName.setObjectName(u"lineTabName")

        self.gridLayout.addWidget(self.lineTabName, 2, 2, 1, 2)

        self.comboPreset = QComboBox(Newtab)
        self.comboPreset.setObjectName(u"comboPreset")

        self.gridLayout.addWidget(self.comboPreset, 0, 2, 1, 2)

        self.comboParent = QComboBox(Newtab)
        self.comboParent.setObjectName(u"comboParent")

        self.gridLayout.addWidget(self.comboParent, 1, 2, 1, 2)

        self.labelParent = QLabel(Newtab)
        self.labelParent.setObjectName(u"labelParent")
        self.labelParent.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.labelParent, 1, 0, 1, 2)


        self.retranslateUi(Newtab)

        QMetaObject.connectSlotsByName(Newtab)
    # setupUi

    def retranslateUi(self, Newtab):
        Newtab.setWindowTitle(QCoreApplication.translate("Newtab", u"Form", None))
        self.pushCancel.setText(QCoreApplication.translate("Newtab", u"Cancel", None))
        self.labelTabName.setText(QCoreApplication.translate("Newtab", u"Name", None))
        self.labelPreset.setText(QCoreApplication.translate("Newtab", u"Preset", None))
        self.pushOk.setText(QCoreApplication.translate("Newtab", u"Ok", None))
        self.labelParent.setText(QCoreApplication.translate("Newtab", u"Parent", None))
    # retranslateUi

