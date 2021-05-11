import os, sys
import time
import pydicom as dicom
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from functools import partial
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

import data
import painter

base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
form_class = uic.loadUiType(os.path.join(base_path,'ui','main.ui'))[0]
sys.path.append(base_path)

g_text_extension = ["Text files (*.txt *.tps)", "Data files (*.dat)"]
g_excel_extension = ["Excel files (*.xls *.xlms)"]

g_save = None
g_template = []
g_component = []
g_patient = data.Patient()

class ComponentWindow(QDialog):
    class Item(QWidget):
        # Write items in listWidget
        def __init__(self):
            QWidget.__init__(self, flags=Qt.Widget)
            self.layout = QBoxLayout(QBoxLayout.LeftToRight)
            self.label = QLabel()
            self.checkbox = QCheckBox()
            self.lineValue = QLineEdit()
            self.lineValue.setMouseTracking(True)

        def import_preset(self, name, path):
            self.layout.setDirection(QBoxLayout.TopToBottom)
            self.checkbox.setText(name)
            self.label.setText("("+path+")")
            self.checkbox.setChecked(True)
            self.layout.addWidget(self.checkbox)
            self.layout.addWidget(self.label)
            self.layout.setSizeConstraint(QBoxLayout.SetFixedSize)
            self.setLayout(self.layout)

        def add_parameter(self, name, value):
            self.layout.setDirection(QBoxLayout.LeftToRight)
            self.label.setText(name)
            self.lineValue.setText(value)
            self.layout.addWidget(self.label)
            self.layout.addWidget(self.lineValue)
            self.layout.setSizeConstraint(QBoxLayout.SetFixedSize)
            self.setLayout(self.layout)
        
        def set_name(self, name):
            self.label.setText(name)
                
    def __init__(self, parent, fname=None):
        super(ComponentWindow, self).__init__(parent)
        uic.loadUi(os.path.join(base_path,'ui','component.ui'), self)

        #self.setMouseTracking(True)
        #self.x = 0
        #self.y = 0

        self.template = data.Component()
        if fname is not None:
            self.preload(fname)

        self.set_action()
        self.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.click_cancel()
    
    #def mouseMoveEvent(self, event):
    #    self.x = event.x()
    #    self.y = event.y()
    #    print(event.x(), event.y())
        
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
        self.pushAppend.clicked.connect(self.append_component)
        self.pushAppendAll.clicked.connect(lambda: self.append_component(save_all=True))
        self.pushClearAll.clicked.connect(self.clear_all)
        self.pushMake.clicked.connect(self.click_make)
        self.pushClearPrev.clicked.connect(self.clear_preview)
        self.pushCancel.clicked.connect(self.click_cancel)
        ### Combo
        self.comboComp.addItem('Select')
        self.comboComp.addItem('New')
        self.comboComp.addItem("Load")
        self.comboComp.insertSeparator(2)
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
        item = self.Item()
        item.import_preset(name, path)
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
        fname = QFileDialog.getOpenFileName(self, initialFilter = g_text_extension[0], filter='\n'.join(i for i in g_text_extension))[0]
        if fname == "": return
        self.draw_import_widget(fname)

    def import_clear(self):
        for f in self.template.imported:
            self.template.modify_file(f, delete=True)
        self.listImport.clear()
        self.update_preview()

    def draw_para_widget(self, tabname):
        listPara = QListWidget()
        listPara.setContextMenuPolicy(Qt.ActionsContextMenu)
        
        actions = {"Add":self.add_element, "Modify":self.modify_element,
                   "Delete":self.delete_element, "Clear":self.clear_elements}
        for key, value in actions.items():
            action = QAction(key, listPara)
            action.triggered.connect(value)
            listPara.addAction(action)
        listPara.itemDoubleClicked.connect(lambda: self.modify_element())

        paras = [i for i in self.template.subcomponent[tabname].parameters]
        for para in paras:
            name = f'{para.vtype}:{para.category}/{para.directory}/{para.name}'
            witem = QListWidgetItem(listPara)
            item = self.Item()
            item.add_parameter(name, para.value)
            item.lineValue.textChanged.connect(lambda: self.modify_element(True))
            item.lineValue.returnPressed.connect(lambda: self.modify_element(True))
            listPara.setItemWidget(witem, item)
            listPara.addItem(witem)
            witem.setSizeHint(item.sizeHint())
        index = self.tabComp.addTab(listPara, tabname)
        return index

    def new_template(self, item):
        if item == '' or item == 'Select':
            return
        self.tabComp.clear()
        self.template = data.Component()
        if item == "New":
            self.clear_all()
            self.template.name = ''
            self.template.ctype = ''
        elif item == "Load":
            fname = QFileDialog.getOpenFileName(self, initialFilter = g_text_extension[0], filter='\n'.join(i for i in g_text_extension))[0]
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
            fname = os.path.join(base_path,'data/components',self.comboComp.currentText(),subcomp+'.tps')
            self.template.load(fname=fname)
            self.template.modify_subname(subcomp, tabname)
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

    def change_subname(self, name):
        widget = self.tabComp.currentWidget()
        subcomp = self.tabComp.tabText(self.tabComp.currentIndex())
        self.template.modify_subname(subcomp, name)

        for idx in round(self.widget.count()):
            para = self.template.subcomponent[subcomp].parameters[idx]
            name = f'{para.vtype}:{para.category}/{para.directory}/{para.name}'

            item.set_name(name=name)
        self.update_preview()

    def add_element(self):
        widget = self.tabComp.currentWidget()
        subcomp = self.tabComp.tabText(self.tabComp.currentIndex())
        name = self.lineNewParaName.text()
        value = self.lineNewParaValue.text()
        if name == "": return
        self.template.modify_parameter(subcomp, {name:value})
        
        witem = QListWidgetItem(widget)
        item = self.Item()
        item.add_parameter(name, value)
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
        text = ""
        for item in self.template.imported:
                text += f"includeFile = {item}\n"
        text += "\n"
        for subcomp in self.template.subcomponent.values():
            if not subcomp.draw: continue
            for para in subcomp.parameters:
                if not para.draw: continue
                text += f'{para.fullname()} = {para.value}\n'
            text += '\n'
        self.textPreview.setText(text)
        
    def clear_all(self):
        self.template = data.Component()
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

    def preload(self, fname):
        if type(fname) == int:
            self.template = g_template[fname]
        elif type(fname) == str:
            self.template.load(fname)
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
        g_template.append(self.template)
        self.accept()
        
    def click_cancel(self):
        reply = QMessageBox.question(self, "Message", "Are you sure to cancel?",
          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.reject()
        else:
            return
        
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
    
class ModifyParameter(QDialog):
    def __init__(self, parent, name="", value=""):
        super(ModifyParameter, self).__init__(parent)
        uic.loadUi(os.path.join(base_path,'ui','modification.ui'), self)
        self.name = name
        self.value = value
        
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

class PatientWindow(QDialog):
    def __init__(self, parent, dirname="", files="", current=""):
        super(PatientWindow, self).__init__(parent)
        uic.loadUi(os.path.join(base_path,'ui','patient.ui'), self)
        
        self.dirname = dirname
        self.files = files
        self.current = current
        
        self.fig = plt.figure()
        self.widgetCanvas = FigureCanvas(self.fig)
        self.gridLayout.addWidget(self.widgetCanvas)
        self.set_action()
        if os.path.exists(os.path.join(self.dirname,self.current)):
            self.show_image(self.current)
        self.show()
        
    def set_action(self):
        self.labelDir.setText("Directory: "+self.dirname)
        current_idx = 0
        for idx, item in enumerate(self.files):
            if not item.startswith("CT"): continue
            if item == self.current: current_idx = idx
            self.comboFiles.addItem(item)
        self.comboFiles.setCurrentIndex(current_idx)
        self.comboFiles.currentTextChanged.connect(lambda: self.show_image(self.comboFiles.currentText()))
        self.pushOpen.clicked.connect(self.open_directory)
        self.pushPrev.clicked.connect(lambda: self.change_image(self.pushPrev))
        self.pushNext.clicked.connect(lambda: self.change_image(self.pushNext))
        
    def show_image(self, ct):
        self.fig.clear()
        CT = dicom.dcmread(os.path.join(self.dirname, ct))
        ax = self.fig.add_subplot(111)
        ax.imshow(CT.pixel_array, cmap=plt.cm.bone)
        self.widgetCanvas.draw()
    
    def open_directory(self):
        newdir = ""
        newdir = QFileDialog.getExistingDirectory(self, "Select Patient CT directory")
        if newdir == self.dirname or newdir == "": return
        else:
            self.dirname = newdir
            self.files = []
            for f in os.listdir(self.dirname):
                if not f.endswith('.dcm'): continue
                self.files.append(f)
            self.files.sort()
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

        self.functions = []
        self.set_action()
        self.show()

    def set_action(self):
        self.pushAdd.clicked.connect(self.add_function)
        self.pushDelete.clicked.connect(self.delete_function)
        self.pushOk.clicked.connect(self.click_ok)
        self.pushCancel.clicked.connect(self.click_cancel)
        
        macros = ['DoseSimulation']
        self.comboMacro.addItem('')
        self.comboMacro.addItem('Open')
        self.comboMacro.insertSeparator(2)
        for macro in macros:
            self.comboMacro.addItem(macro)
        self.comboMacro.currentTextChanged.connect(self.open_macro)       
        #self.listAvailable.itemDoubleClicked.connect(self.add_function)
        #self.listAdded.itemDoubleClicked.connect(self.delete_function)

    def open_macro(self):
        if self.comboMacro.currentText() == 'Open':
            fname = QFileDialog.getOpenFileName(self, filter = "Python files (*.py)")[0]
            if fname == "": return
            self.labelMacro.setText(" Custom File: "+fname.split('/')[-1])
        import config as cfg
        proton = cfg.Proton()
        proton.load(fname)
        processes = []
        for i in proton.module.__dir__():
            if i[0].isupper():  
                processes.append(i)
                self.listAvailable.addItem(QListWidgetItem(i))
        
    def add_function(self):
        item = self.listAvailable.currentItem()
        if any(item.text() == i for i in self.functions): return
        self.functions.append(item.text())
        self.listAdded.addItem(QListWidgetItem(item.text()))

    def delete_function(self):
        idx = self.listAdded.currentRow()
        self.listAdded.takeItem(idx)
        
    def click_ok(self):
        self.accept()
        
    def click_cancel(self):
        self.reject()
        
    def return_para(self):
        return super().exec_()

class RunWindow(QDialog):
    def __init__(self, parent):
        super(RunWindow, self).__init__(parent)
        uic.loadUi(os.path.join(base_path,'ui','run.ui'), self)
        
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
        self.execute_topas()
        self.do_postprocess()

    def undo(self, checkbox):
        if checkbox.isCheckable():
            checkbox.setChecked(True)

    def initialize(self):
        self.textLog.append("...Initialize topas parameters")
        try:
            self.checkInit.setCheckable(True)
            self.checkInit.setChecked(True)
            self.textLog.append("Parameter setting is success.")
        except:
            self.textLog.append("Parameter setting is failed.")
            
    def generate_input(self):
        self.textLog.append("...Generate topas input files")
        try:
            self.checkInput.setCheckable(True)
            self.checkInput.setChecked(True)
            self.textLog.append("Topas input files are generated.")
        except:
            self.textLog.append("Generation is failed.")
            
    def execute_topas(self):
        self.textLog.append("...Execute Topas")
        try:
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
    class Item(QWidget):
        def __init__(self):
            QWidget.__init__(self, flags=Qt.Widget)
            self.name = None
            
        def save(self, name):
            self.layout = QBoxLayout(QBoxLayout.LeftToRight)
            self.label = QLabel(name)
            self.layout.addWidget(self.label)
            self.layout.setSizeConstraint(QBoxLayout.SetFixedSize)
            self.setLayout(self.layout)

    def __init__(self):
        super().__init__()
        self.setupUi(self)


        self.patient = data.Patient()
        self.painter = painter.Painter()

        self.macros = []
        self.set_actions()
        self.tableComp.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.show()

    def set_actions(self):
        # Menubar
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
        ### Simulation
        self.actionSimLoad.triggered.connect(self.simulation)
        ### Run
        self.actionRun = QAction(QIcon('../icons/run.png'), 'Run', self)
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
        self.toolBar.addAction(self.actionPatientConv)
        self.toolBar.addSeparator()

        label = QLabel(" Simulation: ")
        self.toolBar.addWidget(label)
        self.toolBar.addAction(self.actionSimLoad)
        self.toolBar.addSeparator()

        self.toolBar.addAction(self.actionRun)
        self.toolBar.setIconSize(QSize(32,32))
        
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
        self.listPatient.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.listPatient.addAction(self.actionPatientView)
        self.listPatient.itemDoubleClicked.connect(self.patient_view)
        
    # Functions
    def new_simulation(self):
        return 0

    def open_cfg(self):
        return 0

    def save_cfg(self):
        return 0

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
            f = self.Item()
            f.save(name)
            self.listTemplates.setItemWidget(item, f)
            self.listTemplates.addItem(item)
            item.setSizeHint(f.sizeHint())

    def new_template(self):
        template = ComponentWindow(self)
        r = template.return_para()
        if r:
            template = g_template[-1]
            self.generate_template(template.name)

    def modify_template(self):
        if len(g_template) < 1: return
        idx = self.listTemplates.currentRow()

        template = ComponentWindow(self, idx)
        r = template.return_para()
        if r:
            template = g_template[-1]
            if template.name != g_template[idx].name:
                g_template[idx] = template
                g_template.pop(len(g_template)-1)
            self.generate_template(template.name, idx)
    
    def delete_template(self):
        if len(g_template) < 1: return
        idx = self.listTemplates.currentRow()
        g_template.pop(idx)      
        self.listTemplates.takeItem(idx)

    def add_component(self):
        if len(g_template) < 1: return
        idx = self.listTemplates.currentRow()
        g_component.append(g_template[idx])

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
                self.tableComp.setRowCount(row)
                for col, val in enumerate(component.values()):
                    self.tableComp.setItem(row-1,col,QTableWidgetItem(str(val)))
        self.tableComp.resizeColumnsToContents()
        self.window.draw(g_component)

    def modify_component(self):
        idx = self.tableComp.currentRow()
        dic = self.components[idx]
        
        component = ComponentWindow(self, dic)
        r = component.return_para()
        if r:
            self.components.pop(idx)
            row = idx
            maxcol = self.tableComp.columnCount()
            for col in range(maxcol):
                self.tableComp.takeItem(row, col)
            self.add_component()
    
    def delete_component(self):
        row = self.tableComp.currentRow()
        maxcol = self.tableComp.columnCount()
        self.components.pop(row)
        for col in range(maxcol):
            self.tableComp.takeItem(row, col)

    def patient_setup(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Patient CT directory")
        if directory == "": return
        self.patient.patient_setup(directory)
        self.labelPatientDir.setText("Directory: "+self.patient.directory)
        for f in self.patient.files:
            self.listPatient.addItem(QListWidgetItem(str(f)))
        
    def patient_view(self):
        if self.listPatient.count() != 0:
            current = self.listPatient.currentItem().text()
        else:
            current = ""
        pat = PatientWindow(self, self.patient.dirctory, self.patient.files, current)
        r = pat.return_para()
        if r:
            self.patient.directory = pat.dirname
            self.patient.files = pat.files

    def simulation(self):
        sim = SimulationWindow(self)
        r = sim.return_para()
        if r:
            self.macros = sim.functions
            for macro in self.macros:
                self.listMacro.addItem(QListWidgetItem(macro))

    def run(self):
        run = RunWindow(self)

    def load_convalgo(self):
        fname = QFileDialog.getOpenFileName(self, filter = g_excel_extension[0])[0]
        if fname == "": return
        
        self.listConv.clear()
        self.elements = {}
        
        lst = fname.split('/')
        name = lst[-1]
        path = '/'.join(i for i in lst[:-1])
        self.labelConv.setText("File: "+name)
        import getconvalgo as gc
        convalgo = gc.GetParaFromConvAlgo(path, name)

        dic = {
          '1st Scatterer':[convalgo.fscatterer, "int"],
          '2nd Scatterer':[convalgo.sscatterer, "int"],
          'Modulator':[convalgo.modulator, "int"],
          'Stop Position':[convalgo.stop, "int"],
          'Energy':[convalgo.energy, "float"],
          'BCM':[convalgo.bcm_name, "str"]
        }
        nbeam = len(convalgo.fscatterer)
        def convert(item, typ):
            if typ == "int":
                i = int(item)
            elif typ == "float":
                i = round(float(item),3)
            else:
                i = item
            return i
        for key, value in dic.items():
            if str(type(value[0])) == "<class 'list'>":
                for idx, val in enumerate(value[0]):
                    value[0][idx] = convert(val, value[1])
                if len(value[0]) == 1:
                    s = str(value[0][0])
                else:
                    s = ', '.join(str(i) for i in value[0])
            else:
                s = convert(value[0], value[1])

            para = QListWidgetItem(self.listConv)
            parameter = self.Item()
            parameter.add_parameter(key, str(s))
            self.convalgo.append(parameter)
            self.listConv.setItemWidget(para, parameter)
            self.listConv.addItem(para)
            para.setSizeHint(parameter.sizeHint())

if __name__ == '__main__':
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    ex = MainWindow()
    sys.exit(app.exec_())
