
from PySide6.QtWidgets import *

from src.ui_modificationwindow import Ui_ModificationWindow

class ModifyParameter(QDialog, Ui_ModificationWindow):
    def __init__(self, parent, name="", value="", label_name="Name", label_value="Value"):
        super(ModifyParameter, self).__init__(parent)
        self.setupUi(self)
        self.name = name
        self.value = value
        self.labelName.setText(label_name)
        self.labelValue.setText(label_value)
        
        self.lineName.setText(self.name)
        self.lineValue.setText(self.value)
        self.lineName.returnPressed.connect(self.set_name)
        self.lineValue.returnPressed.connect(self.set_value)
        
        self.pushOk.clicked.connect(self.click_ok)
        self.pushCancel.clicked.connect(self.click_cancel)
        self.show()
        
    def set_name(self):
        self.name = self.lineName.text()
    
    def set_value(self):
        self.value = self.lineValue.text()
    
    def click_ok(self):
        self.set_name()
        self.set_value()
        self.accept()
        
    def click_cancel(self):
        self.reject()
    
    def return_para(self):
        return super().exec()