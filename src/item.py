from PySide6.QtWidgets import *

from src.variables import G_TEXT_EXTENSION, G_EXCEL_EXTENSION

class Item(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.layout = QBoxLayout(QBoxLayout.LeftToRight)

    def add_label(self, name):
        self.label = QLabel(name)
        self.layout.addWidget(self.label)
        self.layout.setSizeConstraint(QBoxLayout.SetFixedSize)
        self.setLayout(self.layout)
        
    def add_checkbox(self, name, path=None, layout_direction=QBoxLayout.LeftToRight):
        self.checkbox = QCheckBox()

        self.layout.setDirection(layout_direction)
        self.checkbox.setText(name)
        self.checkbox.setChecked(True)
        self.layout.addWidget(self.checkbox)
        if path is not None:
            self.label = QLabel()
            self.label.setText("("+path+")")
            self.layout.addWidget(self.label)
        self.layout.setSizeConstraint(QBoxLayout.SetFixedSize)
        self.setLayout(self.layout)

    def add_lineedit(self, name, value, layout_direction=QBoxLayout.LeftToRight, readonly=False, makebtn=False):
        self.label = QLabel()
        self.lineValue = QLineEdit()
        self.layout.setDirection(layout_direction)

        self.label.setText(name)
        self.lineValue.setText(value)
        if readonly: 
            self.lineValue.setReadOnly(True)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.lineValue)
        if makebtn:
            self.pushOpen = QPushButton("Open")
            self.pushOpen.clicked.connect(self.click_open)
            self.layout.addWidget(self.pushOpen)
        self.layout.setSizeConstraint(QBoxLayout.SetFixedSize)
        self.setLayout(self.layout)

    def click_open(self):
        self.lineValue.setReadOnly(False)
        if self.label.text().lower() == 'patient':
            fname = QFileDialog.getExistingDirectory(self, "Select Patient CT directory")

        self.lineValue.setText(fname)
        self.lineValue.setReadOnly(True)