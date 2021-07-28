# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'component.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
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
        Component.resize(1288, 475)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Component.sizePolicy().hasHeightForWidth())
        Component.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u"../icons/ncc.png", QSize(), QIcon.Normal, QIcon.Off)
        Component.setWindowIcon(icon)
        self.horizontalLayout = QHBoxLayout(Component)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout_1 = QGridLayout()
        self.gridLayout_1.setObjectName(u"gridLayout_1")
        self.labelOutput = QLabel(Component)
        self.labelOutput.setObjectName(u"labelOutput")

        self.gridLayout_1.addWidget(self.labelOutput, 1, 0, 1, 1)

        self.lineOutput = QLineEdit(Component)
        self.lineOutput.setObjectName(u"lineOutput")

        self.gridLayout_1.addWidget(self.lineOutput, 1, 1, 1, 2)

        self.listImport = QListWidget(Component)
        self.listImport.setObjectName(u"listImport")

        self.gridLayout_1.addWidget(self.listImport, 4, 0, 3, 3)

        self.pushImportClear = QPushButton(Component)
        self.pushImportClear.setObjectName(u"pushImportClear")

        self.gridLayout_1.addWidget(self.pushImportClear, 3, 2, 1, 1)

        self.pushImport = QPushButton(Component)
        self.pushImport.setObjectName(u"pushImport")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushImport.sizePolicy().hasHeightForWidth())
        self.pushImport.setSizePolicy(sizePolicy1)
        self.pushImport.setFocusPolicy(Qt.NoFocus)

        self.gridLayout_1.addWidget(self.pushImport, 3, 0, 1, 2)

        self.labelCtype = QLabel(Component)
        self.labelCtype.setObjectName(u"labelCtype")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.labelCtype.sizePolicy().hasHeightForWidth())
        self.labelCtype.setSizePolicy(sizePolicy2)

        self.gridLayout_1.addWidget(self.labelCtype, 2, 0, 1, 1)

        self.lineCtype = QLineEdit(Component)
        self.lineCtype.setObjectName(u"lineCtype")

        self.gridLayout_1.addWidget(self.lineCtype, 2, 1, 1, 2)


        self.horizontalLayout.addLayout(self.gridLayout_1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pushChangeName = QPushButton(Component)
        self.pushChangeName.setObjectName(u"pushChangeName")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.pushChangeName.sizePolicy().hasHeightForWidth())
        self.pushChangeName.setSizePolicy(sizePolicy3)

        self.gridLayout_2.addWidget(self.pushChangeName, 0, 3, 1, 1)

        self.pushClearVals = QPushButton(Component)
        self.pushClearVals.setObjectName(u"pushClearVals")
        sizePolicy3.setHeightForWidth(self.pushClearVals.sizePolicy().hasHeightForWidth())
        self.pushClearVals.setSizePolicy(sizePolicy3)

        self.gridLayout_2.addWidget(self.pushClearVals, 2, 6, 1, 1)

        self.lineNewParaName = QLineEdit(Component)
        self.lineNewParaName.setObjectName(u"lineNewParaName")
        sizePolicy3.setHeightForWidth(self.lineNewParaName.sizePolicy().hasHeightForWidth())
        self.lineNewParaName.setSizePolicy(sizePolicy3)

        self.gridLayout_2.addWidget(self.lineNewParaName, 2, 1, 1, 2)

        self.lineNewParaValue = QLineEdit(Component)
        self.lineNewParaValue.setObjectName(u"lineNewParaValue")
        sizePolicy3.setHeightForWidth(self.lineNewParaValue.sizePolicy().hasHeightForWidth())
        self.lineNewParaValue.setSizePolicy(sizePolicy3)
        self.lineNewParaValue.setFocusPolicy(Qt.StrongFocus)

        self.gridLayout_2.addWidget(self.lineNewParaValue, 2, 3, 1, 2)

        self.pushAdd = QPushButton(Component)
        self.pushAdd.setObjectName(u"pushAdd")
        sizePolicy3.setHeightForWidth(self.pushAdd.sizePolicy().hasHeightForWidth())
        self.pushAdd.setSizePolicy(sizePolicy3)
        self.pushAdd.setFocusPolicy(Qt.NoFocus)

        self.gridLayout_2.addWidget(self.pushAdd, 2, 5, 1, 1)

        self.comboComp = QComboBox(Component)
        self.comboComp.setObjectName(u"comboComp")
        sizePolicy3.setHeightForWidth(self.comboComp.sizePolicy().hasHeightForWidth())
        self.comboComp.setSizePolicy(sizePolicy3)

        self.gridLayout_2.addWidget(self.comboComp, 0, 0, 1, 1)

        self.labelSubname = QLabel(Component)
        self.labelSubname.setObjectName(u"labelSubname")
        self.labelSubname.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.labelSubname, 0, 4, 1, 1)

        self.pushChangeSubname = QPushButton(Component)
        self.pushChangeSubname.setObjectName(u"pushChangeSubname")

        self.gridLayout_2.addWidget(self.pushChangeSubname, 0, 6, 1, 1)

        self.labelVariable = QLabel(Component)
        self.labelVariable.setObjectName(u"labelVariable")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.labelVariable.sizePolicy().hasHeightForWidth())
        self.labelVariable.setSizePolicy(sizePolicy4)
        font = QFont()
        font.setPointSize(10)
        self.labelVariable.setFont(font)
        self.labelVariable.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.labelVariable, 2, 0, 1, 1)

        self.tabComp = QTabWidget(Component)
        self.tabComp.setObjectName(u"tabComp")
        sizePolicy4.setHeightForWidth(self.tabComp.sizePolicy().hasHeightForWidth())
        self.tabComp.setSizePolicy(sizePolicy4)
        self.tabComp.setMouseTracking(False)
        self.tabComp.setFocusPolicy(Qt.TabFocus)

        self.gridLayout_2.addWidget(self.tabComp, 1, 0, 1, 7)

        self.lineName = QLineEdit(Component)
        self.lineName.setObjectName(u"lineName")
        sizePolicy3.setHeightForWidth(self.lineName.sizePolicy().hasHeightForWidth())
        self.lineName.setSizePolicy(sizePolicy3)

        self.gridLayout_2.addWidget(self.lineName, 0, 2, 1, 1)

        self.labelName = QLabel(Component)
        self.labelName.setObjectName(u"labelName")
        self.labelName.setFont(font)
        self.labelName.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.labelName, 0, 1, 1, 1)

        self.lineSubname = QLineEdit(Component)
        self.lineSubname.setObjectName(u"lineSubname")

        self.gridLayout_2.addWidget(self.lineSubname, 0, 5, 1, 1)

        self.pushAppend = QPushButton(Component)
        self.pushAppend.setObjectName(u"pushAppend")
        sizePolicy3.setHeightForWidth(self.pushAppend.sizePolicy().hasHeightForWidth())
        self.pushAppend.setSizePolicy(sizePolicy3)
        self.pushAppend.setFocusPolicy(Qt.NoFocus)

        self.gridLayout_2.addWidget(self.pushAppend, 3, 0, 1, 2)

        self.pushAppendAll = QPushButton(Component)
        self.pushAppendAll.setObjectName(u"pushAppendAll")
        sizePolicy1.setHeightForWidth(self.pushAppendAll.sizePolicy().hasHeightForWidth())
        self.pushAppendAll.setSizePolicy(sizePolicy1)
        self.pushAppendAll.setFocusPolicy(Qt.NoFocus)

        self.gridLayout_2.addWidget(self.pushAppendAll, 3, 2, 1, 2)

        self.pushClearAll = QPushButton(Component)
        self.pushClearAll.setObjectName(u"pushClearAll")

        self.gridLayout_2.addWidget(self.pushClearAll, 3, 6, 1, 1)

        self.pushDeleteTab = QPushButton(Component)
        self.pushDeleteTab.setObjectName(u"pushDeleteTab")

        self.gridLayout_2.addWidget(self.pushDeleteTab, 3, 5, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout_2)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.pushMake = QPushButton(Component)
        self.pushMake.setObjectName(u"pushMake")
        sizePolicy1.setHeightForWidth(self.pushMake.sizePolicy().hasHeightForWidth())
        self.pushMake.setSizePolicy(sizePolicy1)
        self.pushMake.setFocusPolicy(Qt.NoFocus)

        self.gridLayout_3.addWidget(self.pushMake, 2, 0, 1, 1)

        self.pushCancel = QPushButton(Component)
        self.pushCancel.setObjectName(u"pushCancel")
        sizePolicy1.setHeightForWidth(self.pushCancel.sizePolicy().hasHeightForWidth())
        self.pushCancel.setSizePolicy(sizePolicy1)
        self.pushCancel.setFocusPolicy(Qt.NoFocus)

        self.gridLayout_3.addWidget(self.pushCancel, 2, 2, 1, 1)

        self.label = QLabel(Component)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setPointSize(11)
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 3)

        self.textPreview = QTextBrowser(Component)
        self.textPreview.setObjectName(u"textPreview")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.textPreview.sizePolicy().hasHeightForWidth())
        self.textPreview.setSizePolicy(sizePolicy5)

        self.gridLayout_3.addWidget(self.textPreview, 1, 0, 1, 3)

        self.pushClearPrev = QPushButton(Component)
        self.pushClearPrev.setObjectName(u"pushClearPrev")
        sizePolicy1.setHeightForWidth(self.pushClearPrev.sizePolicy().hasHeightForWidth())
        self.pushClearPrev.setSizePolicy(sizePolicy1)

        self.gridLayout_3.addWidget(self.pushClearPrev, 2, 1, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout_3)

        QWidget.setTabOrder(self.listImport, self.pushCancel)
        QWidget.setTabOrder(self.pushCancel, self.textPreview)

        self.retranslateUi(Component)

        self.tabComp.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(Component)
    # setupUi

    def retranslateUi(self, Component):
        Component.setWindowTitle(QCoreApplication.translate("Component", u"Component", None))
        self.labelOutput.setText(QCoreApplication.translate("Component", u"Output:", None))
        self.pushImportClear.setText(QCoreApplication.translate("Component", u"Clear", None))
        self.pushImport.setText(QCoreApplication.translate("Component", u"Import", None))
        self.labelCtype.setText(QCoreApplication.translate("Component", u"Type:", None))
        self.pushChangeName.setText(QCoreApplication.translate("Component", u"Change", None))
        self.pushClearVals.setText(QCoreApplication.translate("Component", u"Clear Values", None))
        self.pushAdd.setText(QCoreApplication.translate("Component", u"Add", None))
        self.labelSubname.setText(QCoreApplication.translate("Component", u"SubName", None))
        self.pushChangeSubname.setText(QCoreApplication.translate("Component", u"Change", None))
        self.labelVariable.setText(QCoreApplication.translate("Component", u"Variable", None))
        self.labelName.setText(QCoreApplication.translate("Component", u"Name", None))
        self.pushAppend.setText(QCoreApplication.translate("Component", u"Append", None))
        self.pushAppendAll.setText(QCoreApplication.translate("Component", u"Append All", None))
        self.pushClearAll.setText(QCoreApplication.translate("Component", u"Clear Template", None))
        self.pushDeleteTab.setText(QCoreApplication.translate("Component", u"Delete Tab", None))
        self.pushMake.setText(QCoreApplication.translate("Component", u"Make", None))
        self.pushCancel.setText(QCoreApplication.translate("Component", u"Cancel", None))
        self.label.setText(QCoreApplication.translate("Component", u"Preview", None))
        self.pushClearPrev.setText(QCoreApplication.translate("Component", u"Clear", None))
    # retranslateUi

