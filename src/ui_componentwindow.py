# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'component.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_ComponentWindow(object):
    def setupUi(self, Component):
        if not Component.objectName():
            Component.setObjectName(u"Component")
        Component.setWindowModality(Qt.ApplicationModal)
        Component.resize(1260, 572)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Component.sizePolicy().hasHeightForWidth())
        Component.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u"../../../../.designer/icons/ncc.png", QSize(), QIcon.Normal, QIcon.Off)
        Component.setWindowIcon(icon)
        self.horizontalLayout = QHBoxLayout(Component)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout_1 = QGridLayout()
        self.gridLayout_1.setObjectName(u"gridLayout_1")
        self.listImport = QListWidget(Component)
        self.listImport.setObjectName(u"listImport")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.listImport.sizePolicy().hasHeightForWidth())
        self.listImport.setSizePolicy(sizePolicy1)

        self.gridLayout_1.addWidget(self.listImport, 4, 0, 3, 3)

        self.lineFileName = QLineEdit(Component)
        self.lineFileName.setObjectName(u"lineFileName")

        self.gridLayout_1.addWidget(self.lineFileName, 1, 1, 1, 2)

        self.comboPreset = QComboBox(Component)
        self.comboPreset.setObjectName(u"comboPreset")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.comboPreset.sizePolicy().hasHeightForWidth())
        self.comboPreset.setSizePolicy(sizePolicy2)

        self.gridLayout_1.addWidget(self.comboPreset, 0, 0, 1, 3)

        self.labelFileName = QLabel(Component)
        self.labelFileName.setObjectName(u"labelFileName")
        self.labelFileName.setAlignment(Qt.AlignCenter)

        self.gridLayout_1.addWidget(self.labelFileName, 1, 0, 1, 1)

        self.pushImportClear = QPushButton(Component)
        self.pushImportClear.setObjectName(u"pushImportClear")
        sizePolicy2.setHeightForWidth(self.pushImportClear.sizePolicy().hasHeightForWidth())
        self.pushImportClear.setSizePolicy(sizePolicy2)
        self.pushImportClear.setMaximumSize(QSize(75, 16777215))

        self.gridLayout_1.addWidget(self.pushImportClear, 3, 2, 1, 1)

        self.pushImport = QPushButton(Component)
        self.pushImport.setObjectName(u"pushImport")
        sizePolicy2.setHeightForWidth(self.pushImport.sizePolicy().hasHeightForWidth())
        self.pushImport.setSizePolicy(sizePolicy2)
        self.pushImport.setMaximumSize(QSize(75, 16777215))
        self.pushImport.setFocusPolicy(Qt.NoFocus)

        self.gridLayout_1.addWidget(self.pushImport, 3, 1, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout_1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pushOk = QPushButton(Component)
        self.pushOk.setObjectName(u"pushOk")
        sizePolicy2.setHeightForWidth(self.pushOk.sizePolicy().hasHeightForWidth())
        self.pushOk.setSizePolicy(sizePolicy2)
        self.pushOk.setFocusPolicy(Qt.NoFocus)

        self.gridLayout_2.addWidget(self.pushOk, 3, 9, 1, 1)

        self.labelNewVariName = QLabel(Component)
        self.labelNewVariName.setObjectName(u"labelNewVariName")
        self.labelNewVariName.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.labelNewVariName, 2, 3, 1, 1)

        self.pushCancel = QPushButton(Component)
        self.pushCancel.setObjectName(u"pushCancel")
        sizePolicy2.setHeightForWidth(self.pushCancel.sizePolicy().hasHeightForWidth())
        self.pushCancel.setSizePolicy(sizePolicy2)
        self.pushCancel.setFocusPolicy(Qt.NoFocus)

        self.gridLayout_2.addWidget(self.pushCancel, 3, 10, 1, 1)

        self.pushClearVari = QPushButton(Component)
        self.pushClearVari.setObjectName(u"pushClearVari")
        sizePolicy2.setHeightForWidth(self.pushClearVari.sizePolicy().hasHeightForWidth())
        self.pushClearVari.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.pushClearVari, 3, 8, 1, 1)

        self.tabComp = QTabWidget(Component)
        self.tabComp.setObjectName(u"tabComp")
        sizePolicy1.setHeightForWidth(self.tabComp.sizePolicy().hasHeightForWidth())
        self.tabComp.setSizePolicy(sizePolicy1)
        self.tabComp.setMouseTracking(False)
        self.tabComp.setFocusPolicy(Qt.TabFocus)

        self.gridLayout_2.addWidget(self.tabComp, 1, 0, 1, 11)

        self.labelNewVariUnit = QLabel(Component)
        self.labelNewVariUnit.setObjectName(u"labelNewVariUnit")
        self.labelNewVariUnit.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.labelNewVariUnit, 2, 6, 1, 1)

        self.lineTabName = QLineEdit(Component)
        self.lineTabName.setObjectName(u"lineTabName")
        sizePolicy2.setHeightForWidth(self.lineTabName.sizePolicy().hasHeightForWidth())
        self.lineTabName.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.lineTabName, 0, 3, 1, 1)

        self.labelNewVariType = QLabel(Component)
        self.labelNewVariType.setObjectName(u"labelNewVariType")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.labelNewVariType.sizePolicy().hasHeightForWidth())
        self.labelNewVariType.setSizePolicy(sizePolicy3)
        self.labelNewVariType.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.labelNewVariType, 2, 1, 1, 1)

        self.lineNewVariValue = QLineEdit(Component)
        self.lineNewVariValue.setObjectName(u"lineNewVariValue")
        sizePolicy2.setHeightForWidth(self.lineNewVariValue.sizePolicy().hasHeightForWidth())
        self.lineNewVariValue.setSizePolicy(sizePolicy2)
        self.lineNewVariValue.setFocusPolicy(Qt.StrongFocus)

        self.gridLayout_2.addWidget(self.lineNewVariValue, 3, 4, 1, 2)

        self.lineNewVariUnit = QLineEdit(Component)
        self.lineNewVariUnit.setObjectName(u"lineNewVariUnit")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.lineNewVariUnit.sizePolicy().hasHeightForWidth())
        self.lineNewVariUnit.setSizePolicy(sizePolicy4)
        self.lineNewVariUnit.setMaximumSize(QSize(75, 16777215))

        self.gridLayout_2.addWidget(self.lineNewVariUnit, 3, 6, 1, 1)

        self.pushAddVari = QPushButton(Component)
        self.pushAddVari.setObjectName(u"pushAddVari")
        sizePolicy2.setHeightForWidth(self.pushAddVari.sizePolicy().hasHeightForWidth())
        self.pushAddVari.setSizePolicy(sizePolicy2)
        self.pushAddVari.setFocusPolicy(Qt.NoFocus)

        self.gridLayout_2.addWidget(self.pushAddVari, 3, 7, 1, 1)

        self.labelNewVari = QLabel(Component)
        self.labelNewVari.setObjectName(u"labelNewVari")
        sizePolicy1.setHeightForWidth(self.labelNewVari.sizePolicy().hasHeightForWidth())
        self.labelNewVari.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(10)
        self.labelNewVari.setFont(font)
        self.labelNewVari.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.labelNewVari, 3, 0, 1, 1)

        self.pushDeleteAllTabs = QPushButton(Component)
        self.pushDeleteAllTabs.setObjectName(u"pushDeleteAllTabs")
        sizePolicy2.setHeightForWidth(self.pushDeleteAllTabs.sizePolicy().hasHeightForWidth())
        self.pushDeleteAllTabs.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.pushDeleteAllTabs, 0, 10, 1, 1)

        self.pushChangeTabName = QPushButton(Component)
        self.pushChangeTabName.setObjectName(u"pushChangeTabName")
        sizePolicy2.setHeightForWidth(self.pushChangeTabName.sizePolicy().hasHeightForWidth())
        self.pushChangeTabName.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.pushChangeTabName, 0, 4, 1, 1)

        self.lineNewVariName = QLineEdit(Component)
        self.lineNewVariName.setObjectName(u"lineNewVariName")
        sizePolicy2.setHeightForWidth(self.lineNewVariName.sizePolicy().hasHeightForWidth())
        self.lineNewVariName.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.lineNewVariName, 3, 3, 1, 1)

        self.pushDeleteTab = QPushButton(Component)
        self.pushDeleteTab.setObjectName(u"pushDeleteTab")
        sizePolicy2.setHeightForWidth(self.pushDeleteTab.sizePolicy().hasHeightForWidth())
        self.pushDeleteTab.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.pushDeleteTab, 0, 9, 1, 1)

        self.pushAddTab = QPushButton(Component)
        self.pushAddTab.setObjectName(u"pushAddTab")
        sizePolicy2.setHeightForWidth(self.pushAddTab.sizePolicy().hasHeightForWidth())
        self.pushAddTab.setSizePolicy(sizePolicy2)
        self.pushAddTab.setFocusPolicy(Qt.NoFocus)

        self.gridLayout_2.addWidget(self.pushAddTab, 0, 8, 1, 1)

        self.labelNewVariValue = QLabel(Component)
        self.labelNewVariValue.setObjectName(u"labelNewVariValue")
        self.labelNewVariValue.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.labelNewVariValue, 2, 4, 1, 2)

        self.labelTabName = QLabel(Component)
        self.labelTabName.setObjectName(u"labelTabName")
        self.labelTabName.setFont(font)
        self.labelTabName.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.labelTabName, 0, 0, 1, 2)

        self.comboNewVariPrefix = QComboBox(Component)
        self.comboNewVariPrefix.setObjectName(u"comboNewVariPrefix")

        self.gridLayout_2.addWidget(self.comboNewVariPrefix, 3, 2, 1, 1)

        self.comboNewVariType = QComboBox(Component)
        self.comboNewVariType.setObjectName(u"comboNewVariType")

        self.gridLayout_2.addWidget(self.comboNewVariType, 3, 1, 1, 1)

        self.labelNewVariPrefix = QLabel(Component)
        self.labelNewVariPrefix.setObjectName(u"labelNewVariPrefix")
        self.labelNewVariPrefix.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.labelNewVariPrefix, 2, 2, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout_2)


        self.retranslateUi(Component)

        self.tabComp.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(Component)
    # setupUi

    def retranslateUi(self, Component):
        Component.setWindowTitle(QCoreApplication.translate("Component", u"Component", None))
        self.labelFileName.setText(QCoreApplication.translate("Component", u"File name:", None))
        self.pushImportClear.setText(QCoreApplication.translate("Component", u"Clear", None))
        self.pushImport.setText(QCoreApplication.translate("Component", u"Import", None))
        self.pushOk.setText(QCoreApplication.translate("Component", u"Ok", None))
        self.labelNewVariName.setText(QCoreApplication.translate("Component", u"Name", None))
        self.pushCancel.setText(QCoreApplication.translate("Component", u"Cancel", None))
        self.pushClearVari.setText(QCoreApplication.translate("Component", u"Clear", None))
        self.labelNewVariUnit.setText(QCoreApplication.translate("Component", u"Unit", None))
        self.labelNewVariType.setText(QCoreApplication.translate("Component", u"Type", None))
        self.pushAddVari.setText(QCoreApplication.translate("Component", u"Add", None))
        self.labelNewVari.setText(QCoreApplication.translate("Component", u"Variable", None))
        self.pushDeleteAllTabs.setText(QCoreApplication.translate("Component", u"Delete All", None))
        self.pushChangeTabName.setText(QCoreApplication.translate("Component", u"Change", None))
        self.pushDeleteTab.setText(QCoreApplication.translate("Component", u"Delete Tab", None))
        self.pushAddTab.setText(QCoreApplication.translate("Component", u"Add Tab", None))
        self.labelNewVariValue.setText(QCoreApplication.translate("Component", u"Value", None))
        self.labelTabName.setText(QCoreApplication.translate("Component", u"Tab name", None))
        self.labelNewVariPrefix.setText(QCoreApplication.translate("Component", u"Prefix", None))
    # retranslateUi

