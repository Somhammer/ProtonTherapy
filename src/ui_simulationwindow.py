# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'simulation.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_SimulationWindow(object):
    def setupUi(self, Simulation):
        if not Simulation.objectName():
            Simulation.setObjectName(u"Simulation")
        Simulation.resize(1236, 579)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Simulation.sizePolicy().hasHeightForWidth())
        Simulation.setSizePolicy(sizePolicy)
        Simulation.setMinimumSize(QSize(462, 368))
        Simulation.setMaximumSize(QSize(1236, 800))
        icon = QIcon()
        icon.addFile(u"../../../../../.designer/icons/ncc.png", QSize(), QIcon.Normal, QIcon.Off)
        Simulation.setWindowIcon(icon)
        self.gridLayout_4 = QGridLayout(Simulation)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelRequirement = QLabel(Simulation)
        self.labelRequirement.setObjectName(u"labelRequirement")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.labelRequirement.sizePolicy().hasHeightForWidth())
        self.labelRequirement.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(10)
        self.labelRequirement.setFont(font)

        self.gridLayout.addWidget(self.labelRequirement, 1, 0, 1, 2)

        self.comboMacro = QComboBox(Simulation)
        self.comboMacro.setObjectName(u"comboMacro")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.comboMacro.sizePolicy().hasHeightForWidth())
        self.comboMacro.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.comboMacro, 0, 1, 1, 1)

        self.labelImport = QLabel(Simulation)
        self.labelImport.setObjectName(u"labelImport")
        sizePolicy1.setHeightForWidth(self.labelImport.sizePolicy().hasHeightForWidth())
        self.labelImport.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.labelImport, 3, 0, 1, 1)

        self.pushOpenFile = QPushButton(Simulation)
        self.pushOpenFile.setObjectName(u"pushOpenFile")

        self.gridLayout.addWidget(self.pushOpenFile, 3, 1, 1, 1)

        self.label_3 = QLabel(Simulation)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.listRequirement = QListWidget(Simulation)
        self.listRequirement.setObjectName(u"listRequirement")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.listRequirement.sizePolicy().hasHeightForWidth())
        self.listRequirement.setSizePolicy(sizePolicy3)
        self.listRequirement.setMinimumSize(QSize(0, 200))
        self.listRequirement.setMaximumSize(QSize(300, 200))

        self.gridLayout.addWidget(self.listRequirement, 2, 0, 1, 2)

        self.tabImport = QTabWidget(Simulation)
        self.tabImport.setObjectName(u"tabImport")
        self.tabImport.setMinimumSize(QSize(300, 0))
        self.tabImport.setMaximumSize(QSize(300, 16777215))

        self.gridLayout.addWidget(self.tabImport, 4, 0, 1, 2)


        self.gridLayout_4.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.lineNewParaValue = QLineEdit(Simulation)
        self.lineNewParaValue.setObjectName(u"lineNewParaValue")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.lineNewParaValue.sizePolicy().hasHeightForWidth())
        self.lineNewParaValue.setSizePolicy(sizePolicy4)

        self.gridLayout_2.addWidget(self.lineNewParaValue, 2, 2, 1, 2)

        self.labelVariable = QLabel(Simulation)
        self.labelVariable.setObjectName(u"labelVariable")
        self.labelVariable.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.labelVariable, 2, 0, 1, 1)

        self.pushAppendComp = QPushButton(Simulation)
        self.pushAppendComp.setObjectName(u"pushAppendComp")

        self.gridLayout_2.addWidget(self.pushAppendComp, 3, 0, 1, 2)

        self.pushAddNewPara = QPushButton(Simulation)
        self.pushAddNewPara.setObjectName(u"pushAddNewPara")
        sizePolicy4.setHeightForWidth(self.pushAddNewPara.sizePolicy().hasHeightForWidth())
        self.pushAddNewPara.setSizePolicy(sizePolicy4)

        self.gridLayout_2.addWidget(self.pushAddNewPara, 2, 4, 1, 1)

        self.label_2 = QLabel(Simulation)
        self.label_2.setObjectName(u"label_2")
        sizePolicy3.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy3)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_2, 0, 2, 1, 1)

        self.pushChangeName = QPushButton(Simulation)
        self.pushChangeName.setObjectName(u"pushChangeName")

        self.gridLayout_2.addWidget(self.pushChangeName, 0, 4, 1, 1)

        self.pushClearComp = QPushButton(Simulation)
        self.pushClearComp.setObjectName(u"pushClearComp")

        self.gridLayout_2.addWidget(self.pushClearComp, 3, 2, 1, 3)

        self.tabComp = QTabWidget(Simulation)
        self.tabComp.setObjectName(u"tabComp")
        self.tabComp.setMinimumSize(QSize(400, 0))
        self.tabComp.setMaximumSize(QSize(1000, 16777215))

        self.gridLayout_2.addWidget(self.tabComp, 1, 0, 1, 5)

        self.lineNewParaName = QLineEdit(Simulation)
        self.lineNewParaName.setObjectName(u"lineNewParaName")
        sizePolicy5 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.lineNewParaName.sizePolicy().hasHeightForWidth())
        self.lineNewParaName.setSizePolicy(sizePolicy5)

        self.gridLayout_2.addWidget(self.lineNewParaName, 2, 1, 1, 1)

        self.comboComp = QComboBox(Simulation)
        self.comboComp.setObjectName(u"comboComp")

        self.gridLayout_2.addWidget(self.comboComp, 0, 0, 1, 2)

        self.lineCompName = QLineEdit(Simulation)
        self.lineCompName.setObjectName(u"lineCompName")

        self.gridLayout_2.addWidget(self.lineCompName, 0, 3, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 1, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.listTemplates = QListWidget(Simulation)
        self.listTemplates.setObjectName(u"listTemplates")
        self.listTemplates.setMinimumSize(QSize(400, 0))
        self.listTemplates.setMaximumSize(QSize(400, 16777215))

        self.gridLayout_3.addWidget(self.listTemplates, 1, 0, 1, 3)

        self.pushClear = QPushButton(Simulation)
        self.pushClear.setObjectName(u"pushClear")

        self.gridLayout_3.addWidget(self.pushClear, 3, 1, 1, 1)

        self.pushMake = QPushButton(Simulation)
        self.pushMake.setObjectName(u"pushMake")

        self.gridLayout_3.addWidget(self.pushMake, 3, 0, 1, 1)

        self.pushCancel = QPushButton(Simulation)
        self.pushCancel.setObjectName(u"pushCancel")

        self.gridLayout_3.addWidget(self.pushCancel, 3, 2, 1, 1)

        self.label = QLabel(Simulation)
        self.label.setObjectName(u"label")
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 3)

        self.tabComponents = QTabWidget(Simulation)
        self.tabComponents.setObjectName(u"tabComponents")

        self.gridLayout_3.addWidget(self.tabComponents, 2, 0, 1, 3)


        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 2, 1, 1)


        self.retranslateUi(Simulation)

        self.tabImport.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(Simulation)
    # setupUi

    def retranslateUi(self, Simulation):
        Simulation.setWindowTitle(QCoreApplication.translate("Simulation", u"Simulation", None))
        self.labelRequirement.setText(QCoreApplication.translate("Simulation", u"Requirements", None))
        self.labelImport.setText(QCoreApplication.translate("Simulation", u"Import Files", None))
        self.pushOpenFile.setText(QCoreApplication.translate("Simulation", u"Open", None))
        self.label_3.setText(QCoreApplication.translate("Simulation", u"Plugin", None))
        self.labelVariable.setText(QCoreApplication.translate("Simulation", u"Variable", None))
        self.pushAppendComp.setText(QCoreApplication.translate("Simulation", u"Append", None))
        self.pushAddNewPara.setText(QCoreApplication.translate("Simulation", u"Add", None))
        self.label_2.setText(QCoreApplication.translate("Simulation", u"Name", None))
        self.pushChangeName.setText(QCoreApplication.translate("Simulation", u"Change", None))
        self.pushClearComp.setText(QCoreApplication.translate("Simulation", u"Clear", None))
        self.pushClear.setText(QCoreApplication.translate("Simulation", u"Clear", None))
        self.pushMake.setText(QCoreApplication.translate("Simulation", u"Make", None))
        self.pushCancel.setText(QCoreApplication.translate("Simulation", u"Cancel", None))
        self.label.setText(QCoreApplication.translate("Simulation", u"Simulation Components", None))
    # retranslateUi

