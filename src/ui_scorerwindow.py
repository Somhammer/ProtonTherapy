# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'scorer.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_ScorerWindow(object):
    def setupUi(self, ScorerWindow):
        if not ScorerWindow.objectName():
            ScorerWindow.setObjectName(u"ScorerWindow")
        ScorerWindow.resize(1236, 579)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ScorerWindow.sizePolicy().hasHeightForWidth())
        ScorerWindow.setSizePolicy(sizePolicy)
        ScorerWindow.setMinimumSize(QSize(462, 368))
        ScorerWindow.setMaximumSize(QSize(1236, 800))
        icon = QIcon()
        icon.addFile(u"../../../../../.designer/icons/ncc.png", QSize(), QIcon.Normal, QIcon.Off)
        ScorerWindow.setWindowIcon(icon)
        self.gridLayout_4 = QGridLayout(ScorerWindow)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.comboMacro = QComboBox(ScorerWindow)
        self.comboMacro.setObjectName(u"comboMacro")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboMacro.sizePolicy().hasHeightForWidth())
        self.comboMacro.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.comboMacro, 0, 1, 1, 1)

        self.label_4 = QLabel(ScorerWindow)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 2)

        self.labelRequirement = QLabel(ScorerWindow)
        self.labelRequirement.setObjectName(u"labelRequirement")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.labelRequirement.sizePolicy().hasHeightForWidth())
        self.labelRequirement.setSizePolicy(sizePolicy2)
        font = QFont()
        font.setPointSize(10)
        self.labelRequirement.setFont(font)

        self.gridLayout.addWidget(self.labelRequirement, 1, 0, 1, 2)

        self.label_3 = QLabel(ScorerWindow)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.tabRun = QTabWidget(ScorerWindow)
        self.tabRun.setObjectName(u"tabRun")
        self.tabRun.setMinimumSize(QSize(300, 0))
        self.tabRun.setMaximumSize(QSize(300, 16777215))

        self.gridLayout.addWidget(self.tabRun, 4, 0, 1, 2)

        self.tabRequirement = QTabWidget(ScorerWindow)
        self.tabRequirement.setObjectName(u"tabRequirement")

        self.gridLayout.addWidget(self.tabRequirement, 2, 0, 1, 2)


        self.gridLayout_4.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.lineNewParaValue = QLineEdit(ScorerWindow)
        self.lineNewParaValue.setObjectName(u"lineNewParaValue")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.lineNewParaValue.sizePolicy().hasHeightForWidth())
        self.lineNewParaValue.setSizePolicy(sizePolicy3)

        self.gridLayout_2.addWidget(self.lineNewParaValue, 2, 2, 1, 2)

        self.labelVariable = QLabel(ScorerWindow)
        self.labelVariable.setObjectName(u"labelVariable")
        self.labelVariable.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.labelVariable, 2, 0, 1, 1)

        self.pushAppendComp = QPushButton(ScorerWindow)
        self.pushAppendComp.setObjectName(u"pushAppendComp")

        self.gridLayout_2.addWidget(self.pushAppendComp, 3, 0, 1, 2)

        self.pushAddNewPara = QPushButton(ScorerWindow)
        self.pushAddNewPara.setObjectName(u"pushAddNewPara")
        sizePolicy3.setHeightForWidth(self.pushAddNewPara.sizePolicy().hasHeightForWidth())
        self.pushAddNewPara.setSizePolicy(sizePolicy3)

        self.gridLayout_2.addWidget(self.pushAddNewPara, 2, 4, 1, 1)

        self.label_2 = QLabel(ScorerWindow)
        self.label_2.setObjectName(u"label_2")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy4)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_2, 0, 2, 1, 1)

        self.pushChangeName = QPushButton(ScorerWindow)
        self.pushChangeName.setObjectName(u"pushChangeName")

        self.gridLayout_2.addWidget(self.pushChangeName, 0, 4, 1, 1)

        self.pushClearComp = QPushButton(ScorerWindow)
        self.pushClearComp.setObjectName(u"pushClearComp")

        self.gridLayout_2.addWidget(self.pushClearComp, 3, 2, 1, 3)

        self.tabComp = QTabWidget(ScorerWindow)
        self.tabComp.setObjectName(u"tabComp")
        self.tabComp.setMinimumSize(QSize(400, 0))
        self.tabComp.setMaximumSize(QSize(1000, 16777215))

        self.gridLayout_2.addWidget(self.tabComp, 1, 0, 1, 5)

        self.lineNewParaName = QLineEdit(ScorerWindow)
        self.lineNewParaName.setObjectName(u"lineNewParaName")
        sizePolicy5 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.lineNewParaName.sizePolicy().hasHeightForWidth())
        self.lineNewParaName.setSizePolicy(sizePolicy5)

        self.gridLayout_2.addWidget(self.lineNewParaName, 2, 1, 1, 1)

        self.comboComp = QComboBox(ScorerWindow)
        self.comboComp.setObjectName(u"comboComp")

        self.gridLayout_2.addWidget(self.comboComp, 0, 0, 1, 2)

        self.lineCompName = QLineEdit(ScorerWindow)
        self.lineCompName.setObjectName(u"lineCompName")

        self.gridLayout_2.addWidget(self.lineCompName, 0, 3, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 1, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.listTemplates = QListWidget(ScorerWindow)
        self.listTemplates.setObjectName(u"listTemplates")
        self.listTemplates.setMinimumSize(QSize(400, 0))
        self.listTemplates.setMaximumSize(QSize(400, 16777215))

        self.gridLayout_3.addWidget(self.listTemplates, 1, 0, 1, 3)

        self.pushClear = QPushButton(ScorerWindow)
        self.pushClear.setObjectName(u"pushClear")

        self.gridLayout_3.addWidget(self.pushClear, 3, 1, 1, 1)

        self.pushMake = QPushButton(ScorerWindow)
        self.pushMake.setObjectName(u"pushMake")

        self.gridLayout_3.addWidget(self.pushMake, 3, 0, 1, 1)

        self.pushCancel = QPushButton(ScorerWindow)
        self.pushCancel.setObjectName(u"pushCancel")

        self.gridLayout_3.addWidget(self.pushCancel, 3, 2, 1, 1)

        self.label = QLabel(ScorerWindow)
        self.label.setObjectName(u"label")
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 3)

        self.tabScorer = QTabWidget(ScorerWindow)
        self.tabScorer.setObjectName(u"tabScorer")

        self.gridLayout_3.addWidget(self.tabScorer, 2, 0, 1, 3)


        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 2, 1, 1)


        self.retranslateUi(ScorerWindow)

        self.tabRun.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(ScorerWindow)
    # setupUi

    def retranslateUi(self, ScorerWindow):
        ScorerWindow.setWindowTitle(QCoreApplication.translate("ScorerWindow", u"Scorer", None))
        self.label_4.setText(QCoreApplication.translate("ScorerWindow", u"Nozzle Component", None))
        self.labelRequirement.setText(QCoreApplication.translate("ScorerWindow", u"Requirements", None))
        self.label_3.setText(QCoreApplication.translate("ScorerWindow", u"Plugin", None))
        self.labelVariable.setText(QCoreApplication.translate("ScorerWindow", u"Variable", None))
        self.pushAppendComp.setText(QCoreApplication.translate("ScorerWindow", u"Append", None))
        self.pushAddNewPara.setText(QCoreApplication.translate("ScorerWindow", u"Add", None))
        self.label_2.setText(QCoreApplication.translate("ScorerWindow", u"Name", None))
        self.pushChangeName.setText(QCoreApplication.translate("ScorerWindow", u"Change", None))
        self.pushClearComp.setText(QCoreApplication.translate("ScorerWindow", u"Clear", None))
        self.pushClear.setText(QCoreApplication.translate("ScorerWindow", u"Clear", None))
        self.pushMake.setText(QCoreApplication.translate("ScorerWindow", u"Make", None))
        self.pushCancel.setText(QCoreApplication.translate("ScorerWindow", u"Cancel", None))
        self.label.setText(QCoreApplication.translate("ScorerWindow", u"Scorer Components", None))
    # retranslateUi

