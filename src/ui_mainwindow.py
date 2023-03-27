# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1298, 782)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u"../../../../../../.designer/icons/ncc.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.actionFileNew = QAction(MainWindow)
        self.actionFileNew.setObjectName(u"actionFileNew")
        icon1 = QIcon()
        icon1.addFile(u"../../../../../../.designer/icons/new.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionFileNew.setIcon(icon1)
        font = QFont()
        self.actionFileNew.setFont(font)
        self.actionFileOpen = QAction(MainWindow)
        self.actionFileOpen.setObjectName(u"actionFileOpen")
        icon2 = QIcon()
        icon2.addFile(u"../../../../../../.designer/icons/open.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionFileOpen.setIcon(icon2)
        self.actionFileSave = QAction(MainWindow)
        self.actionFileSave.setObjectName(u"actionFileSave")
        icon3 = QIcon()
        icon3.addFile(u"../../../../../../.designer/icons/save.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionFileSave.setIcon(icon3)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        icon4 = QIcon()
        icon4.addFile(u"../../../../../../.designer/icons/exit.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionExit.setIcon(icon4)
        self.actionExit.setFont(font)
        self.actionSimLoad = QAction(MainWindow)
        self.actionSimLoad.setObjectName(u"actionSimLoad")
        self.actionSimLoad.setIcon(icon2)
        self.actionScorerNew = QAction(MainWindow)
        self.actionScorerNew.setObjectName(u"actionScorerNew")
        self.actionScorerNew.setIcon(icon2)
        self.actionPatientView = QAction(MainWindow)
        self.actionPatientView.setObjectName(u"actionPatientView")
        icon5 = QIcon()
        icon5.addFile(u"../../../../../../.designer/icons/view.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionPatientView.setIcon(icon5)
        self.actionTempNew = QAction(MainWindow)
        self.actionTempNew.setObjectName(u"actionTempNew")
        self.actionTempNew.setIcon(icon1)
        self.actionTempLoad = QAction(MainWindow)
        self.actionTempLoad.setObjectName(u"actionTempLoad")
        self.actionTempLoad.setIcon(icon2)
        self.actionCompSave = QAction(MainWindow)
        self.actionCompSave.setObjectName(u"actionCompSave")
        self.actionCompSave.setIcon(icon3)
        self.actionTempModify = QAction(MainWindow)
        self.actionTempModify.setObjectName(u"actionTempModify")
        icon6 = QIcon()
        icon6.addFile(u"../../../../../../.designer/icons/write.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionTempModify.setIcon(icon6)
        self.actionScorerModify = QAction(MainWindow)
        self.actionScorerModify.setObjectName(u"actionScorerModify")
        self.actionTempDelete = QAction(MainWindow)
        self.actionTempDelete.setObjectName(u"actionTempDelete")
        icon7 = QIcon()
        icon7.addFile(u"../../../../../../.designer/icons/delete.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionTempDelete.setIcon(icon7)
        self.actionCompAdd = QAction(MainWindow)
        self.actionCompAdd.setObjectName(u"actionCompAdd")
        self.actionCompAdd.setIcon(icon1)
        self.actionTemplate = QAction(MainWindow)
        self.actionTemplate.setObjectName(u"actionTemplate")
        self.actionComponent = QAction(MainWindow)
        self.actionComponent.setObjectName(u"actionComponent")
        self.actionCompModify = QAction(MainWindow)
        self.actionCompModify.setObjectName(u"actionCompModify")
        self.actionCompModify.setIcon(icon6)
        self.actionCompDelete = QAction(MainWindow)
        self.actionCompDelete.setObjectName(u"actionCompDelete")
        self.actionCompDelete.setIcon(icon7)
        self.actionCompNew = QAction(MainWindow)
        self.actionCompNew.setObjectName(u"actionCompNew")
        self.actionScorerDelete = QAction(MainWindow)
        self.actionScorerDelete.setObjectName(u"actionScorerDelete")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(u"gridLayout")
        self.listComponents = QListWidget(self.centralwidget)
        self.listComponents.setObjectName(u"listComponents")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.listComponents.sizePolicy().hasHeightForWidth())
        self.listComponents.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.listComponents, 3, 0, 1, 3)

        self.frameParameters = QFrame(self.centralwidget)
        self.frameParameters.setObjectName(u"frameParameters")
        self.frameParameters.setMinimumSize(QSize(0, 330))
        self.frameParameters.setFrameShape(QFrame.NoFrame)
        self.frameParameters.setFrameShadow(QFrame.Plain)
        self.gridLayout_6 = QGridLayout(self.frameParameters)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.tabParameters = QTabWidget(self.frameParameters)
        self.tabParameters.setObjectName(u"tabParameters")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tabParameters.sizePolicy().hasHeightForWidth())
        self.tabParameters.setSizePolicy(sizePolicy2)

        self.gridLayout_6.addWidget(self.tabParameters, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frameParameters, 5, 0, 1, 3)

        self.labelComp = QLabel(self.centralwidget)
        self.labelComp.setObjectName(u"labelComp")
        sizePolicy2.setHeightForWidth(self.labelComp.sizePolicy().hasHeightForWidth())
        self.labelComp.setSizePolicy(sizePolicy2)
        font1 = QFont()
        font1.setPointSize(10)
        self.labelComp.setFont(font1)
        self.labelComp.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.labelComp, 2, 0, 1, 3)

        self.labelNozzle = QLabel(self.centralwidget)
        self.labelNozzle.setObjectName(u"labelNozzle")
        font2 = QFont()
        font2.setPointSize(12)
        self.labelNozzle.setFont(font2)

        self.gridLayout.addWidget(self.labelNozzle, 0, 0, 1, 3)

        self.labelNozzlePara = QLabel(self.centralwidget)
        self.labelNozzlePara.setObjectName(u"labelNozzlePara")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.labelNozzlePara.sizePolicy().hasHeightForWidth())
        self.labelNozzlePara.setSizePolicy(sizePolicy3)
        self.labelNozzlePara.setFont(font1)

        self.gridLayout.addWidget(self.labelNozzlePara, 4, 0, 1, 1)

        self.groupNozzleMode = QGroupBox(self.centralwidget)
        self.groupNozzleMode.setObjectName(u"groupNozzleMode")
        sizePolicy2.setHeightForWidth(self.groupNozzleMode.sizePolicy().hasHeightForWidth())
        self.groupNozzleMode.setSizePolicy(sizePolicy2)
        self.groupNozzleMode.setFont(font1)
        self.gridLayout_5 = QGridLayout(self.groupNozzleMode)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.radioFBRT1 = QRadioButton(self.groupNozzleMode)
        self.radioFBRT1.setObjectName(u"radioFBRT1")

        self.gridLayout_5.addWidget(self.radioFBRT1, 0, 0, 1, 1)

        self.radioGTR2 = QRadioButton(self.groupNozzleMode)
        self.radioGTR2.setObjectName(u"radioGTR2")

        self.gridLayout_5.addWidget(self.radioGTR2, 0, 1, 1, 1)

        self.radioGTR3 = QRadioButton(self.groupNozzleMode)
        self.radioGTR3.setObjectName(u"radioGTR3")

        self.gridLayout_5.addWidget(self.radioGTR3, 0, 2, 1, 1)


        self.gridLayout.addWidget(self.groupNozzleMode, 1, 0, 1, 3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 4, 1, 1, 2)


        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 2, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.lineRTP = QLineEdit(self.centralwidget)
        self.lineRTP.setObjectName(u"lineRTP")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.lineRTP.sizePolicy().hasHeightForWidth())
        self.lineRTP.setSizePolicy(sizePolicy4)
        self.lineRTP.setReadOnly(True)

        self.gridLayout_4.addWidget(self.lineRTP, 5, 1, 1, 2)

        self.labelCT = QLabel(self.centralwidget)
        self.labelCT.setObjectName(u"labelCT")
        sizePolicy3.setHeightForWidth(self.labelCT.sizePolicy().hasHeightForWidth())
        self.labelCT.setSizePolicy(sizePolicy3)

        self.gridLayout_4.addWidget(self.labelCT, 3, 0, 1, 3)

        self.lineRTS = QLineEdit(self.centralwidget)
        self.lineRTS.setObjectName(u"lineRTS")
        sizePolicy4.setHeightForWidth(self.lineRTS.sizePolicy().hasHeightForWidth())
        self.lineRTS.setSizePolicy(sizePolicy4)
        self.lineRTS.setReadOnly(True)

        self.gridLayout_4.addWidget(self.lineRTS, 6, 1, 1, 2)

        self.labelPatientDir = QLabel(self.centralwidget)
        self.labelPatientDir.setObjectName(u"labelPatientDir")
        sizePolicy3.setHeightForWidth(self.labelPatientDir.sizePolicy().hasHeightForWidth())
        self.labelPatientDir.setSizePolicy(sizePolicy3)

        self.gridLayout_4.addWidget(self.labelPatientDir, 2, 0, 1, 1)

        self.labelMacro = QLabel(self.centralwidget)
        self.labelMacro.setObjectName(u"labelMacro")
        sizePolicy.setHeightForWidth(self.labelMacro.sizePolicy().hasHeightForWidth())
        self.labelMacro.setSizePolicy(sizePolicy)

        self.gridLayout_4.addWidget(self.labelMacro, 8, 0, 1, 1)

        self.labelRTP = QLabel(self.centralwidget)
        self.labelRTP.setObjectName(u"labelRTP")
        sizePolicy5 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.labelRTP.sizePolicy().hasHeightForWidth())
        self.labelRTP.setSizePolicy(sizePolicy5)

        self.gridLayout_4.addWidget(self.labelRTP, 5, 0, 1, 1)

        self.listPatientCT = QListWidget(self.centralwidget)
        self.listPatientCT.setObjectName(u"listPatientCT")
        sizePolicy.setHeightForWidth(self.listPatientCT.sizePolicy().hasHeightForWidth())
        self.listPatientCT.setSizePolicy(sizePolicy)

        self.gridLayout_4.addWidget(self.listPatientCT, 4, 0, 1, 3)

        self.linePatientDir = QLineEdit(self.centralwidget)
        self.linePatientDir.setObjectName(u"linePatientDir")
        sizePolicy4.setHeightForWidth(self.linePatientDir.sizePolicy().hasHeightForWidth())
        self.linePatientDir.setSizePolicy(sizePolicy4)
        self.linePatientDir.setReadOnly(True)

        self.gridLayout_4.addWidget(self.linePatientDir, 2, 1, 1, 2)

        self.labelScorer = QLabel(self.centralwidget)
        self.labelScorer.setObjectName(u"labelScorer")
        sizePolicy3.setHeightForWidth(self.labelScorer.sizePolicy().hasHeightForWidth())
        self.labelScorer.setSizePolicy(sizePolicy3)
        self.labelScorer.setFont(font2)

        self.gridLayout_4.addWidget(self.labelScorer, 0, 0, 1, 3)

        self.lineMacro = QLineEdit(self.centralwidget)
        self.lineMacro.setObjectName(u"lineMacro")
        sizePolicy4.setHeightForWidth(self.lineMacro.sizePolicy().hasHeightForWidth())
        self.lineMacro.setSizePolicy(sizePolicy4)
        self.lineMacro.setReadOnly(True)

        self.gridLayout_4.addWidget(self.lineMacro, 8, 1, 1, 2)

        self.lineRD = QLineEdit(self.centralwidget)
        self.lineRD.setObjectName(u"lineRD")
        sizePolicy4.setHeightForWidth(self.lineRD.sizePolicy().hasHeightForWidth())
        self.lineRD.setSizePolicy(sizePolicy4)
        self.lineRD.setReadOnly(True)

        self.gridLayout_4.addWidget(self.lineRD, 7, 1, 1, 2)

        self.labelRTS = QLabel(self.centralwidget)
        self.labelRTS.setObjectName(u"labelRTS")

        self.gridLayout_4.addWidget(self.labelRTS, 6, 0, 1, 1)

        self.labelRD = QLabel(self.centralwidget)
        self.labelRD.setObjectName(u"labelRD")

        self.gridLayout_4.addWidget(self.labelRD, 7, 0, 1, 1)

        self.tabScorer = QTabWidget(self.centralwidget)
        self.tabScorer.setObjectName(u"tabScorer")

        self.gridLayout_4.addWidget(self.tabScorer, 1, 0, 1, 3)


        self.gridLayout_3.addLayout(self.gridLayout_4, 0, 3, 2, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.tableComp = QTableWidget(self.centralwidget)
        if (self.tableComp.columnCount() < 17):
            self.tableComp.setColumnCount(17)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignCenter);
        self.tableComp.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setTextAlignment(Qt.AlignCenter);
        self.tableComp.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setTextAlignment(Qt.AlignCenter);
        self.tableComp.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setTextAlignment(Qt.AlignCenter);
        self.tableComp.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setTextAlignment(Qt.AlignCenter);
        self.tableComp.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setTextAlignment(Qt.AlignCenter);
        self.tableComp.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setTextAlignment(Qt.AlignCenter);
        self.tableComp.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setTextAlignment(Qt.AlignCenter);
        self.tableComp.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setTextAlignment(Qt.AlignCenter);
        self.tableComp.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        __qtablewidgetitem9.setTextAlignment(Qt.AlignCenter);
        self.tableComp.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        __qtablewidgetitem10.setTextAlignment(Qt.AlignCenter);
        self.tableComp.setHorizontalHeaderItem(10, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        __qtablewidgetitem11.setTextAlignment(Qt.AlignCenter);
        self.tableComp.setHorizontalHeaderItem(11, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        __qtablewidgetitem12.setTextAlignment(Qt.AlignCenter);
        self.tableComp.setHorizontalHeaderItem(12, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        __qtablewidgetitem13.setTextAlignment(Qt.AlignCenter);
        self.tableComp.setHorizontalHeaderItem(13, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        __qtablewidgetitem14.setTextAlignment(Qt.AlignCenter);
        self.tableComp.setHorizontalHeaderItem(14, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        __qtablewidgetitem15.setTextAlignment(Qt.AlignCenter);
        self.tableComp.setHorizontalHeaderItem(15, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        __qtablewidgetitem16.setTextAlignment(Qt.AlignCenter);
        self.tableComp.setHorizontalHeaderItem(16, __qtablewidgetitem16)
        self.tableComp.setObjectName(u"tableComp")
        sizePolicy.setHeightForWidth(self.tableComp.sizePolicy().hasHeightForWidth())
        self.tableComp.setSizePolicy(sizePolicy)
        self.tableComp.setFont(font1)
        self.tableComp.setFrameShape(QFrame.StyledPanel)
        self.tableComp.setFrameShadow(QFrame.Sunken)
        self.tableComp.setLineWidth(1)
        self.tableComp.setMidLineWidth(1)
        self.tableComp.verticalHeader().setVisible(False)

        self.gridLayout_2.addWidget(self.tableComp, 4, 0, 1, 1)

        self.labelPreview = QLabel(self.centralwidget)
        self.labelPreview.setObjectName(u"labelPreview")
        sizePolicy3.setHeightForWidth(self.labelPreview.sizePolicy().hasHeightForWidth())
        self.labelPreview.setSizePolicy(sizePolicy3)
        self.labelPreview.setMaximumSize(QSize(16777215, 16777215))
        self.labelPreview.setFont(font1)

        self.gridLayout_2.addWidget(self.labelPreview, 1, 0, 1, 1)

        self.widgetNozzle = QWidget(self.centralwidget)
        self.widgetNozzle.setObjectName(u"widgetNozzle")

        self.gridLayout_2.addWidget(self.widgetNozzle, 2, 0, 1, 1)

        self.labelGeometry = QLabel(self.centralwidget)
        self.labelGeometry.setObjectName(u"labelGeometry")
        sizePolicy3.setHeightForWidth(self.labelGeometry.sizePolicy().hasHeightForWidth())
        self.labelGeometry.setSizePolicy(sizePolicy3)
        self.labelGeometry.setFont(font2)

        self.gridLayout_2.addWidget(self.labelGeometry, 0, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 1, 2, 2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1298, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuComp = QMenu(self.menubar)
        self.menuComp.setObjectName(u"menuComp")
        self.menuScorer = QMenu(self.menubar)
        self.menuScorer.setObjectName(u"menuScorer")
        self.menuSimulation = QMenu(self.menubar)
        self.menuSimulation.setObjectName(u"menuSimulation")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuComp.menuAction())
        self.menubar.addAction(self.menuScorer.menuAction())
        self.menubar.addAction(self.menuSimulation.menuAction())
        self.menuFile.addAction(self.actionFileNew)
        self.menuFile.addAction(self.actionFileOpen)
        self.menuFile.addAction(self.actionFileSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuComp.addAction(self.actionCompNew)
        self.menuComp.addAction(self.actionCompModify)
        self.menuComp.addAction(self.actionCompDelete)
        self.menuScorer.addAction(self.actionScorerNew)
        self.menuScorer.addAction(self.actionScorerModify)
        self.menuScorer.addAction(self.actionScorerDelete)
        self.menuSimulation.addAction(self.actionSimLoad)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Proton Therapy Monte Carlo Simulation", None))
        self.actionFileNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
#if QT_CONFIG(shortcut)
        self.actionFileNew.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.actionFileOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(shortcut)
        self.actionFileOpen.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionFileSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(shortcut)
        self.actionFileSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
#if QT_CONFIG(statustip)
        self.actionExit.setStatusTip(QCoreApplication.translate("MainWindow", u"Quit Application", None))
#endif // QT_CONFIG(statustip)
        self.actionSimLoad.setText(QCoreApplication.translate("MainWindow", u"Simulation", None))
        self.actionScorerNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.actionPatientView.setText(QCoreApplication.translate("MainWindow", u"View", None))
#if QT_CONFIG(shortcut)
        self.actionPatientView.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+V", None))
#endif // QT_CONFIG(shortcut)
        self.actionTempNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.actionTempLoad.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.actionCompSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionTempModify.setText(QCoreApplication.translate("MainWindow", u"Modify", None))
        self.actionScorerModify.setText(QCoreApplication.translate("MainWindow", u"Modify", None))
        self.actionTempDelete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.actionCompAdd.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.actionTemplate.setText(QCoreApplication.translate("MainWindow", u"Template", None))
        self.actionComponent.setText(QCoreApplication.translate("MainWindow", u"Component", None))
        self.actionCompModify.setText(QCoreApplication.translate("MainWindow", u"Modify", None))
        self.actionCompDelete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.actionCompNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.actionScorerDelete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.labelComp.setText(QCoreApplication.translate("MainWindow", u"Nozzle Component", None))
        self.labelNozzle.setText(QCoreApplication.translate("MainWindow", u"Nozzle", None))
        self.labelNozzlePara.setText(QCoreApplication.translate("MainWindow", u"Parameters", None))
        self.groupNozzleMode.setTitle(QCoreApplication.translate("MainWindow", u"Type", None))
        self.radioFBRT1.setText(QCoreApplication.translate("MainWindow", u"FBRT 1", None))
        self.radioGTR2.setText(QCoreApplication.translate("MainWindow", u"GTR 2", None))
        self.radioGTR3.setText(QCoreApplication.translate("MainWindow", u"GTR 3", None))
        self.labelCT.setText(QCoreApplication.translate("MainWindow", u"CT", None))
        self.labelPatientDir.setText(QCoreApplication.translate("MainWindow", u"Directory", None))
        self.labelMacro.setText(QCoreApplication.translate("MainWindow", u"Macro", None))
        self.labelRTP.setText(QCoreApplication.translate("MainWindow", u"RTP", None))
        self.labelScorer.setText(QCoreApplication.translate("MainWindow", u"Scorer", None))
        self.labelRTS.setText(QCoreApplication.translate("MainWindow", u"RTS", None))
        self.labelRD.setText(QCoreApplication.translate("MainWindow", u"RD", None))
        ___qtablewidgetitem = self.tableComp.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Name", None));
        ___qtablewidgetitem1 = self.tableComp.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Component", None));
        ___qtablewidgetitem2 = self.tableComp.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Parent", None));
        ___qtablewidgetitem3 = self.tableComp.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"HLX", None));
        ___qtablewidgetitem4 = self.tableComp.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"HLY", None));
        ___qtablewidgetitem5 = self.tableComp.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"HLZ", None));
        ___qtablewidgetitem6 = self.tableComp.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"RMin", None));
        ___qtablewidgetitem7 = self.tableComp.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"RMax", None));
        ___qtablewidgetitem8 = self.tableComp.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"HL", None));
        ___qtablewidgetitem9 = self.tableComp.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"SPhi", None));
        ___qtablewidgetitem10 = self.tableComp.horizontalHeaderItem(10)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"DPhi", None));
        ___qtablewidgetitem11 = self.tableComp.horizontalHeaderItem(11)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"RotX", None));
        ___qtablewidgetitem12 = self.tableComp.horizontalHeaderItem(12)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"RotY", None));
        ___qtablewidgetitem13 = self.tableComp.horizontalHeaderItem(13)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"RotZ", None));
        ___qtablewidgetitem14 = self.tableComp.horizontalHeaderItem(14)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"TransX", None));
        ___qtablewidgetitem15 = self.tableComp.horizontalHeaderItem(15)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"TransY", None));
        ___qtablewidgetitem16 = self.tableComp.horizontalHeaderItem(16)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"TransZ", None));
        self.labelPreview.setText(QCoreApplication.translate("MainWindow", u"2D Preview", None))
        self.labelGeometry.setText(QCoreApplication.translate("MainWindow", u"Geometry", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuComp.setTitle(QCoreApplication.translate("MainWindow", u"Component", None))
        self.menuScorer.setTitle(QCoreApplication.translate("MainWindow", u"Scorer", None))
        self.menuSimulation.setTitle(QCoreApplication.translate("MainWindow", u"Simulation", None))
    # retranslateUi

