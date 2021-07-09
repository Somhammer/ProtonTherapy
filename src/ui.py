import os, sys
import time
import datetime
import subprocess
import yaml
import pydicom as dicom
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from functools import partial
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

import data
import config as cfg

base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(base_path)

form_class = uic.loadUiType(os.path.join(base_path,'ui','main.ui'))[0]

g_text_extension = ["Text files (*.txt *.tps)", "Data files (*.dat)"]
g_excel_extension = ["Excel files (*.xls *.xlms)"]

g_outdir = os.path.join(base_path, 'prod', datetime.date.today().strftime('%y%m%d'))
g_nozzle_type = None
# Solid component: Below components are not changed for each beam sequences.
g_template = []
g_component = [] # nozzle
g_patient = data.Patient()
g_convalgo = {
  'File':[None,"str"],
  'Number of Beams':[None, "int"],
  '1st Scatterer':[None, "int"],
  '2nd Scatterer':[None, "int"],
  'Modulator':[None, "int"],
  'Stop Position':[None, "int"],
  'Energy':[None, "float"],
  'BCM':[None, "str"],
  'BWT':[None, "str"]
}
g_phase = {}
g_order = {}
g_filter = []
# Liquid component: Below components are changed for each beam sequences.

def setup_convalgo(fname):
    if fname == "": return
                
    lst = fname.split('/')
    name = lst[-1]
    path = '/'.join(i for i in lst[:-1])
    import getconvalgo as gc
    convalgo = gc.GetParaFromConvAlgo(path, name)
    g_convalgo['File'][0] = fname
    g_convalgo['Number of Beams'][0] = len(convalgo.fscatterer)
    g_convalgo['1st Scatterer'][0] = convalgo.fscatterer
    g_convalgo['2nd Scatterer'][0] = convalgo.sscatterer
    g_convalgo['Modulator'][0] = convalgo.modulator
    g_convalgo['Stop Position'][0] = convalgo.stop
    g_convalgo['Energy'][0] = convalgo.energy
    g_convalgo['BCM'][0] = convalgo.bcm
    g_convalgo['BWT'][0] = convalgo.bwt

class Item(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
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
        if self.label.text().lower() == 'convalgo':
            fname = QFileDialog.getOpenFileName(self, initialFilter = g_excel_extension[0], filter='\n'.join(i for i in g_excel_extension))[0]
        if self.label.text().lower() == 'patient':
            fname = QFileDialog.getExistingDirectory(self, "Select Patient CT directory")

        self.lineValue.setText(fname)
        self.lineValue.setReadOnly(True)

class ModifyParameter(QDialog):
    def __init__(self, parent, name="", value="", label_name="Name", label_value="Value"):
        super(ModifyParameter, self).__init__(parent)
        uic.loadUi(os.path.join(base_path,'ui','modification.ui'), self)
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
        return super().exec_()

class ComponentWindow(QDialog):
    def __init__(self, parent, fname=None, modify_component=False):
        super(ComponentWindow, self).__init__(parent)
        uic.loadUi(os.path.join(base_path,'ui','component.ui'), self)

        self.template = data.Component(g_nozzle_type)
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
        self.tabAddBtn.setIcon(QIcon("../icons/new.png"))
        self.tabAddBtn.clicked.connect(self.add_subcomponent)

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
        fname = QFileDialog.getOpenFileName(self, 'Import file', os.path.join(base_path, 'data/components'), 
            initialFilter = g_text_extension[0], filter='\n'.join(i for i in g_text_extension))[0]
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
        self.template = data.Component(g_nozzle_type)
        if item == "New":
            self.clear_all()
            self.template.name = ''
            self.template.ctype = ''
        elif item == "Load":
            fname = QFileDialog.getOpenFileName(self, 'Load', os.path.join(base_path, 'data/components'),
                initialFilter = g_text_extension[0], filter='\n'.join(i for i in g_text_extension))[0]
            if fname == '': 
                self.comboComp.setCurrentIndex(0)
                return
            self.listImport.clear()
            self.template.load(fname=fname)
        else:
            dirname = os.path.join(base_path, 'data/components', self.comboComp.currentText())
            self.template.load(fname=dirname)
        
        for i in range(len(self.template.imported)):
            self.draw_import_widget(fname=self.template.imported[i])
        tabs = [i.name for i in self.template.subcomponent.values()]
        for tab in tabs:
            self.draw_para_widget(tabname=tab)

        self.lineOutput.setText(self.template.name)
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
            #fname = os.path.join(base_path,'data/components',self.comboComp.currentText(),subcomp+'.tps')
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
        self.template = data.Component(g_nozzle_type)
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
                self.template = g_component[self.fname]
            else:
                self.template = g_template[self.fname]
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
        self.update_preview()

    def click_make(self):
        if self.modify_component:
            g_component[self.fname] = self.template
        else:
            g_template.append(self.template)
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

class NewTab(QDialog):
    def __init__(self, parent, components):
        super(NewTab, self).__init__(parent)
        uic.loadUi(os.path.join(base_path,'ui','newtab.ui'), self)
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

class PatientWindow(QDialog):
    def __init__(self, parent, current=None):
        super(PatientWindow, self).__init__(parent)
        uic.loadUi(os.path.join(base_path,'ui','patient.ui'), self)

        if current is None:
            self.current = ""
        else:
            self.current = current
        
        self.fig = plt.figure()
        self.widgetCanvas = FigureCanvas(self.fig)
        self.gridLayout.addWidget(self.widgetCanvas)
        self.set_action()
        if os.path.exists(os.path.join(g_patient.directory, self.current)):
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
        self.lineDir.setText(g_patient.directory)
        current_idx = 0
        for idx, item in enumerate(g_patient.CT):
            if item == self.current: current_idx = idx
            self.comboFiles.addItem(item)
        self.comboFiles.setCurrentIndex(current_idx)
        self.comboFiles.currentTextChanged.connect(lambda: self.show_image(self.comboFiles.currentText()))
        self.pushOpen.clicked.connect(self.open_directory)
        self.pushPrev.clicked.connect(lambda: self.change_image(self.pushPrev))
        self.pushNext.clicked.connect(lambda: self.change_image(self.pushNext))
        self.pushClose.clicked.connect(self.click_close)
        
    def show_image(self, ct):
        self.fig.clear()
        CT = dicom.dcmread(os.path.join(g_patient.directory, ct))
        ax = self.fig.add_subplot(111)
        ax.imshow(CT.pixel_array, cmap=plt.cm.bone)
        self.widgetCanvas.draw()
    
    def open_directory(self):
        newdir = ""
        newdir = QFileDialog.getExistingDirectory(self, "Select Patient CT directory")
        if newdir == g_patient.directory or newdir == "": return
        else:
            g_patient.patient_setup(newdir)
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

class SimulationWindow(QDialog):
    def __init__(self, parent):
        super(SimulationWindow, self).__init__(parent)
        uic.loadUi(os.path.join(base_path,'ui','simulation.ui'), self)

        self.instance = None
        self.templates = {}
        self.components = {}
        self.set_action()
        self.show()

    def set_action(self):
        self.pushLoad.clicked.connect(lambda: self.load_cfg(push=True))

        self.pushSave.clicked.connect(self.save_cfg)
        self.pushMake.clicked.connect(self.write_output)
        self.pushClear.clicked.connect(self.write_output)
        self.pushCancel.clicked.connect(self.click_cancel)
        self.pushOpenFile.clicked.connect(self.add_import)
        self.pushAddNewPara.clicked.connect(self.add_element)
        self.pushAppendComp.clicked.connect(self.add_template)
        #self.pushClearComp.clicked.connect()
        
        macros = ['NewSimulation', 'DoseSimulation']
        self.comboMacro.addItem('Select')
        self.comboMacro.addItem('New')
        self.comboMacro.addItem('Open')
        self.comboMacro.insertSeparator(3)
        for macro in macros:
            self.comboMacro.addItem(macro)
        self.comboMacro.currentTextChanged.connect(self.open_macro)

        self.comboComp.addItem('Select')
        self.comboComp.addItem('New')
        self.comboComp.insertSeparator(3)
        temp = data.Component(btype=g_nozzle_type, phase=True)
        for key in temp.component_list().keys():
            self.comboComp.addItem(key)
        self.comboComp.currentTextChanged.connect(lambda: self.new_template(self.comboComp.currentText()))

        self.listTemplates.setContextMenuPolicy(Qt.ActionsContextMenu)
        actionAdd = QAction("Add", self.listTemplates)
        actionAdd.triggered.connect(self.add_component)        
        self.listTemplates.addAction(actionAdd)
        self.listTemplates.itemDoubleClicked.connect(self.add_component)

    def open_macro(self):
        if self.comboMacro.currentText() == 'Select': return

        if self.comboMacro.currentText() == 'Open':
            fname = QFileDialog.getOpenFileName(self, filter = "Python files (*.py)")[0]
            if fname == "": return
        elif self.comboMacro.currentText() == 'New':
            fname = 'simulation.py'
        else:
            fname = f'{self.comboMacro.currentText().lower()}.py'

        import config as cfg
        proton = cfg.Proton()
        proton.load(fname)
        cls_name = proton.name(fname)
        self.instance = proton.process(proton.name(fname))(outdir=g_outdir, nozzle=g_nozzle_type, patient=g_patient)
        requirements = self.instance.requirements
        for key, value in requirements.items():
            witem = QListWidgetItem(self.listRequirement)
            item = Item()
            if any(key.lower() == i.lower() for i in ['convalgo', 'patient']):
                item.add_lineedit(key, value[0], readonly=True, makebtn=True)
            else:
                item.add_lineedit(key, value[0])
            self.listRequirement.setItemWidget(witem, item)
            self.listRequirement.addItem(witem)
            witem.setSizeHint(item.sizeHint())
            item.lineValue.textChanged.connect(self.set_requirement)
            item.lineValue.returnPressed.connect(self.set_requirement)

        self.comboComp.insertSeparator(self.comboComp.count())
        for key in self.instance.keys:
            self.comboComp.addItem(key)

        for key in self.instance.keys:
            listImport = QListWidget()
            listImport.setContextMenuPolicy(Qt.ActionsContextMenu)
            for component in g_component:
                witem = QListWidgetItem(listImport)
                item = Item()
                item.add_checkbox(component.name, path=component.outname)
                listImport.setItemWidget(witem, item)
                listImport.addItem(witem)
                witem.setSizeHint(item.sizeHint())
            self.tabImport.addTab(listImport, key)

        for key in self.instance.keys:
            listComponent = QListWidget()
            listComponent.setContextMenuPolicy(Qt.ActionsContextMenu)
            actionDel = QAction("Delete", listComponent)
            actionDel.triggered.connect(self.delete_component)
            listComponent.addAction(actionDel)
            listComponent.itemDoubleClicked.connect(self.delete_component)
            self.tabComponents.addTab(listComponent, key)

        self.load_cfg(fname)

    def clear_all(self):
        self.templates = {}
        self.components = {}

    def save_cfg(self):
        if self.comboMacro.currentText() == 'Select': return

        fname = QFileDialog.getSaveFileName(self, 'Save', os.path.join(base_path, 'plugin'), filter="Nozzle files (*.nzl)")[0]
        if not fname.endswith('.nzl'):
            fname = fname.split('.')[0] + '.nzl'
        fout = open(fname, 'w')
        fout.write(f"Template: \n")
        for name, component in self.components.items():
            for subcomp in component.subcomponent.values():
                for para in subcomp.parameters: para.draw = True
            fulltext = component.fulltext().split('\n')
            for idx, text in enumerate(fulltext):
                fulltext[idx] = '      ' + text
            fulltext = "\n\n".join(t for t in fulltext)
            fout.write(f"  {name}:\n    Type: {component.ctype}\n    Text: >\n{fulltext}\n\n")

        tmp_dict = {i:[] for i in self.instance.keys}
        for idx in range(self.tabComponents.count()):
            name = self.tabComponents.tabText(idx)
            widget = self.tabComponents.widget(idx)
            for idx2 in range(widget.count()):
                item = widget.itemWidget(widget.item(idx2))
                text = item.label.text()
                tmp_dict[name].append(text)
        
        for key, values in tmp_dict.items():
            fout.write(f"{key}:\n")
            for value in values:
                fout.write(f'  - "{value}"\n')
        fout.close()

    def load_cfg(self, fname=None, push=False):
        if self.comboMacro.currentText() == 'Select': return
        if not push and self.comboMacro.currentText() == "New": return
        if fname is None and not push: return
        if push:
            fname = QFileDialog.getOpenFileName(self, 'Load Phase')[0]

        self.clear_all()
        with open(os.path.join(base_path, 'plugin', fname.replace('.py', '.nzl')), 'r') as f:
            cfg = yaml.load(f, Loader=yaml.FullLoader)
        for name, comp_info in cfg['Template'].items():
            template = data.Component(btype=g_nozzle_type, phase=True)
            template.load(comp_info['Text'], load=True)
            template.name = name
            template.ctype = comp_info['Type']
            self.components[template.name] = template

            witem = QListWidgetItem(self.listTemplates)
            item = Item()
            item.add_label(name=f'{template.ctype} - {name}')
            self.listTemplates.setItemWidget(witem, item)
            self.listTemplates.addItem(witem)
            witem.setSizeHint(item.sizeHint())

        for idx in range(self.tabComponents.count()):
            tabname = self.tabComponents.tabText(idx)
            widget = self.tabComponents.widget(idx)
            if not tabname in cfg: continue
            for text in cfg[tabname]:
                witem = QListWidgetItem(widget)
                item = Item()
                item.add_label(text)
                widget.setItemWidget(witem, item)
                widget.addItem(witem)
                witem.setSizeHint(item.sizeHint())

    def set_requirement(self):
        for idx in range(len(self.listRequirement)):
            item = self.listRequirement.itemWidget(self.listRequirement.item(idx))
            vtype = item.label.text()
            vari = None
            if vtype.lower() == "convalgo":
                setup_convalgo(fname=item.lineValue.text())
                vname = g_convalgo['File']
                vari = g_convalgo
            elif vtype.lower() == "patient":
                g_patient.patient_setup(item.lineValue.text())
                vname = g_patient.directory
                vari = g_patient
            else:
                vname = item.lineValue.text()
                vari = item.lineValue.text()
            self.instance.set_requirement(vtype=vtype, vname=vname, vari=vari)
        
    def add_import(self):
        if self.comboMacro.currentText() == 'Select': return

        fname = QFileDialog.getOpenFileName(self, "Import",  os.path.join(base_path,'data/components'), initialFilter = g_text_extension[0], filter='\n'.join(i for i in g_text_extension))[0]
        widget = self.tabImport.currentWidget()
        witem = QListWidgetItem(widget)
        item = Item()
        item.add_checkbox(fname.split('/')[-1].replace('.tps',''), path=fname)
        widget.setItemWidget(witem, item)
        widget.addItem(witem)
        witem.setSizeHint(item.sizeHint())

    def new_template(self, cname):
        if self.comboMacro.currentText() == 'Select': return

        if cname == '' or cname == 'Select':
            return
        self.tabComp.clear()
        if cname == "New":
            self.tabComp.clear()
            template = data.Component(btype=g_nozzle_type)
            template.name = ''
            template.ctype = ''
            modify = ModifyParameter(parent=self, name=template.name, value=template.ctype, label_name="Name", label_value="Type")
            r = modify.return_para()
            if r:
                template.name = modify.name
                template.ctype = modify.value
            listPara = QListWidget()
            listPara.setContextMenuPolicy(Qt.ActionsContextMenu)
        
            actions = {"Modify":self.modify_element, "Delete":self.delete_element}
            for key, value in actions.items():
                action = QAction(key, listPara)
                action.triggered.connect(value)
                listPara.addAction(action)
            listPara.itemDoubleClicked.connect(lambda: self.modify_element())
            self.tabComp.addTab(listPara, template.name)
            self.templates[template.name] = template
        elif any(cname == i for i in self.instance.keys):
            self.tabComp.clear()
            template = data.Component(btype=g_nozzle_type)
            template.name = cname
            template.ctype = cname
            listPara = QListWidget()
            listPara.setContextMenuPolicy(Qt.ActionsContextMenu)
        
            actions = {"Modify":self.modify_element, "Delete":self.delete_element}
            for key, value in actions.items():
                action = QAction(key, listPara)
                action.triggered.connect(value)
                listPara.addAction(action)
            listPara.itemDoubleClicked.connect(lambda: self.modify_element())
            self.tabComp.addTab(listPara, template.name)
            self.templates[template.name] = template
        else:
            dirname = os.path.join(base_path, 'data/components', self.comboComp.currentText())
            for f in os.listdir(dirname):
                template = data.Component(btype=g_nozzle_type, phase=True)
                template.load(fname=os.path.join(dirname, f))
                template.ctype = cname
                listPara = QListWidget()
                listPara.setContextMenuPolicy(Qt.ActionsContextMenu)
        
                actions = {"Modify":self.modify_element, "Delete":self.delete_element}

                for key, value in actions.items():
                    action = QAction(key, listPara)
                    action.triggered.connect(value)
                    listPara.addAction(action)
                listPara.itemDoubleClicked.connect(lambda: self.modify_element())

                paras = [i for i in template.subcomponent['Basis'].parameters]
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
            
                self.tabComp.addTab(listPara, template.name)
                self.templates[template.name] = template

    def add_template(self):
        name = self.tabComp.tabText(self.tabComp.currentIndex())
        witem = QListWidgetItem(self.listTemplates)
        item = Item()
        item.add_label(name=f'{self.templates[name].ctype} - {name}')
        self.listTemplates.setItemWidget(witem, item)
        self.listTemplates.addItem(witem)
        witem.setSizeHint(item.sizeHint())
        self.components[self.templates[name].name] = self.templates[name]

    def add_component(self):
        widget = self.tabComponents.currentWidget()
        witem = QListWidgetItem(widget)
        item = Item()
        i = self.listTemplates.itemWidget(self.listTemplates.currentItem())
        item.add_label(i.label.text())
        widget.setItemWidget(witem, item)
        widget.addItem(witem)
        witem.setSizeHint(item.sizeHint())
    
    def delete_component(self):
        widget = self.tabComponents.currentWidget()
        item = widget.takeItem(widget.currentRow())

    def add_element(self):
        widget = self.tabComp.currentWidget()
        subcomp = self.tabComp.tabText(self.tabComp.currentIndex())
        name = self.lineNewParaName.text()
        value = self.lineNewParaValue.text()
        if name == "": return
        self.templates[subcomp].modify_parameter(subcomp, {name:value})
        
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
        self.templates[subcomp].modify_parameter('Basis',{name:value},delete=True)
        widget.takeItem(widget.currentRow())
        
    def modify_element(self,direct=False):
        # FIXME
        # widget 클릭 안하고 lineEdit 건드려서 엔터쳐서 이게 돌아가면 아이템 NoneType 되서 터짐.... 
        widget = self.tabComp.currentWidget()
        idx = widget.currentRow()
        item = widget.itemWidget(widget.item(idx))
        if item is None: return
        subcomp = self.tabComp.tabText(self.tabComp.currentIndex())
        name = self.templates[subcomp].subcomponent['Basis'].parameters[idx].fullname()
        value = self.templates[subcomp].subcomponent['Basis'].parameters[idx].value
        if not direct:
            modify = ModifyParameter(self,name,value)
            r = modify.return_para()
            if r:
                name = modify.name
                value = modify.value
        else:
            value = item.lineValue.text()
        self.templates[subcomp].modify_parameter('Basis', {name:value})
        item.lineValue.setText(value)
        
    def write_output(self):
        if not self.instance.is_workable():
            QMessageBox.warning(self, "Message", "Please, Fill requirements", QMessageBox.Ok)
            return
            
        tmp_dict = {i:[] for i in self.instance.keys}

        for idx in range(self.tabImport.count()):
            name = self.tabImport.tabText(idx)
            widget = self.tabImport.widget(idx)
            tmp = []
            for idx2 in range(widget.count()):
                item = widget.itemWidget(widget.item(idx2))
                if item.checkbox.isChecked():
                    text = item.label.text()[1:-1]
                    tmp.append(text)
            self.instance.set_import_files(name, tmp)
        
            widget = self.tabComponents.widget(idx)
            for idx2 in range(widget.count()):
                item = widget.itemWidget(widget.item(idx2))
                text = item.label.text()
                tmp = text.replace(' - ','-').split('-')
                tmp = (tmp[0], tmp[1])
                tmp_dict[name].append(tmp)

        self.instance.set_templates(tmp_dict, self.components)
        global g_phase, g_filter, g_order
        g_phase, g_filter = self.instance.run()
        g_order = self.instance.order
        self.click_ok()

    def click_ok(self):
        self.accept()
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.click_cancel(event)

    def closeEvent(self, event):
        self.click_cancel(event)

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

class RunWindow(QDialog):
    def __init__(self, parent):
        super(RunWindow, self).__init__(parent)
        uic.loadUi(os.path.join(base_path,'ui','run.ui'), self)

        self.topas = cfg.Topas()
        self.idict = {} # ibeam:{order:input}

        self.set_action()
        self.show()
        self.run()

    def set_action(self):
        self.checkInit.clicked.connect(lambda: self.undo(self.checkInit))
        self.checkInput.clicked.connect(lambda: self.undo(self.checkInput))
        self.checkTopasRun.clicked.connect(lambda: self.undo(self.checkTopasRun))
        self.checkPost.clicked.connect(lambda: self.undo(self.checkPost))
        
        self.pushResubmit.clicked.connect(self.resubmit_process)
        self.pushSaveLog.clicked.connect(self.save_log)
    
    def run(self):
        self.initialize()
        self.generate_input()
        #self.execute_topas()
        #self.do_postprocess()

    def undo(self, checkbox):
        if checkbox.isCheckable():
            checkbox.setChecked(True)

    def initialize(self):
        self.textLog.append("...Initialize topas")
        try:
            self.topas.set_path(g_outdir)
            self.checkInit.setCheckable(True)
            self.checkInit.setChecked(True)
            self.textLog.append("Parameter setting is success.")
        except:
            self.textLog.append("Parameter setting is failed.")
            
    def generate_input(self):
        self.textLog.append("...Generate topas input files")
        try:
            lst = []
            if g_nozzle_type == 'scanning': lst = ['nozzle', 'parallels']
            else: lst = ['nozzle', 'aperture', 'compensator', 'parallels']
            for i in lst:
                if not os.path.exists(os.path.join(g_outdir,i)):
                    os.makedirs(os.path.join(g_outdir,i))

            self.textLog.append("......Generate topas files")
            for component in g_component:
                f = open(os.path.join(component.outname),'w')
                f.write(component.fulltext())

            self.textLog.append("......Generate filter files")
            for fil in g_filter:
                f = open(os.path.join(g_outdir, fil['OutName']), 'w')
                f.write(fil['RawText'])

            self.textLog.append("......Generate phase files")
            for key, values in g_phase.items():
                if key.lower() != 'patient': continue
                for value in values:
                    f = open(os.path.join(value.outname), 'w')
                    f.write(value.fulltext())
                del g_phase[key]
                 
            temp = g_phase.keys()
            self.idict = {i:{order:None for order in g_order.values()} for i in temp}
            for key, phases in g_phase.items():
                order = g_order[key]
                for ibeam, phase in enumerate(phases):
                    f = open(os.path.join(phase.outname), 'w')
                    f.write(phase.fulltext())
                    self.idict[key][ibeam] = phase.outname
                    for i in phase.imported:
                        name = i.split('/')[-1]
                        if any(name in j for j in os.listdir(os.path.join(g_outdir,'nozzle'))): continue
                        for (path, directories, files) in os.walk(base_path, 'data/components'):
                            for f in files:
                                if f == name:
                                    cmd = ['cp', os.path.join(path, f), os.path.join(g_outdir, 'nozzle', f)]
                                    subprocess.call(cmd)

            self.checkInput.setCheckable(True)
            self.checkInput.setChecked(True)
            self.textLog.append("Topas input files are generated.")
        except:
            self.textLog.append("Generation is failed.")
            
    def execute_topas(self):
        self.textLog.append("...Execute Topas")
        try:
            for ibeam in range(len(g_main[0])):
                self.topas.set_input(self.idict[ibeam])
                self.topas.run()
            self.checkTopasRun.setCheckable(True)
            self.checkTopasRun.setChecked(True)
            self.textLog.append("Simulation is success.")
        except:
            self.textLog.append("Simlation is failed.")

    def do_postprocess(self):
        self.textLog.append("...Do post process")
        try:
            self.checkPost.setCheckable(True)
            self.checkPost.setChecked(True)
            self.textLog.append("Success. All processes has been completed.")
        except:
            self.textLog.append("Post process is failed.")

    def resubmit_process(self):
        return
        
    def save_log(self):
        return
        
    def return_para(self):
        return super().exec_()

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.widgetNozzle = Painter()
        #self.painter = painter.Painter(self.widgetNozzle)
        self.comp_to_table_map = {}
        self.macros = []

        self.set_icons()
        self.set_layout()
        self.set_actions()

        self.show()

    def set_icons(self):
        # Remove this function when coding is completed.
        icon_dir = os.path.join(base_path,'icons')
        ncc = QIcon(os.path.join(icon_dir, 'ncc.png'))
        ext = QIcon(os.path.join(icon_dir, 'exit.png'))
        new = QIcon(os.path.join(icon_dir, 'new.png'))
        opn = QIcon(os.path.join(icon_dir, 'open.png'))
        save = QIcon(os.path.join(icon_dir, 'save.png'))
        write = QIcon(os.path.join(icon_dir, 'write.png'))
        delete = QIcon(os.path.join(icon_dir, 'delete.png'))
        view = QIcon(os.path.join(icon_dir, 'view.png'))
        run = QIcon(os.path.join(icon_dir, 'run.png'))
        
        self.setWindowIcon(QIcon(os.path.join(base_path,'icons/ncc.png')))
        self.actionFileNew.setIcon(new)
        self.actionFileOpen.setIcon(opn)
        self.actionFileSave.setIcon(save)
        self.actionExit.setIcon(ext)
        self.actionTempNew.setIcon(new)
        self.actionTempModify.setIcon(write)
        self.actionTempDelete.setIcon(delete)
        self.actionCompAdd.setIcon(new)
        self.actionCompModify.setIcon(write)
        self.actionCompDelete.setIcon(delete)
        self.actionPatientSetup.setIcon(opn)
        self.actionPatientView.setIcon(view)
        self.actionSimLoad.setIcon(opn)

    def set_layout(self):
        self.tableComp.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.gridLayout_2.addWidget(self.widgetNozzle,1,0)

        self.radioScattering = QRadioButton("Scattering")
        self.radioScanning = QRadioButton("Scanning")
        layoutNozzleMode = QHBoxLayout()
        layoutNozzleMode.addWidget(self.radioScattering)
        layoutNozzleMode.addWidget(self.radioScanning)
        self.groupNozzleMode.setLayout(layoutNozzleMode)

        layoutConvalgo = QGridLayout()
        self.conv_values = []
        for irow, text in enumerate(g_convalgo.keys()):
            label = QLabel(text)
            edit = QLineEdit()
            self.conv_values.append(edit)
            layoutConvalgo.addWidget(label, irow, 0)
            layoutConvalgo.addWidget(edit, irow, 1)
        self.groupConvalgo.setLayout(layoutConvalgo)

        self.linePatientDir.setReadOnly(True)
        self.lineRTP.setReadOnly(True)
        self.lineRTS.setReadOnly(True)
        self.lineRD.setReadOnly(True)
        self.lineMacro.setReadOnly(True)

    def set_actions(self):
        ### File
        self.actionFileNew.triggered.connect(self.new_simulation)
        self.actionFileOpen.triggered.connect(self.open_cfg)
        self.actionFileSave.triggered.connect(self.save_cfg)
        self.actionExit.triggered.connect(qApp.quit)
        ### Template
        self.actionTempNew.triggered.connect(self.new_template)
        #self.actionTempLoad.triggered.connect(self.load_template)
        self.actionTempModify.triggered.connect(self.modify_template)
        self.actionTempDelete.triggered.connect(self.delete_template)
        ### Component
        self.actionCompAdd.triggered.connect(self.add_component)
        self.actionCompModify.triggered.connect(self.modify_component)
        self.actionCompDelete.triggered.connect(self.delete_component)
        ### Patient
        self.actionPatientSetup.triggered.connect(self.patient_setup)
        self.actionPatientView.triggered.connect(self.patient_view)
        self.actionPatientConv.triggered.connect(self.load_convalgo)
        ### Simulation
        self.actionSimLoad.triggered.connect(self.simulation)
        ### Run
        self.actionRun = QAction(QIcon(os.path.join(base_path,'icons/run.png')), 'Run', self)
        self.actionRun.setShortcut('Ctrl+R')
        self.actionRun.setStatusTip('Run Topas simulation')
        self.actionRun.triggered.connect(self.run)

        # Toolbar
        self.toolBar.addAction(self.actionExit)
        self.toolBar.addSeparator()
        
        label = QLabel(" File: ")
        self.toolBar.addWidget(label)
        self.toolBar.addAction(self.actionFileNew)
        self.toolBar.addAction(self.actionFileOpen)
        self.toolBar.addAction(self.actionFileSave)
        self.toolBar.addSeparator()

        label = QLabel(" Template: ")
        self.toolBar.addWidget(label)
        self.toolBar.addAction(self.actionTempNew)
        self.toolBar.addAction(self.actionTempModify)
        self.toolBar.addAction(self.actionTempDelete)
        self.toolBar.addSeparator()
        
        label = QLabel(" Component: ")
        self.toolBar.addWidget(label)
        self.toolBar.addAction(self.actionCompAdd)
        self.toolBar.addAction(self.actionCompModify)
        self.toolBar.addAction(self.actionCompDelete)
        self.toolBar.addSeparator()

        label = QLabel(" Patient: ")
        self.toolBar.addWidget(label)
        self.toolBar.addAction(self.actionPatientSetup)
        self.toolBar.addAction(self.actionPatientView)
        self.toolBar.addSeparator()

        self.toolBar.addAction(self.actionPatientConv)
        self.toolBar.addSeparator()

        label = QLabel(" Simulation: ")
        self.toolBar.addWidget(label)
        self.toolBar.addAction(self.actionSimLoad)
        self.toolBar.addSeparator()

        self.toolBar.addAction(self.actionRun)
        self.toolBar.setIconSize(QSize(32,32))
        
        # Nozzle Mode
        self.radioScattering.clicked.connect(self.set_beam_mode)
        self.radioScanning.clicked.connect(self.set_beam_mode)

        # Template
        self.listTemplates.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.listTemplates.addAction(self.actionTempNew)
        self.listTemplates.addAction(self.actionTempModify)
        self.listTemplates.addAction(self.actionTempDelete)
        self.listTemplates.addAction(self.actionCompAdd)
        self.listTemplates.itemDoubleClicked.connect(self.add_component)

        # Component
        self.tableComp.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.tableComp.addAction(self.actionCompModify)
        self.tableComp.addAction(self.actionCompDelete)
        self.tableComp.itemDoubleClicked.connect(self.modify_component)
        
        # Patient
        self.listPatientCT.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.listPatientCT.addAction(self.actionPatientView)
        self.listPatientCT.itemDoubleClicked.connect(self.patient_view)
        
    # Functions
    def set_beam_mode(self):
        global g_nozzle_type
        if self.radioScattering.isChecked(): g_nozzle_type = "scattering"
        if self.radioScanning.isChecked(): g_nozzle_type = "scanning"

    def check_beam_mode(self):
        global g_nozzle_type
        if g_nozzle_type is None:
            QMessageBox.warning(self, "Warning", "Please, select nozzle type")
            return False
        else:
            return True

    def clear_all(self):
        global g_template, g_component, g_patient, g_convalgo, g_main, g_aperture, g_compensator, g_phantom

        g_template = []
        self.listTemplates.clear()

        g_component = []
        self.tableComp.setRowCount(0)
        self.widgetNozzle.trigger_refresh()

        g_patient = data.Patient()
        self.linePatientDir.clear()
        self.listPatientCT.clear()
        self.lineRTS.clear()
        self.lineRTP.clear()
        self.lineRD.clear()
        self.lineMacro.clear()

        g_convalgo = {
            'File':[None,"str"], 'Number of Beams':[None, "int"], '1st Scatterer':[None, "int"], '2nd Scatterer':[None, "int"],
            'Modulator':[None, "int"], 'Stop Position':[None, "int"], 'Energy':[None, "float"], 'BCM':[None, "str"], 'BWT':[None, "str"]
        }
        for val in self.conv_values:
            val.clear()

        g_main = []
        g_aperture = []
        g_compensator = []
        g_phantom = []

    def new_simulation(self):
        reply = QMessageBox.question(self, "Message", "Are you sure to remove all?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.clear_all()
        else:
            return

    def save_cfg(self):
        global g_nozzle_type
        fname = QFileDialog.getSaveFileName(self, 'Save', os.path.join(base_path,'prod'), filter="Nozzle files (*.nzl)")[0]
        if not fname.endswith('.nzl'):
            fname = fname + '.nzl'
        fout = open(fname, 'w')
        fout.write(f"Nozzle: {g_nozzle_type}\n")
        for component in g_component:
            fulltext = component.fulltext().split('\n')
            for idx, text in enumerate(fulltext):
                fulltext[idx] = '  ' + text
            fulltext = '\n\n'.join(t for t in fulltext)
            fout.write(f"{component.name}: >\n{fulltext}\n\n")
        fout.close()

    def open_cfg(self):
        global g_nozzle_type
        fname = QFileDialog.getOpenFileName(self, 'Open', os.path.join(base_path,'prod'), filter = "Nozzle files (*.nzl)")[0]
        if fname == '' or fname is None: return
        if not fname.endswith('.nzl'): return
        with open(fname, 'r') as f:
            self.clear_all()
            cfg = yaml.load(f, Loader=yaml.FullLoader)
        g_nozzle_type = cfg['Nozzle'].lower()
        if g_nozzle_type == 'scattering': self.radioScattering.setChecked(True)
        elif g_nozzle_type == 'scanning': self.radioScanning.setChecked(True)
        for name, text in cfg.items():
            if name == 'Nozzle': continue
            component = data.Component(g_nozzle_type)
            component.load(text, load=True, draw_all=True)
            component.name = name
            g_template.append(component)
            item = QListWidgetItem(self.listTemplates)
            f = Item()
            f.add_label(component.name)
            self.listTemplates.setItemWidget(item, f)
            self.listTemplates.addItem(item)
            item.setSizeHint(f.sizeHint())
            self.add_component()

    def generate_template(self, name, idx=-999):
        replace = False
        if any(name == i.name for i in g_template[:-1]):
            reply = QMessageBox.question(self, "Message", f'Are you sure to replace {name}?',
              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                replace = True
                for idx, template in enumerate(g_template[:-1]):
                    if name == template.name:
                        g_template[idx] = template
                        g_template.pop(len(g_template)-1)
            else:
                return

        if idx >= 0:
            item = self.listTemplates.itemWidget(self.listTemplates.item(idx))
            item.name = name
            item.label.setText(name)
            return

        if not replace:
            item = QListWidgetItem(self.listTemplates)
            f = Item()
            f.add_label(name)
            self.listTemplates.setItemWidget(item, f)
            self.listTemplates.addItem(item)
            item.setSizeHint(f.sizeHint())

    def new_template(self):
        if not self.check_beam_mode(): return

        template = ComponentWindow(self)
        r = template.return_para()
        if r:
            template = g_template[-1]
            self.generate_template(template.name)        

    def modify_template(self):
        if not self.check_beam_mode(): return

        if len(g_template) < 1: return
        idx = self.listTemplates.currentRow()

        template = ComponentWindow(self, fname=idx)
        r = template.return_para()
        if r:
            template = g_template[-1]
            if template.name != g_template[idx].name:
                g_template[idx] = template
                g_template.pop(len(g_template)-1)
            self.generate_template(template.name, idx)
    
    def delete_template(self):
        if not self.check_beam_mode(): return

        if len(g_template) < 1: return
        idx = self.listTemplates.currentRow()
        g_template.pop(idx)      
        self.listTemplates.takeItem(idx)

    def add_component(self):
        if not self.check_beam_mode(): return

        if len(g_template) < 1: return
        idx = self.listTemplates.currentRow()
        g_component.append(g_template[idx])
        g_component[-1].outname = os.path.join(g_outdir, 'nozzle', g_component[-1].name+'.tps')

        replace = False
        if len(g_component)> 1 and any(g_component[idx].name == i.name for i in g_component[:-1]):
            reply = QMessageBox.question(self, "Message", f'Are you sure to replace {g_template[idx].name}?',
              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                replace = True
                for idx, component in enumerate(g_component[:-1]):
                    if g_template[idx].name == component.name:
                        g_component[idx] = component
                        g_component.pop(len(g_component)-1)
            else:
                return

        components = []
        for subname, subcomp in g_component[-1].subcomponent.items():
            info = {'Name':'','Component':'','Parent':'',
                    'HLX':"0.0 mm",'HLY':"0.0 mm",'HLZ':"0.0 mm",
                    'RMin':"0.0 mm",'RMax':"0.0 mm",
                    'HL':"0.0 mm", 'SPhi':"0.0 deg", 'DPhi':"0.0 deg",
                    'RotX':"0.0 deg",'RotY':"0.0 deg",'RotZ':"0.0 deg",
                    'TransX':"0.0 mm",'TransY':"0.0 mm",'TransZ':"0.0 mm"}
            if subname == 'Basis':
                info['Name'] = g_component[-1].name
                info['Component'] = g_component[-1].ctype
            else:
                info['Name'] = f'└─{subcomp.name}'
                info['Component'] = subcomp.name
            for para in subcomp.parameters:
                if any(para.name.lower() == i.lower() for i in info.keys()):
                    info[para.name] = para.value

            components.append(info)

        if replace:
            for irow in range(self.tableComp.rowCount()):
                for icol in range(self.tableComp.columnCount()):
                    colname = self.tableComp.horizontalHeaderItem(icol).text()
                    value = components[irow][colname]
                    self.tableComp.setItem(irow, icol, QTableWidgetItem(str(value)))
        else:
            for component in components:
                row = self.tableComp.rowCount() + 1
                self.comp_to_table_map[row-1] = len(g_component) - 1
                self.tableComp.setRowCount(row)
                for col, val in enumerate(component.values()):
                    self.tableComp.setItem(row-1,col,QTableWidgetItem(str(val)))
        self.tableComp.resizeColumnsToContents()
        self.widgetNozzle.trigger_refresh()

    def modify_component(self):
        if not self.check_beam_mode(): return

        if len(g_component) < 1: return
        row = self.tableComp.currentRow()
        idx = self.comp_to_table_map[row]

        component = ComponentWindow(self, fname=idx, modify_component=True)
        r = component.return_para()
        if r:
            rowmin = 999
            rowmax = -999
            for key, value in self.comp_to_table_map.items():
                if not value == idx: continue
                if rowmin > key: rowmin = key
                if rowmax < key: rowmax = key
            for irow in range(rowmin, rowmax+1):
                name = self.tableComp.item(irow, 1).text().replace('└─','')
                if not name in g_component[idx].subcomponent:
                    subcomp = g_component[idx].subcomponent['Basis']
                else:
                    subcomp = g_component[idx].subcomponent[name]
                for icol in range(self.tableComp.columnCount()):
                    paraname = self.tableComp.horizontalHeaderItem(icol).text()
                    for para in subcomp.parameters:
                        if para.name.lower() == paraname.lower():
                            self.tableComp.setItem(irow, icol, QTableWidgetItem(str(para.value)))
                            continue
            self.tableComp.resizeColumnsToContents()
            self.widgetNozzle.trigger_refresh()

    def delete_component(self):
        if not self.check_beam_mode(): return

        if len(g_component) < 1: return
        row = self.tableComp.currentRow()
        idx = self.comp_to_table_map[row]
        rowmin = 999
        rowmax = -999
        for key, value in self.comp_to_table_map.items():
            if not value == idx: continue
            if rowmin > key: rowmin = key
            if rowmax < key: rowmax = key
        for irow in range(rowmin, rowmax+1):
            self.tableComp.removeRow(rowmin)
        g_component.pop(idx)
        self.tableComp.resizeColumnsToContents()
        self.widgetNozzle.trigger_refresh()

    def patient_setup(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Patient CT directory")
        if directory == "": return
        g_patient.patient_setup(directory)
        self.linePatientDir.setText(g_patient.directory)
        for f in g_patient.CT:
            self.listPatientCT.addItem(QListWidgetItem(str(f)))
        self.lineRTS.setText(g_patient.RTS)
        self.lineRTP.setText(g_patient.RTP)
        self.lineRD.setText(g_patient.RD)
        
    def patient_view(self):
        if self.listPatientCT.count() != 0:
            if self.listPatientCT.currentItem() is None:
                current = self.listPatientCT.item(0).text()
            else:
                current = self.listPatientCT.currentItem().text()
        else:
            current = ""
        pat = PatientWindow(self, current)
        r = pat.return_para()
        if r:
            self.linePatientDir.setText(g_patient.directory)
            self.listPatientCT.clear()
            for f in g_patient.CT:
                self.listPatientCT.addItem(QListWidgetItem(str(f)))
            self.lineRTS.setText(g_patient.RTS)
            self.lineRTP.setText(g_patient.RTP)
            self.lineRD.setText(g_patient.RD)

    def simulation(self):
        if not self.check_beam_mode(): return

        sim = SimulationWindow(self)
        r = sim.return_para()
        if r:
            self.lineMacro.setText(sim.instance.name)

    def run(self):
        if not self.check_beam_mode(): return

        run = RunWindow(self)

    def load_convalgo(self):
        fname = QFileDialog.getOpenFileName(self, filter = g_excel_extension[0])[0]
        if fname == '': return
        setup_convalgo(fname=fname)

        def convert(item, typ):
            if typ == "int": i = int(item)
            elif typ == "float": i = round(float(item),3)
            else: i = item
            return i
        for idx, name in enumerate(g_convalgo.keys()):
            value = g_convalgo[name]
            if str(type(value[0])) == "<class 'list'>":
                for i, val in enumerate(value[0]):
                    value[0][i] = convert(val, value[1])
                if len(value[0]) == 1:
                    s = str(value[0][0])
                else:
                    s = ', '.join(str(j) for j in value[0])
            else:
                s = convert(value[0], value[1])
            self.conv_values[idx].setText(f'{s}')

class Painter(QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding
        )
        self.painter = QPainter()
        self.paintEvent(self)
                
        self.zmax = 0.00
        self.zeros = None

    def trigger_refresh(self):
        self.update()

    def paintEvent(self,event):
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.Base)
        self.painter.begin(self)
        self.draw_axis()
        self.draw()
        self.painter.end()

    def draw_axis(self):
        self.painter.setPen(QPen(Qt.blue,2))
        self.painter.drawLine(0,int(self.height()/2),self.width(),int(self.height()/2))
        self.painter.setPen(QPen(Qt.black,2))
        matrices = QFontMetrics(self.font())
        width = matrices.width('beam')
        self.painter.drawText(0,(int(self.height()/2))+10, 'beam')
        self.painter.drawLine(width+5,0,width+5,self.height())
        self.painter.setPen(QPen(Qt.black,1))
        self.zeros = [width+6, int(self.height()/2)]

    def draw(self):
        #if len(g_component) < 1:
        #    return
        for component in g_component:
            if component.ctype == "Beam": continue
            self.container(component)

    def container(self, component):
        # Only Draw container...
        # Should update subcomponent figure
        pos = {'HLX':"0.0 mm",'HLY':"0.0 mm",'HLZ':"0.0 mm",
               'RMin':"0.0 mm",'RMax':"0.0 mm",
               'HL':"0.0 mm", 'SPhi':"0.0 deg", 'DPhi':"0.0 deg",
               'RotX':"0.0 deg",'RotY':"0.0 deg",'RotZ':"0.0 deg",
               'TransX':"0.0 mm",'TransY':"0.0 mm",'TransZ':"0.0 mm"}
        ftype = ''
        for para in component.subcomponent['Basis'].parameters:
            if 'Type' == para.name:
                ftype = para.value.replace('"','').replace("'",'').replace(' ','')
            if any(para.name.lower() == i.lower() for i in pos.keys()):
                value, unit = component.calculate_value(para)
                if unit == 'mm': 
                    value = value / 10
                elif unit == 'm': 
                    value *= 100
                pos[para.name] = value

        for key, val in pos.items():
            if str(type(val)) == "<class 'str'>":
                temp = val.split(' ')
                pos[key] = float(temp[0])

        if pos['TransZ'] > self.zmax:
            self.zmax = pos['TransZ']

        if ftype == '': ftype = 'Other'

        if any(ftype == i for i in ['TsBox', 'TsDipoleMagnet', 'Other']) and any(i == 0.0 for i in [pos['HLY'], pos['HLZ']]):
            if pos['HLY'] == 0.0:
                HLY = 0.0
                for subname, subcomp in component.subcomponent.items():
                    if subname == 'Basis': continue
                    for para in subcomp.parameters:
                        if not para.name.lower() == 'hly': continue
                        value, unit = component.calculate_value(para)
                        if unit == 'mm': value = value / 10
                        elif unit == 'm': value *= 100
                        if value > HLY: HLY = value
                pos['HLY'] = HLY
            if pos['HLZ'] == 0.0:
                HLZ = 0.0
                for subname, subcomp in component.subcomponent.items():
                    if subname == 'Basis': continue
                    for para in subcomp.parameters:
                        if not para.name.lower() == 'hlz': continue
                        value, unit = component.calculate_value(para)
                        if unit == 'mm': value = value / 10
                        elif unit == 'm': value *= 100
                        HLZ += value
                pos['HLZ'] = HLZ

        elif any(ftype == i for i in ['TsCylinder', 'TsRangeModulator']) and any(i == 0.0 for i in [pos['RMax'], pos['HL']]):
            if pos['RMax'] == 0.0:
                RMax = 0.0
                for subname, subcomp in component.subcomponent.items():
                    if subname == 'Basis': continue
                    for para in subcomp.parameters:
                        if not para.name.lower() == 'rmax': continue
                        value, unit = component.calculate_value(para)
                        if unit == 'mm': value = value / 10
                        elif unit == 'm': value *= 100
                        if value > RMax: RMax = value
                pos['RMax'] = RMax
            if pos['HL'] == 0.0:
                HL = 0.0
                for subname, subcomp in component.subcomponent.items():
                    if subname == 'Basis': continue
                    for para in subcomp.parameters:
                        if not para.name.lower() == 'hl': continue
                        value, unit = component.calculate_value(para)
                        if unit == 'mm': value = value / 10
                        elif unit == 'm': value *= 100
                        HL += value
                pos['HLZ'] = HL

        self.figure(ftype, pos)

    def figure(self, ftype, pos):
        hexcodes = { # Name:(Container, Interior)
            'TsBox':('#07098a','#1be32c'), 
            'TsCylinder':('#9d1be3','#1be32c'),
            'TsRangeModulator':('#373d36','#f0e373'),
            'TsDipoleMagnet':('#23fabd','#23d2fa'),
            'TsAperture':('#30d14e','#a69b94'),
            'TsCompensator':('#e88133','#a69b94'),
            'Group':('#ffff00','#59ff00'),
            'Other':('#000000','#000000')}
        color = QColor(0,0,0)
        idx = 0 # Removing interior part, if you have enough time update interior
        color.setNamedColor(hexcodes[ftype][idx])
        self.painter.setBrush(color)
        yaxis = pos['TransY']
        zaxis = pos['TransZ']
        if ftype == "TsBox":
            height = pos['HLY']
            width = pos['HLZ']
        elif ftype == "TsCylinder":
            height = pos['RMax']
            width = pos['HL']
        elif ftype == "TsRangeModulator":
            # FIXME
            height = pos['RMax']*2
            width = pos['HL']
        elif ftype == "TsDipoleMagnet":
            height = pos['HLY']
            width = pos['HLZ']
        else:
            height = pos['HLY']
            width = pos['HLZ']
            if height == 0.0: height = 10.0
            if width == 0.0: width = 10.0

        if pos['TransZ'] == self.zmax:
            start = (self.zeros[0],self.zeros[1]-5*height/2)
            end = (self.zeros[0]+5*width,self.zeros[1]+5*height/2)
        else:
            relz = self.zmax - pos['TransZ']
            start = (self.zeros[0]+3*relz,self.zeros[1]-5*height/2)
            end = (self.zeros[0]+3*relz+5*width, self.zeros[1]+5*height/2)
        
        self.painter.drawRect(int(start[0]),int(start[1]),int(end[0]-start[0]),int(end[1]-start[1]))

if __name__ == '__main__':
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    ex = MainWindow()
    sys.exit(app.exec())