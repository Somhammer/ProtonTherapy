import pydicom
import cv2

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

import numpy as np
import matplotlib.pyplot as plt

import src.variables as var
from src.data import *

from src.ui_patientwindow import Ui_PatientWindow

class PatientWindow(QDialog, Ui_PatientWindow):
    def __init__(self, parent, current=None):
        super(PatientWindow, self).__init__(parent)
        self.setupUi(self)

        if current is None:
            self.current = ""
        else:
            self.current = current
        
        self.fig = plt.figure()
        self.widgetCanvas = QLabel()
        self.gridLayout.addWidget(self.widgetCanvas)
        self.set_action()
        if os.path.exists(os.path.join(var.G_PATIENT.directory, self.current)):
            self.show_image(self.current)
        self.show()
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.closeEvent(event)

    def closeEvent(self, event):
        self.click_close(event)

    def click_close(self, event=None):
        reply = QMessageBox.question(self, "Message", "Are you sure to close?",
          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.accept()
        else:
            if event is None or type(event) == bool:
                return
            else:
                event.ignore()

    def set_action(self):
        self.lineDir.setText(var.G_PATIENT.directory)
        current_idx = 0
        for idx, item in enumerate(var.G_PATIENT.CT):
            if item == self.current: current_idx = idx
            self.comboFiles.addItem(item)
        self.comboFiles.setCurrentIndex(current_idx)
        self.comboFiles.currentTextChanged.connect(lambda: self.show_image(self.comboFiles.currentText()))
        self.pushOpen.clicked.connect(self.open_directory)
        self.pushPrev.clicked.connect(lambda: self.change_image(self.pushPrev))
        self.pushNext.clicked.connect(lambda: self.change_image(self.pushNext))
        self.pushClose.clicked.connect(self.click_close)
        
    def show_image(self, ct):
        # FIXME
        # matplotlib이 Pyside6를 지원하지 않아서 다른 툴로 바꿔야 함.
        return
        """
        CT = pydicom.dcmread(os.path.join(var.G_PATIENT.directory, ct))
        array = int(CT.RescaleSlope) * CT.pixel_array + int(CT.RescaleIntercept)
        center = CT.WindowCenter
        width = CT.WindowWidth
        image = np.clip(array, center - (width / 2), center + (width / 2))
        height, width = image.shape
        channel = 2
        qImg = QImage(image, width, height,  width*channel, QImage.Format_Grayscale16)
        pixmap = QPixmap.fromImage(qImg)
        self.widgetCanvas.setPixmap(pixmap)
        #self.widgetCanvas.resize(pixmap.width(), pixmap.height())
        self.widgetCanvas.show()
        """


    def open_directory(self):
        newdir = ""
        newdir = QFileDialog.getExistingDirectory(self, "Select Patient CT directory")
        if newdir == var.G_PATIENT.directory or newdir == "": return
        else:
            var.G_PATIENT.patient_setup(newdir)
            self.set_action()
    
    def change_image(self, button):
        if button == self.pushNext:
            if self.comboFiles.currentIndex() == self.comboFiles.count()-1: return
            self.comboFiles.setCurrentIndex(self.comboFiles.currentIndex()+1)
        if button == self.pushPrev:
            if self.comboFiles.currentIndex() == 0: return
            self.comboFiles.setCurrentIndex(self.comboFiles.currentIndex()-1)

    def return_para(self):
        return super().exec_()