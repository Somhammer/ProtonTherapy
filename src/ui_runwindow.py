# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'run.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_RunWindow(object):
    def setupUi(self, Run):
        if not Run.objectName():
            Run.setObjectName(u"Run")
        Run.resize(483, 343)
        icon = QIcon()
        icon.addFile(u"../icons/ncc.png", QSize(), QIcon.Normal, QIcon.Off)
        Run.setWindowIcon(icon)
        self.gridLayout = QGridLayout(Run)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushOk = QPushButton(Run)
        self.pushOk.setObjectName(u"pushOk")

        self.gridLayout.addWidget(self.pushOk, 1, 1, 1, 1)

        self.textLog = QTextBrowser(Run)
        self.textLog.setObjectName(u"textLog")
        font = QFont()
        font.setPointSize(11)
        self.textLog.setFont(font)

        self.gridLayout.addWidget(self.textLog, 0, 0, 1, 2)

        self.progressBar = QProgressBar(Run)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.gridLayout.addWidget(self.progressBar, 1, 0, 1, 1)


        self.retranslateUi(Run)

        QMetaObject.connectSlotsByName(Run)
    # setupUi

    def retranslateUi(self, Run):
        Run.setWindowTitle(QCoreApplication.translate("Run", u"Topas simulation", None))
        self.pushOk.setText(QCoreApplication.translate("Run", u"Ok", None))
    # retranslateUi

