from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

import src.variables as var
from src.data import *

from src.ui_componentwindow import Ui_ComponentWindow

from src.item import *

class NewTab(QDialog):
    def __init__(self, parent, components):
        super(NewTab, self).__init__(parent)
        uic.loadUi(os.path.join(var.BASE_PATH,'ui','newtab.ui'), self)
        self.setWindowTitle("New tab")
        
        for item in components:
            self.comboSubcomp.addItem(item)
        
        self.lineTabName.returnPressed.connect(self.click_ok)
        self.pushOk.clicked.connect(self.click_ok)
        self.pushCancel.clicked.connect(self.click_cancel)
        self.show()
        
    def click_ok(self):
        self.subcomp = self.comboSubcomp.currentText()
        self.tabname = self.lineTabName.text()
        if self.lineTabName.text() == "":
            QMessageBox.warning(self, "Warning", "Please, Write the new tab name")
            return
        self.accept()
        
    def click_cancel(self):
        self.reject()
        
    def return_para(self):
        return super().exec_()

class ComponentWindow(QDialog, Ui_ComponentWindow):
    def __init__(self, parent, fname=None, modify_component=False):
        super(ComponentWindow, self).__init__(parent)
        self.setupUi(self)

        self.template = Component(var.G_NOZZLE_TYPE)
        self.modify_component = modify_component
        self.fname = fname
        if self.fname is not None:
            self.preload()

        self.set_action()
        self.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.click_cancel(event)

    def closeEvent(self, event):
        self.click_cancel(event)
        
    def set_action(self):
        # Import
        self.pushImport.clicked.connect(self.import_component)
        self.pushImportClear.clicked.connect(self.import_clear)
        # Element
        ### LineEdit
        self.lineOutput.returnPressed.connect(lambda: self.set_name(self.lineOutput.text()))
        self.lineOutput.textChanged.connect(lambda: self.set_name(self.lineOutput.text()))
        self.lineCtype.returnPressed.connect(lambda: self.set_ctype(self.lineCtype.text()))
        self.lineCtype.textChanged.connect(lambda: self.set_ctype(self.lineCtype.text()))
        self.lineNewParaName.returnPressed.connect(self.add_element)
        self.lineNewParaValue.returnPressed.connect(self.add_element)
        self.lineName.returnPressed.connect(lambda: self.change_compname(self.lineName.text()))
        ### Button
        self.pushAdd.clicked.connect(self.add_element)
        self.pushClearVals.clicked.connect(self.clear_elements)
        self.pushChangeName.clicked.connect(lambda: self.change_compname(self.lineName.text()))
        self.pushChangeSubname.clicked.connect(lambda:  self.change_subname(self.lineSubname.text()))
        self.pushAppend.clicked.connect(self.append_component)
        self.pushAppendAll.clicked.connect(lambda: self.append_component(save_all=True))
        self.pushDeleteTab.clicked.connect(self.delete_subcomp)
        self.pushClearAll.clicked.connect(self.clear_all)
        self.pushMake.clicked.connect(self.click_make)
        self.pushClearPrev.clicked.connect(self.clear_preview)
        self.pushCancel.clicked.connect(self.click_cancel)
        ### Combo
        self.comboComp.addItem('Select')
        self.comboComp.addItem('New')
        self.comboComp.addItem("Load")
        self.comboComp.insertSeparator(3)
        for key in self.template.component_list().keys():
            self.comboComp.addItem(key)
        self.comboComp.currentTextChanged.connect(lambda: self.new_template(self.comboComp.currentText()))
        ### Element tab
        self.tabAddBtn = QToolButton()
        self.tabComp.setCornerWidget(self.tabAddBtn, Qt.TopRightCorner)
        self.tabAddBtn.setAutoRaise(True)
        self.tabAddBtn.setIcon(QIcon(os.path.join(var.BASE_PATH,"icons/new.png")))
        self.tabAddBtn.clicked.connect(self.add_subcomponent)

    def set_name(self, text):
        self.template.name = text

    def set_ctype(self, text):
        self.template.ctype = text

    def draw_import_widget(self, fname):
        lst = fname.split('/')
        name = lst[-1]
        path = '/'.join(i for i in lst)

        witem = QListWidgetItem(self.listImport)
        item = Item()
        item.add_checkbox(name, path=path, layout_direction=QBoxLayout.TopToBottom)
        if item.checkbox.isChecked():
            self.add_file(path, item.checkbox)
        item.checkbox.stateChanged.connect(lambda: self.add_file(path, item.checkbox))
        self.listImport.setItemWidget(witem, item)
        self.listImport.addItem(witem)
        witem.setSizeHint(item.sizeHint())
        self.update_preview()

    def add_file(self, path, checkbox):
        if checkbox.isChecked():
            self.template.modify_file(path)
        else:
            self.template.modify_file(path, delete=True)
        self.update_preview()

    def import_component(self):
        fname = QFileDialog.getOpenFileName(self, 'Import file', os.path.join(var.BASE_PATH, 'data/components'), 
            selectedFilter = var.G_TEXT_EXTENSION[0], filter='\n'.join(i for i in var.G_TEXT_EXTENSION))[0]
        if fname == "": return
        self.draw_import_widget(fname)

    def import_clear(self):
        for f in self.template.imported:
            self.template.modify_file(f, delete=True)
        self.listImport.clear()
        self.update_preview()

    def draw_para_widget(self, tabname, tabidx=-999):
        listPara = QListWidget()
        listPara.setContextMenuPolicy(Qt.ActionsContextMenu)
        
        actions = {"Modify":self.modify_element, "Delete":self.delete_element}
        for key, value in actions.items():
            action = QAction(key, listPara)
            action.triggered.connect(value)
            listPara.addAction(action)
        listPara.itemDoubleClicked.connect(self.modify_element)

        paras = [i for i in self.template.subcomponent[tabname].parameters]
        for para in paras:
            name = f'{para.vtype}:{para.category}/{para.directory}/{para.name}'
            witem = QListWidgetItem(listPara)
            item = Item()
            item.add_lineedit(name, para.value)
            item.lineValue.textChanged.connect(lambda: self.modify_element(True))
            item.lineValue.returnPressed.connect(lambda: self.modify_element(True))
            listPara.setItemWidget(witem, item)
            listPara.addItem(witem)
            witem.setSizeHint(item.sizeHint())
        if not tabidx < 0:
            index = self.tabComp.insertTab(tabidx, listPara, tabname)
        else:
            index = self.tabComp.addTab(listPara, tabname)
        return index

    def new_template(self, item):
        if item == '' or item == 'Select':
            return
        self.tabComp.clear()
        self.template = Component(var.G_NOZZLE_TYPE)
        if item == "New":
            self.clear_all()
            self.template.name = ''
            self.template.ctype = ''
        elif item == "Load":
            fname = QFileDialog.getOpenFileName(self, 'Load', os.path.join(var.BASE_PATH, 'data/components'),
                selectedFilter = var.G_TEXT_EXTENSION[0], filter='\n'.join(i for i in var.G_TEXT_EXTENSION))[0]
            if fname == '': 
                self.comboComp.setCurrentIndex(0)
                return
            self.listImport.clear()
            self.template.load(fname=fname)
        else:
            dirname = os.path.join(var.BASE_PATH, 'data/components', self.comboComp.currentText())
            self.template.load(fname=dirname)
        
        for i in range(len(self.template.imported)):
            self.draw_import_widget(fname=self.template.imported[i])
        tabs = [i.name for i in self.template.subcomponent.values()]
        for tab in tabs:
            self.draw_para_widget(tabname=tab)

        self.lineOutput.setText(self.template.name)
        self.lineCtype.setText(self.template.ctype)
        if item == "Load":
            self.append_component(save_all=True)
        self.update_preview()
        self.comboComp.setCurrentIndex(0)

    def add_subcomponent(self):
        if not self.comboComp.currentText() == "Load":
            newtab = NewTab(self, self.template.component_list()[self.template.ctype])
        else:
            newtab = NewTab(self, [])
        r = newtab.return_para()
        if r:
            subcomp = newtab.comboSubcomp.currentText()
            tabname = newtab.lineTabName.text()
            fname = os.path.join(self.template.ctype, subcomp+'.tps')
            self.template.load(fname=fname, add=tabname)
            index = self.draw_para_widget(tabname=tabname)
            self.tabComp.setCurrentIndex(index)
        self.update_preview()

    def change_compname(self, name):
        self.template.modify_name(self.template.name, name)
        self.lineOutput.setText(self.template.name)
        self.tabComp.clear()
        tabs = [i.name for i in self.template.subcomponent.values()]
        for tab in tabs:
            self.draw_para_widget(tabname=tab)
        self.update_preview()

    def delete_subcomp(self):
        tabname = self.tabComp.tabText(self.tabComp.currentIndex())
        self.template.modify_subcomponent(subname=tabname, paras=None, delete=True)
        self.tabComp.removeTab(self.tabComp.currentIndex())

    def change_subname(self, name):
        idx = self.tabComp.currentIndex()
        subcomp = self.tabComp.tabText(idx)
        if not self.template.subcomponent[subcomp].parameters[0].directory:
            return
        self.template.modify_subname(subcomp, name)
        self.tabComp.removeTab(idx)
        self.draw_para_widget(tabname=name, tabidx = idx)
        self.update_preview()

    def add_element(self):
        widget = self.tabComp.currentWidget()
        subcomp = self.tabComp.tabText(self.tabComp.currentIndex())
        name = self.lineNewParaName.text()
        value = self.lineNewParaValue.text()
        if name == "": return
        self.template.modify_parameter(subcomp, {name:value})
        
        witem = QListWidgetItem(widget)
        item = Item()
        item.add_lineedit(name, value)
        idx = widget.count() - 1
        widget.setItemWidget(witem, item)
        widget.addItem(witem)
        witem.setSizeHint(item.sizeHint())
        self.update_preview()
  
    def delete_element(self):
        widget = self.tabComp.currentWidget()
        subcomp = self.tabComp.tabText(self.tabComp.currentIndex())
        item = widget.itemWidget(widget.currentItem())
        name = item.label.text()
        value = item.lineValue.text()
        self.template.modify_parameter(subcomp,{name:value},delete=True)
        widget.takeItem(widget.currentRow())
        self.update_preview()
        
    def modify_element(self,direct=False):
        # FIXME
        # widget 클릭 안하고 lineEdit 건드려서 엔터쳐서 이게 돌아가면 아이템 NoneType 되서 터짐.... 
        widget = self.tabComp.currentWidget()
        idx = widget.currentRow()
        item = widget.itemWidget(widget.item(idx))
        if item is None: return
        subcomp = self.tabComp.tabText(self.tabComp.currentIndex())
        name = self.template.subcomponent[subcomp].parameters[idx].fullname()
        value = self.template.subcomponent[subcomp].parameters[idx].value
        if not direct:
            modify = ModifyParameter(self,name,value)
            r = modify.return_para()
            if r:
                name = modify.name
                value = modify.value
        else:
            value = item.lineValue.text()
        self.template.modify_parameter(subcomp, {name:value})
        item.lineValue.setText(value)
        self.update_preview()
            
    def append_component(self, save_all=False):
        if save_all:
            for sub in self.template.subcomponent.values():
                sub.draw = True
                for para in sub.parameters:
                    para.draw = True
        else:
            subcomp = self.tabComp.tabText(self.tabComp.currentIndex())
            self.template.subcomponent[subcomp].draw = True
            widget = self.tabComp.currentWidget()
            for para in self.template.subcomponent[subcomp].parameters:
                para.draw = True
        self.update_preview()

    def update_preview(self):
        self.textPreview.setText(self.template.fulltext())
        
    def clear_all(self):
        self.template = Component(var.G_NOZZLE_TYPE)
        self.lineOutput.clear()
        self.listImport.clear()
        self.tabComp.clear()
        self.update_preview()

    def clear_elements(self):
        subcomp = self.tabComp.tabText(self.tabComp.currentIndex())
        widget = self.tabComp.currentWidget()
        for idx in range(widget.count()):
            self.template.subcomponent[subcomp].parameters[idx].value = ''
            widget.itemWidget(widget.item(idx)).lineValue.setText('')
        self.update_preview()
        
    def clear_preview(self):
        for sub in self.template.subcomponent.values():
            sub.draw = False
            for para in sub.parameters:
                para.draw = False
        self.update_preview()

    def preload(self):
        if type(self.fname) == int:
            if self.modify_component:
                self.template = var.G_COMPONENT[self.fname]
            else:
                self.template = var.G_TEMPLATE[self.fname]
        elif type(self.fname) == str:
            self.template.load(self.fname)
        else:
            return

        for i in range(len(self.template.imported)):
            self.draw_import_widget(fname=self.template.imported[i])
        tabs = [i.name for i in self.template.subcomponent.values()]
        for tab in tabs:
            self.draw_para_widget(tabname=tab)

        self.lineOutput.setText(self.template.name)
        self.lineOutput.setReadOnly(True)
        self.lineCtype.setText(self.template.ctype)
        self.lineCtype.setReadOnly(True)
        self.update_preview()

    def click_make(self):
        if self.modify_component:
            var.G_COMPONENT[self.fname] = self.template
        else:
            var.G_TEMPLATE.append(self.template)
        self.accept()
        
    def click_cancel(self, event=None):
        reply = QMessageBox.question(self, "Message", "Are you sure to cancel?",
          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.reject()
        else:
            if event is None or type(event) == bool:
                return
            else:
                event.ignore()
        
    def return_para(self):
        return super().exec_()
