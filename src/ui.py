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

base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(base_path)

form_class = uic.loadUiType(os.path.join(base_path,'ui','main.ui'))[0]
extension = ["Text files (*.txt *.tps)", "Data files (*.dat)"]

class SimulationWindow(QDialog):
    def __init__(self, parent):
        super(SimulationWindow, self).__init__(parent)
        uic.loadUi(os.path.join(base_path,'ui','simulation.ui'), self)

        self.functions = []
        self.set_action()
        self.show()

    def set_action(self):
        self.pushOpen.clicked.connect(self.open_macro)
        self.pushAdd.clicked.connect(self.add_function)
        self.pushAdd2.clicked.connect(self.add_function)
        self.pushDelete.clicked.connect(self.delete_function)
        self.pushOk.clicked.connect(self.click_ok)
        self.pushCancel.clicked.connect(self.click_cancel)
        
        self.listAvailable.itemDoubleClicked.connect(self.add_function)
        self.listAdded.itemDoubleClicked.connect(self.delete_function)

    def open_macro(self):
        fname = QFileDialog.getOpenFileName(self, filter = "Python files (*.py)")[0]
        if fname == "": return
        self.labelMacro.setText(" Macro: "+fname.split('/')[-1])
        self.listAvailable.addItem(QListWidgetItem("item1"))
        self.listAvailable.addItem(QListWidgetItem("item2"))
        
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

class ComponentWindow(QDialog):
    class Item(QWidget):
        # Write items in listWidget
        def __init__(self):
            QWidget.__init__(self, flags=Qt.Widget)

            self.type = None
            self.category = None
            self.name = None
            self.subname = None
            self.paraname = None
            self.value = None
            
            self.checked = None

        def import_preset(self, name, path):
            self.layout = QBoxLayout(QBoxLayout.TopToBottom)
            self.checkbox = QCheckBox(name)
            #self.checkbox.setChecked(True)
            #self.checkbox.stateChanged.connect(self.checkbox_state)
            self.layout.addWidget(self.checkbox)
            self.label = QLabel("("+path+")")
            self.layout.addWidget(self.label)
            self.layout.setSizeConstraint(QBoxLayout.SetFixedSize)
            self.setLayout(self.layout)
            self.paraname = name
            self.value = path

        def add_parameter(self, variable, default):
            variable = variable.replace("\n", "").replace("\t", "").replace(" ","")
            default = default.replace("\n","").replace("\t","").replace(" ","")
            self.layout = QBoxLayout(QBoxLayout.LeftToRight)
            self.label = QLabel(variable)
            self.layout.addWidget(self.label)
            self.txt = QLineEdit(default)
            self.layout.addWidget(self.txt)
            self.layout.setSizeConstraint(QBoxLayout.SetFixedSize)
            self.setLayout(self.layout)
            self.value = default
            
            temp = variable.split(':')[-1].split('/')
            if ':' in variable:
                self.type = variable.split(':')[0]
            self.paraname = temp[-1]
            if len(temp) == 2:
                self.name = temp[0]
            elif len(temp) == 3:
                self.category = temp[0]
                self.name = temp[1]
            elif len(temp) == 4:
                self.category = temp[0]
                self.name = temp[1]
                self.subname = temp[2]
            else:
                return

        def set_value(self, value):
            self.value = value
            self.txt.setText(value)
            
        def set_name(self, name, only_sub = False):
            if only_sub:
                self.subname = name
            else:
                temp = name.split('/')
                self.name = temp[0]
                self.subname = '/'.join(i for i in temp[1:])
                
            if self.subname is not None:
                name = f'{self.type}:{self.category}/{self.name}/{self.subname}/{self.paraname}'
            else:
                name = f'{self.type}:{self.category}/{self.name}/{self.paraname}'

            self.label.setText(name)
        
        def get_full_name(self):
            name = ""
            if self.type is not None:
                name += self.type+":"
            if self.category is not None:
                name += self.category
            if self.name is not None:
                name += "/"+self.name
            if self.subname is not None:
                name += "/"+self.subname
            if self.paraname is not None:
                name += "/"+self.paraname
            return name
                
    def __init__(self, parent, component = None, modify = False):
        super(ComponentWindow, self).__init__(parent)
        uic.loadUi(os.path.join(base_path,'ui','component.ui'), self)

        self.components = {
          'MonitorElement':['Basis', 'CylinderFrame', 'BoxFrame', 'CylinderLayer', 'BoxLayer'],
          'Scatterer':['Basis', 'Scatterer1', 'Lollipop', 'Scatterer2', 'Holder', 'Hole'],
          'RangeModulator':['LargeWheel','SmallWheel'], 
          'SMAG':['Basis','Dipole'],
          'VC':['Basis','XJaws', 'YJaws'],
          'Snout':['Basis','BrassBlock', 'BrassCone'],
          'Apperture':['Basis'],
          'Compensator':['Basis'],
          'PhaseSpaceVolume':['Basis'],
          'Contour':['Basis']
        }
        self.convalgo = []
        self.imported = []
        self.elements = {}
        self.component = {
            "import":[],
            "parameter":{}
        }
        self.para_from_macro = []

        self._set_action()
        if component is not None:
            self._preload(component, modify)
        if not modify:
            self.accept()

        self.show()
        
    def _set_action(self):
        # Convalgo
        self.pushConv.clicked.connect(self._load_convalgo)
        # Import
        self.pushImport.clicked.connect(self._open_component)
        # Element
        ### LineEdit
        self.lineNewParaName.returnPressed.connect(self._add_element)
        self.lineNewParaValue.returnPressed.connect(self._add_element)
        self.lineName.returnPressed.connect(lambda: self._change_component_name(self.lineName.text()))
        ### Button
        self.pushAdd.clicked.connect(self._add_element)
        self.pushClear.clicked.connect(self._clear_elements)
        self.pushAppend.clicked.connect(self._append_component)
        self.pushMake.clicked.connect(self._click_make)
        self.pushCancel.clicked.connect(self._click_cancel)
        ### Combo
        self.comboComp.addItem('New')
        self.comboComp.addItem("Load")
        self.comboComp.insertSeparator(2)
        for key, value in self.components.items():
            self.comboComp.addItem(key)
        self.comboComp.currentTextChanged.connect(lambda: self._new_component(self.comboComp.currentText()))
        ### Element tab
        self.tabAddBtn = QToolButton()
        self.tabComp.setCornerWidget(self.tabAddBtn, Qt.TopRightCorner)
        self.tabAddBtn.setAutoRaise(True)
        self.tabAddBtn.setIcon(QIcon("../icons/new.png"))
        self.tabAddBtn.clicked.connect(self._add_subcomponent)
        
    def _load_convalgo(self):
        excel_extension = "Excel files (*.xls *.xlms)"
        fname = QFileDialog.getOpenFileName(self, filter = excel_extension)[0]
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

    def _import_component(self, fname):
        lst = fname.split('/')
        name = lst[-1]
        path = '/'.join(i for i in lst)
        if any(path == i.value for i in self.imported):
            return
        item = QListWidgetItem(self.listImport)
        f = self.Item()
        f.import_preset(name, path)
        f.checkbox.stateChanged.connect(self._append_component)
        self.imported.append(f)
        self.listImport.setItemWidget(item, f)
        self.listImport.addItem(item)
        item.setSizeHint(f.sizeHint())

    def _open_component(self):
        fname = QFileDialog.getOpenFileName(self, initialFilter = extension[0], filter='\n'.join(i for i in extension))[0]
        if fname == "": return
        self._import_component(fname)

    def _load_component(self, name, filename):
        listPara = QListWidget()
        listPara.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.elements[name] = []
        actions = {"Add":self._add_element, "Modify":self._modify_element,
                   "Delete":self._delete_element, "Clear":self._clear_elements}
        for key, value in actions.items():
            action = QAction(key, listPara)
            action.triggered.connect(value)
            listPara.addAction(action)
        
        if str(type(filename)) == "<class 'list'>":
            lines = filename
        else:
            try:
                f = open(filename, 'r')
                lines = f.readlines()
            except:
                index = self.tabComp.addTab(listPara, name)
                return index
        
        maxlen = 1
        for line in lines:
            if line.startswith('#'): continue

            line = line.replace('\t','').replace('\n', '').replace(' ', '')
            if line == '': continue
            line = line.split('=')
            if line[0].startswith("includeFile"):
                self._import_component(line[-1])
                continue
            if maxlen < len(line[0]): maxlen = len(line[0])
            if any(line[0] == i.name for i in self.elements[name]): continue
                
            para = QListWidgetItem(listPara)
            parameter = self.Item()
            parameter.add_parameter(line[0], line[1])
            self.elements[name].append(parameter)
            listPara.setItemWidget(para, parameter)
            listPara.addItem(para)
            para.setSizeHint(parameter.sizeHint())
        index = self.tabComp.addTab(listPara, name)
        return index

    def _new_component(self, item):
        if item == "Load" or item == "New": 
            dic = {item:['Basis']}
            outtext = "CustomComponent"
        elif item == "": return
        else: 
            dic = {item:self.components[item]}
            outtext = item
        
        self.tabComp.clear()
        self.elements = {}
        
        for subcomp in dic[item]:
            if item == "Load":
                filename = QFileDialog.getOpenFileName(self, initialFilter = extension[0], filter='\n'.join(i for i in extension))[0]
            else:
                filename = os.path.join(base_path,'data/components',item,subcomp+'.tps')
            self._load_component(name = subcomp, filename = filename)
        
        self.lineOutput.setText(outtext)

    def _add_subcomponent(self):
        if not self.comboComp.currentText() == "Load":
            newtab = NewTab(self, self.components[self.comboComp.currentText()])
        else:
            newtab = NewTab(self, [])
        r = newtab.return_para()
        if r:
            subcomp = newtab.comboSubcomp.currentText()
            name = newtab.lineTabName.text()
            filename = os.path.join(base_path,'data/components',self.comboComp.currentText(),subcomp+'.tps')
            index = self._load_component(name = name, filename = filename)
            self.tabComp.setCurrentIndex(index)
            self._change_component_name(name = name, only_sub = True)

    def _change_component_name(self, name, only_sub = False):
        widget = self.tabComp.currentWidget()
        subcomp = self.tabComp.tabText(self.tabComp.currentIndex())
        for item in self.elements[subcomp]:
            item.set_name(name, only_sub)

    def _add_element(self):
        widget = self.tabComp.currentWidget()
        subcomp = self.tabComp.tabText(self.tabComp.currentIndex())
        name = self.lineNewParaName.text()
        value = self.lineNewParaValue.text()
        if name == "": return
        for idx in range(len(self.elements[subcomp])):
            if name == self.elements[subcomp][idx].name:
                self.elements[subcomp][idx].set_value(value)
                return
        para = QListWidgetItem(widget)
        parameter = self.Item()
        parameter.add_parameter(name, value)
        self.elements[subcomp].append(parameter)
        idx = len(self.elements) - 1
        widget.setItemWidget(para, parameter)
        widget.addItem(para)
        para.setSizeHint(parameter.sizeHint())
  
    def _delete_element(self):
        widget = self.tabComp.currentWidget()
        idx = widget.currentRow()
        subcomp = self.tabComp.tabText(self.tabComp.currentIndex())
        self.elements[subcomp].pop(idx)
        widget.takeItem(widget.currentRow())
        
    def _modify_element(self):
        widget = self.tabComp.currentWidget()
        idx = widget.currentRow()
        subcomp = self.tabComp.tabText(self.tabComp.currentIndex())
        name = self.elements[subcomp][idx].get_full_name()
        value = self.elements[subcomp][idx].value
        modify = ModifyParameter(self,name,value)
        r = modify.return_para()
        if r:
            self.elements[subcomp][idx].set_name(modify.name)
            self.elements[subcomp][idx].set_value(modify.value)

    def _append_component(self):
        self.component['import'] = []
        for item in self.imported:
            if item.checkbox.isChecked() == True:
                text = f"includeFile = {item.value}"
                self.component['import'].append(text)
        subcomp = self.tabComp.tabText(self.tabComp.currentIndex())
        self.component['parameter'][subcomp] = []
        for item in self.elements[subcomp]:
            text = f"{item.get_full_name()} = {item.value}"
            self.component['parameter'][subcomp].append(text)
        print(self.component['parameter'])
        self._update_preview()

    def _clear_elements(self):
        subcomp = self.tabComp.tabText(self.tabComp.currentIndex())
        for item in self.elements[subcomp]:
            item.set_value(None)

    def _update_preview(self):
        text = ""
        text += "\n".join(i for i in self.component['import'])
        if len(self.component['import']) > 1:
            text += "\n\n"
        for key, value in self.component['parameter'].items():
            text += "\n".join(i for i in value)
            text += "\n\n"
        self.textPreview.setText(text)
        
    def _preload(self, component, modify):
        outtext = component['name']
        fname = component.get('file')
        if fname is not None:
            self._load_component("Load",fname)
        else:
            for key, value in component['parameter'].items():
                self._load_component(key, value)
        self.lineOutput.setText(outtext)
        self.lineOutput.setReadOnly(True)

    def _click_make(self):
        self.accept()
        
    def _click_cancel(self):
        self.reject()
        
    def return_para(self):
        return super().exec_()

class NewTab(QDialog):
    def __init__(self, parent, components):
        super(NewTab, self).__init__(parent)
        uic.loadUi(os.path.join(base_path,'ui','newtab.ui'), self)
        self.setWindowTitle("New tab")
        
        for item in components:
            self.comboSubcomp.addItem(item)
        
        self.lineTabName.returnPressed.connect(self.return_para)
        self.pushOk.clicked.connect(self._click_ok)
        self.pushCancel.clicked.connect(self._click_cancel)
        self.show()
        
    def _click_ok(self):
        self.accept()
        
    def _click_cancel(self):
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
        
        self.pushOk.clicked.connect(self.click_ok)
        self.pushCancel.clicked.connect(self.click_cancel)
        self.show()
    
    def click_ok(self):
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
        
        self.cfg = None
        self.templates = []
        self.components = []
        self.patient = {"directory":"","files":[]}
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
        self.actionTempLoad.triggered.connect(self.load_template)
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
        self.toolBar.addAction(self.actionTempLoad)
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
        self.listTemplates.addAction(self.actionTempLoad)
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

    def generate_template(self, name, template):
        item = QListWidgetItem(self.listTemplates)
        f = self.Item()
        f.save(name)
        self.listTemplates.setItemWidget(item, f)
        self.listTemplates.addItem(item)
        item.setSizeHint(f.sizeHint())
        dic = template
        dic['name'] = name
        self.templates.append(dic)

    def new_template(self):
        template = ComponentWindow(self)
        r = template.return_para()
        if r:
            self.generate_template(template.lineOutput.text(), template.component)

    def load_template(self):
        fname = QFileDialog.getOpenFileName(self, filter = '\n'.join(i for i in extension))[0]
        if fname == "": return
        
        lst = fname.split('/')
        name = lst[-1].split('.')[0]
        dic = {}
        dic['name'] = name
        dic['file'] = '/'.join(i for i in lst)
        template = ComponentWindow(self, dic)
        self.generate_template(template.lineOutput.text(), template.component)
        
    def modify_template(self):
        idx = self.listTemplates.currentRow()
        dic = self.templates[idx]

        template = ComponentWindow(self, dic)
        r = template.return_para()
        if r:
            self.templates.pop(idx)
            self.listTemplates.takeItem(self.listTemplates.currentRow())
            self.generate_template(template.lineOutput.text(), template.component)
    
    def delete_template(self):
        idx = self.listTemplates.currentRow()
        self.templates.pop(idx)      
        self.listTemplates.takeItem(idx)

    def add_component(self):
        idx = self.listTemplates.currentRow()
        template = self.templates[idx]
        components = []
        for key, value in template['parameter'].items():
            info = {'name':'','component':'','parent':'',
                    'HLX':"0.0 mm",'HLY':"0.0 mm",'HLZ':"0.0 mm",
                    'RotX':"0.0 mm",'RotY':"0.0 mm",'RotZ':"0.0 deg",
                    'TransX':"0.0 mm",'TransY':"0.0 mm",'TransZ':"0.0 mm"}
            for item in value:
                tmp = item.replace(' ','').split('=')
                name = tmp[0].split(':')[-1]
                val = tmp[1]
                if len(name.split('/')) == 3:
                    info['name'] = name.split('/')[1]
                    info['component'] = info['name']
                    if 'parent' in name.lower():
                        info['parent'] = val
                elif len(name.split('/')) >= 4:
                    tmp = name.split('/')
                    info['name'] = "└ "+tmp[2]
                    info['component'] = tmp[1]+'/'+tmp[2]
                    if 'parent' in name.lower():
                        info['parent'] = val
                
                for k in info.keys():
                    if k.lower() == name.split('/')[-1].lower():
                        info[k] = val
            components.append(info)

        for component in components:
            row = self.tableComp.rowCount() + 1
            self.tableComp.setRowCount(row)
            for col, val in enumerate(component.values()):
                #item = QTableWidgetItem(str(val))
                self.tableComp.setItem(row-1,col,QTableWidgetItem(str(val)))
        self.tableComp.resizeColumnsToContents()

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
        self.patient['directory'] = QFileDialog.getExistingDirectory(self, "Select Patient CT directory")
        self.labelPatientDir.setText("Directory: "+self.patient['directory'])
        if self.patient['directory'] == "": return
        for f in os.listdir(self.patient['directory']):
            if not f.endswith('.dcm'): continue
            self.patient['files'].append(str(f))
        self.patient['files'].sort()
        for f in self.patient['files']:
            self.listPatient.addItem(QListWidgetItem(str(f)))
        
    def patient_view(self):
        if self.listPatient.count() != 0:
            current = self.listPatient.currentItem().text()
        else:
            current = ""
        pat = PatientWindow(self, self.patient['directory'], self.patient['files'], current)
        r = pat.return_para()
        if r:
            self.patient['directory'] = pat.dirname
            self.patient['files'] = pat.files
            

    def simulation(self):
        sim = SimulationWindow(self)
        r = sim.return_para()
        if r:
            self.macros = sim.functions
            for macro in self.macros:
                self.listMacro.addItem(QListWidgetItem(macro))

    def run(self):
        run = RunWindow(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
