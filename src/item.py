from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import *
from src.variables import G_TEXT_EXTENSION, G_EXCEL_EXTENSION

class MyLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.prev_text = None
        self.allWords = ['ocean', 'coding', 'python', 'pizza']
        self.trigger_word = "{"
        self.completer = QCompleter(self.allWords)
        #self.completer = MyCompleter(self.allWords)
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        #self.completer.highlighted.connect(self.on_completer_highlighted)
        self.completer.activated.connect(lambda: self.on_completer_activated())

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.text() == self.trigger_word:
            self.setCompleter(self.completer)
            self.completer.highlighted.connect(self.on_completer_highlighted)
            self.completer.complete()
        else:
            self.setCompleter(None)
        super().keyPressEvent(event)
        self.prev_text = self.text()

    def on_completer_highlighted(self, completion: str):
        print("on_completer_highlighted;", self.prev_text, ";", self.text(), ";", completion)
        text = f"{self.prev_text}{completion}}}"
        self.setText(text)

    def insert_completion(self):
        print("insert_completion;", self.prev_text, ";")
        text = f"{self.prev_text}"
        print(text)
        self.setText(text)

    def on_completer_activated(self):
        self.completer.popup().hide()
        QTimer.singleShot(1, lambda: self.insert_completion())

class Item(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.layout = QBoxLayout(QBoxLayout.LeftToRight)
        self.label = QLabel()
        self.checkbox = QCheckBox()

    def get_label(self):
        return self.label

    def get_checkbox(self):
        return self.checkbox

    def add_label(self, name):
        self.label = QLabel(name)
        self.layout.addWidget(self.label)
        self.layout.setSizeConstraint(QBoxLayout.SetFixedSize)
        self.setLayout(self.layout)

    def add_checkbox(self, name, path=None, layout_direction=QBoxLayout.LeftToRight):
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