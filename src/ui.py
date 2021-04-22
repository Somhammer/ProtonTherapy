import os, sys
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

        self._set_action()
        self.show()

    def _set_action(self):
        self.pushLoad.clicked.connect(self._load)
        self.pushAdd.clicked.connect(self._add)
        self.pushRemove.clicked.connect(self._remove)
        self.pushApply.clicked.connect(self._apply)

    def _load(self):
        return 0

    def _add(self):
        return 0

    def _remove(self):
        return 0

    def _apply(self):
        return 0

class ComponentWindow(QDialog):
    class Item(QWidget):
        # Write items in listWidget
        def __init__(self):
            QWidget.__init__(self, flags=Qt.Widget)

            self.name = None
            self.value = None
            self.layout = QBoxLayout(QBoxLayout.LeftToRight)

        def import_preset(self, name, path):
            self.checkbox = QCheckBox(name)
            self.checkbox.setChecked(True)
            self.layout.addWidget(self.checkbox)
            self.label = QLabel("("+path+")")
            self.layout.addWidget(self.label)
            self.layout.setSizeConstraint(QBoxLayout.SetFixedSize)
            self.setLayout(self.layout)

        def load_parameter(self, variable, default):
            self.label = QLabel(variable)
            self.layout.addWidget(self.label)
            self.txt = QLineEdit(default)
            self.layout.addWidget(self.txt)
            self.layout.setSizeConstraint(QBoxLayout.SetFixedSize)
            self.setLayout(self.layout)
            self.name = variable
            self.value = default

        def set_value(self, value):
            self.value = value
            self.txt.setText(value)
    
    def __init__(self, parent):
        super(ComponentWindow, self).__init__(parent)
        uic.loadUi(os.path.join(base_path,'ui','component.ui'), self)

        self.components = [
          "MonitorElement",
          "Scatterer",
          "SMAG",
          "Dipole",
          "VC",
          "Snout",
          "Apperture",
          "Compensator",
          "Contour"
        ]
        self.component = None
        self.convalgo = []
        self.elements = []

        self.listPara.setContextMenuPolicy(Qt.ActionsContextMenu)

        self._set_action()

        self.show()
        
    def _set_action(self):
        # LineEdit
        self.lineNewParaName.returnPressed.connect(self._add_element)
        self.lineNewParaValue.returnPressed.connect(self._add_element)
        self.lineName.returnPressed.connect(self._set_element_name)

        # Button
        self.pushConv.clicked.connect(self._load_convalgo)
        self.pushImport.clicked.connect(self._import_component)
        self.pushAdd.clicked.connect(self._add_element)
        self.pushClear.clicked.connect(self._clear_value)
        self.pushApply.clicked.connect(self._apply_elements)

        self.pushMake.clicked.connect(self._make_file)
        # Combo
        self.comboComp.addItem('')
        for item in self.components:
            self.comboComp.addItem(item)
        self.comboComp.insertSeparator(len(self.components)+1)
        self.comboComp.addItem("Load")
        self.comboComp.currentTextChanged.connect(lambda: self._get_elements(self.comboComp.currentText()))

        # Element list
        self.actionParaDelete = QAction("Delete", self.listPara)
        self.actionParaDelete.triggered.connect(self._delete_element)
        self.listPara.addAction(self.actionParaDelete)

    def _load_convalgo(self):
        excel_extension = "Excel files (*.xls *.xlms)"
        fname = QFileDialog.getOpenFileName(self, filter = excel_extension)[0]
        if fname == "": return
        
        self.listConv.clear()
        self.elements = []
        
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
            parameter.load_parameter(key, str(s))
            self.convalgo.append(parameter)
            self.listConv.setItemWidget(para, parameter)
            self.listConv.addItem(para)
            para.setSizeHint(parameter.sizeHint())

    def _import_component(self):
        fname = QFileDialog.getOpenFileName(self, initialFilter = extension[0], filter='\n'.join(i for i in extension))[0]
        if fname == "": return
        lst = fname.split('/')
        name = lst[-1]
        path = '/'.join(i for i in lst)
        item = QListWidgetItem(self.listImport)
        f = self.Item()
        f.import_preset(name, path)
        self.listImport.setItemWidget(item, f)
        self.listImport.addItem(item)
        item.setSizeHint(f.sizeHint())

    def _get_elements(self, item):
        name = ""
        if item == "Load":
            name = QFileDialog.getOpenFileName(self, initialFilter = extension[0], filter='\n'.join(i for i in extension))[0]
        else:
            if not item == "":
                name = os.path.join(base_path,'data',item+'.tps')
        if name == "": return

        self.listPara.clear()
        self.elements = []
 
        with open(name,'r') as f:
            lines = f.readlines()
            maxlen = 1
            for line in lines:
                if line.startswith('#'): continue
                line = line.replace('\t','')
                line = line.split('=')
                if maxlen < len(line[0]): 
                    maxlen = len(line[0])

                if len(self.elements) > 1:
                    if any(line[0] == i.name for i in self.elements):
                        continue
                
                para = QListWidgetItem(self.listPara)
                parameter = self.Item()
                parameter.load_parameter(line[0], line[1])
                self.elements.append(parameter)
                idx = len(self.elements) - 1 
                self.listPara.setItemWidget(para, self.elements[idx])
                self.listPara.addItem(para)
                para.setSizeHint(parameter.sizeHint())

    def _set_element_name(self):
        return

    def _add_element(self):
        name = self.lineNewParaName.text()
        value = self.lineNewParaValue.text()
        if name == "": return
        for idx in range(len(self.elements)):
            if name == self.elements[idx].name:
                self.elements[idx].set_value(value)
                return
        para = QListWidgetItem(self.listPara)
        parameter = self.Item()
        parameter.load_parameter(name, value)
        self.elements.append(parameter)
        idx = len(self.elements) - 1
        self.listPara.setItemWidget(para, self.elements[idx])
        self.listPara.addItem(para)
        para.setSizeHint(parameter.sizeHint())
  
    def _delete_element(self):
        # self.listPara.currentItem()
        self.listPara.takeItem(self.listPara.currentRow())

    def _apply_elements(self):
        return

    def _clear_value(self):
        for idx in range(len(self.elements)):
            self.elements[idx].set_value(None)

    def _make_file(self):
        return

class PatientWindow(QDialog):
    def __init__(self, parent):
        super(PatientWindow, self).__init__(parent)
        uic.loadUi(os.path.join(base_path,'ui','patient.ui'), self)
        self.show()

class RunWindow(QDialog):
    def __init__(self, parent):
        super(RunWindow, self).__init__(parent)
        uic.loadUi(os.path.join(base_path,'ui','run.ui'), self)
        self.show()

    def _set_action(self):
        self.pushResubmit.clicked.connect(self._resubmit)
        self.pushLog.clicked.connect(self._log)

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._set_actions()
        self.show()

    def _set_actions(self):
        # Menubar
        ### File
        self.actionFileNew.triggered.connect(self._new_simulation)
        self.actionFileOpen.triggered.connect(self._open_cfg)
        self.actionFileSave.triggered.connect(self._save_cfg)
        self.actionExit.triggered.connect(qApp.quit)
        ### Component
        self.actionCompNew.triggered.connect(self._new_component)
        self.actionCompLoad.triggered.connect(self._load_component)
        self.actionCompSave.triggered.connect(self._save_component)
        self.actionCompModify.triggered.connect(self._modify_component)
        ### Patient
        self.actionPatientSetup.triggered.connect(self._patient_setup)
        self.actionPatientView.triggered.connect(self._patient_view)
        ### Simulation
        self.actionSimLoad.triggered.connect(self._simulation)
        ### Run
        self.actionRun = QAction(QIcon('../icons/run.png'), 'Run', self)
        self.actionRun.setShortcut('Ctrl+R')
        self.actionRun.setStatusTip('Run Topas simulation')
        self.actionRun.triggered.connect(self._run)

        # Toolbar
        self.toolBar.addAction(self.actionExit)
        self.toolBar.addSeparator()
        
        label = QLabel(" File: ")
        self.toolBar.addWidget(label)
        self.toolBar.addAction(self.actionFileNew)
        self.toolBar.addAction(self.actionFileOpen)
        self.toolBar.addAction(self.actionFileSave)
        self.toolBar.addSeparator()

        label = QLabel(" Component: ")
        self.toolBar.addWidget(label)
        self.toolBar.addAction(self.actionCompNew)
        #self.toolBar.addAction(self.actionCompLoad)
        #self.toolBar.addAction(self.actionCompSave)
        self.toolBar.addAction(self.actionCompModify)
        #self.toolBar.addAction(self.actionCompDelete)
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

    # Functions
    def _new_simulation(self):
        return 0

    def _open_cfg(self):
        return 0

    def _save_cfg(self):
        return 0

    def _new_component(self):
        ComponentWindow(self)

    def _load_component(self):
        return 0

    def _save_component(self):
        return 0

    def _modify_component(self):
        return 0

    def _add_component(self):
        return 0

    def _remove_component(self):
        return 0

    def _patient_setup(self):
        return 0

    def _patient_view(self):
        PatientWindow(self)

    def _simulation(self):
        sim = SimulationWindow(self)

    def _run(self):
        RunWindow(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
