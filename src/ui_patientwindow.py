# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'patient.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_PatientWindow(object):
    def setupUi(self, Patient):
        if not Patient.objectName():
            Patient.setObjectName(u"Patient")
        Patient.resize(600, 600)
        icon = QIcon()
        icon.addFile(u"../icons/ncc.png", QSize(), QIcon.Normal, QIcon.Off)
        Patient.setWindowIcon(icon)
        self.gridLayout_2 = QGridLayout(Patient)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.comboFiles = QComboBox(Patient)
        self.comboFiles.setObjectName(u"comboFiles")

        self.gridLayout_2.addWidget(self.comboFiles, 2, 0, 1, 3)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")

        self.gridLayout_2.addLayout(self.gridLayout, 3, 0, 1, 3)

        self.pushPrev = QPushButton(Patient)
        self.pushPrev.setObjectName(u"pushPrev")

        self.gridLayout_2.addWidget(self.pushPrev, 5, 0, 1, 1)

        self.pushClose = QPushButton(Patient)
        self.pushClose.setObjectName(u"pushClose")

        self.gridLayout_2.addWidget(self.pushClose, 5, 2, 1, 1)

        self.pushOpen = QPushButton(Patient)
        self.pushOpen.setObjectName(u"pushOpen")

        self.gridLayout_2.addWidget(self.pushOpen, 0, 2, 1, 1)

        self.pushNext = QPushButton(Patient)
        self.pushNext.setObjectName(u"pushNext")

        self.gridLayout_2.addWidget(self.pushNext, 5, 1, 1, 1)

        self.labelDir = QLabel(Patient)
        self.labelDir.setObjectName(u"labelDir")

        self.gridLayout_2.addWidget(self.labelDir, 0, 0, 1, 1)

        self.lineDir = QLineEdit(Patient)
        self.lineDir.setObjectName(u"lineDir")
        self.lineDir.setReadOnly(True)

        self.gridLayout_2.addWidget(self.lineDir, 0, 1, 1, 1)


        self.retranslateUi(Patient)

        QMetaObject.connectSlotsByName(Patient)
    # setupUi

    def retranslateUi(self, Patient):
        Patient.setWindowTitle(QCoreApplication.translate("Patient", u"Patient", None))
        self.pushPrev.setText(QCoreApplication.translate("Patient", u"< Prev", None))
        self.pushClose.setText(QCoreApplication.translate("Patient", u"Close", None))
        self.pushOpen.setText(QCoreApplication.translate("Patient", u"Open", None))
        self.pushNext.setText(QCoreApplication.translate("Patient", u"Next >", None))
        self.labelDir.setText(QCoreApplication.translate("Patient", u"Directory", None))
    # retranslateUi

