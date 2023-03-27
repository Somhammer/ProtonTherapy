import datetime
import yaml
from collections import OrderedDict

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

import src.variables as var
from src.data import *

from src.ui_mainwindow import Ui_MainWindow

from src.painter import *
from src.item import *

from src.componentwindow import ComponentWindow
from src.patientwindow import PatientWindow
from src.runwindow import RunWindow
from src.scorerwindow import ScorerWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        today =  datetime.datetime.now().strftime("%y%m%d")
        self.outdir = os.path.join(var.BASE_PATH, 'prod', today)

        self.widgetNozzle = Painter()
        self.gridLayout_2.addWidget(self.widgetNozzle,1,0)

        self.comp_to_table_map = {}
        self.macros = []

        self.nozzle_type = None
        self.field_container = OrderedDict()
        self.nozzle_container = OrderedDict()
        self.scorer_container = OrderedDict()
        self.filter_container = OrderedDict()
        self.ct_directory = ""

        self.set_icons()
        self.set_actions()

        self.show()

    def set_icons(self):
        # Remove this function when coding is completed.
        icon_dir = os.path.join(var.BASE_PATH,'icons')
        ncc = QIcon(os.path.join(icon_dir, 'ncc.png'))
        ext = QIcon(os.path.join(icon_dir, 'exit.png'))
        new = QIcon(os.path.join(icon_dir, 'new.png'))
        opn = QIcon(os.path.join(icon_dir, 'open.png'))
        save = QIcon(os.path.join(icon_dir, 'save.png'))
        write = QIcon(os.path.join(icon_dir, 'write.png'))
        delete = QIcon(os.path.join(icon_dir, 'delete.png'))
        view = QIcon(os.path.join(icon_dir, 'view.png'))
        run = QIcon(os.path.join(icon_dir, 'run.png'))
        
        self.setWindowIcon(QIcon(os.path.join(icon_dir, 'ncc.png')))
        self.actionFileNew.setIcon(new)
        self.actionFileOpen.setIcon(opn)
        self.actionFileSave.setIcon(save)
        self.actionExit.setIcon(ext)

        self.actionCompNew.setIcon(new)
        self.actionCompModify.setIcon(write)
        self.actionCompDelete.setIcon(delete)
        self.actionScorerNew.setIcon(new)
        self.actionScorerModify.setIcon(write)
        self.actionScorerDelete.setIcon(delete)
        self.actionSimLoad.setIcon(opn)

    def set_actions(self):
        # File
        self.actionFileNew.triggered.connect(self.new_simulation)
        self.actionFileOpen.triggered.connect(self.open_cfg)
        self.actionFileSave.triggered.connect(self.save_cfg)
        self.actionExit.triggered.connect(QCoreApplication.quit)
        # Component
        self.actionCompNew.triggered.connect(self.new_component)
        self.actionCompModify.triggered.connect(self.modify_component)
        self.actionCompDelete.triggered.connect(self.delete_component)
        # Scorer
        self.actionScorerNew.triggered.connect(self.new_scorer)
        #self.actionScorerModify.setIcon(write)
        #self.actionScorerDelete.setIcon(delete)
        ### Simulation
        #self.actionSimLoad.triggered.connect(self.simulation)
        ### Run
        self.actionRun = QAction(QIcon(os.path.join(var.BASE_PATH,'icons/run.png')), 'Run', self)
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
        
        label = QLabel(" Component: ")
        self.toolBar.addWidget(label)
        self.toolBar.addAction(self.actionCompNew)
        self.toolBar.addAction(self.actionCompModify)
        self.toolBar.addAction(self.actionCompDelete)
        self.toolBar.addSeparator()

        label = QLabel(" Scorer: ")
        self.toolBar.addWidget(label)
        self.toolBar.addAction(self.actionScorerNew)
        self.toolBar.addAction(self.actionScorerModify)
        self.toolBar.addAction(self.actionScorerDelete)
        self.toolBar.addSeparator()

        self.toolBar.addAction(self.actionRun)
        self.toolBar.setIconSize(QSize(32,32))
        
        # Nozzle Mode
        self.radioFBRT1.clicked.connect(lambda: self.set_beam_mode(var.FBRT1))
        self.radioGTR2.clicked.connect(lambda: self.set_beam_mode(var.GTR2))
        self.radioGTR3.clicked.connect(lambda: self.set_beam_mode(var.GTR3))

        # Components
        self.listComponents.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.listComponents.addAction(self.actionCompModify)
        self.listComponents.addAction(self.actionCompDelete)
        #self.listComponents.itemDoubleClicked.connect(self.action)
        self.tableComp.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableComp.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.tableComp.addAction(self.actionCompModify)
        self.tableComp.addAction(self.actionCompDelete)
        self.tableComp.itemDoubleClicked.connect(self.modify_component)

        # Parameters
        #self.pushConValgo.clicked.connect(self.load_convalgo)

        # Field parameters
        self.tabAddBtn = QToolButton()
        self.tabParameters.setCornerWidget(self.tabAddBtn, Qt.TopRightCorner)
        self.tabAddBtn.setAutoRaise(True)
        self.tabAddBtn.setIcon(QIcon(os.path.join(var.BASE_PATH,"icons/new.png")))
        self.tabAddBtn.clicked.connect(self.add_field)

        # Patient
        self.listPatientCT.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.listPatientCT.addAction(self.actionPatientView)
        self.listPatientCT.itemDoubleClicked.connect(self.patient_view)

    def new_simulation(self):
        reply = QMessageBox.question(self, "Message", "Are you sure to remove all?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.clear_all()
        else:
            return

    def save_cfg(self):
        fname = QFileDialog.getSaveFileName(self, 'Save', os.path.join(var.BASE_PATH,'prod'), filter="Nozzle files (*.nzl)")[0]
        if not fname.endswith('.nzl'):
            fname = fname + '.nzl'
        fout = open(fname, 'w')
        fout.write(f"Nozzle: {self.nozzle_type}\n")
        for name, component in self.nozzle_container.items():
            fulltext = component.fulltext().split('\n')
            for idx, text in enumerate(fulltext):
                fulltext[idx] = '  ' + text
            fulltext = '\n'.join(t for t in fulltext)
            fout.write(f"{name}: >\n{fulltext}\n\n")
        fout.close()

    def open_cfg(self):
        fname = QFileDialog.getOpenFileName(self, 'Open', os.path.join(var.BASE_PATH,'prod'), filter = "Nozzle files (*.nzl)")[0]
        if fname == '' or fname is None: return
        if not fname.endswith('.nzl'): return
        with open(fname, 'r') as f:
            self.clear_all()
            cfg = yaml.load(f, Loader=yaml.FullLoader)
        
        self.nozzle_type = int(cfg['Nozzle'])
        if self.nozzle_type == var.FBRT1: self.radioFBRT1.setChecked(True)
        if self.nozzle_type == var.GTR2: self.radioGTR2.setChecked(True)
        if self.nozzle_type == var.GTR3: self.radioGTR3.setChecked(True)

        if self.tabParameters.count() == 0:
            self.add_field()

        for name, text in cfg.items():
            if name == 'Nozzle': continue
            component = Component(self.nozzle_type)
            component.load(text, load=True, draw_all=True)
            component.name = name
            self.nozzle_container[name] = component

        self.update_geometry()

    def clear_all(self):
        self.nozzle_type = None
        for key in self.nozzle_container.keys():
            del self.nozzle_container[key]
        for key in self.field_container.keys():
            del self.field_container[key]
        for key in self.scorer_container.keys():
            del self.scorer_container[key]
        self.radioFBRT1.setCheckable(False)
        self.radioGTR2.setCheckable(False)
        self.radioGTR3.setCheckable(False)
        self.radioFBRT1.setCheckable(True)
        self.radioGTR2.setCheckable(True)
        self.radioGTR3.setCheckable(True)

        self.listComponents.clear()

        self.tabParameters.clear()

        self.tableComp.setRowCount(0)
        self.widgetNozzle.trigger_refresh(self.nozzle_container.values())

        self.linePatientDir.clear()
        self.listPatientCT.clear()
        self.lineRTS.clear()
        self.lineRTP.clear()
        self.lineRD.clear()
        self.lineMacro.clear()

    def update_geometry(self):
        if not self.check_beam_mode(): return
        if len(self.nozzle_container) < 1: return

        self.listComponents.clear()
        self.tableComp.setRowCount(0)

        for name, component in self.nozzle_container.items():
            item = QListWidgetItem(self.listComponents)
            f = Item()
            f.add_label(name)
            self.listComponents.setItemWidget(item, f)
            self.listComponents.addItem(item)
            item.setSizeHint(f.sizeHint())

            geometry_info = {'Name':'','Component':'','Parent':'',
                        'HLX':"0.0 mm",'HLY':"0.0 mm",'HLZ':"0.0 mm",
                        'RMin':"0.0 mm",'RMax':"0.0 mm",
                        'HL':"0.0 mm", 'SPhi':"0.0 deg", 'DPhi':"0.0 deg",
                        'RotX':"0.0 deg",'RotY':"0.0 deg",'RotZ':"0.0 deg",
                        'TransX':"0.0 mm",'TransY':"0.0 mm",'TransZ':"0.0 mm"}
            for subname, subcomp in component.subcomponent.items():
                if subname == 'Basis': 
                    geometry_info['Name'] = component.name
                    geometry_info['Component'] = component.ctype
                    for para in subcomp.parameters:
                        if any(para.name.lower() == i.lower() for i in geometry_info.keys()):
                            geometry_info[para.name] = para.value

            row_count = self.tableComp.rowCount()
            self.tableComp.setRowCount(row_count + 1)
            row = self.tableComp.rowCount()
            for icol in range(self.tableComp.columnCount()):
                colname = self.tableComp.horizontalHeaderItem(icol).text()
                value = geometry_info[colname]
                self.tableComp.setItem(row-1, icol, QTableWidgetItem(str(value)))
        self.tableComp.resizeColumnsToContents()
        self.widgetNozzle.trigger_refresh(self.nozzle_container.values())

    def new_component(self):
        if not self.check_beam_mode(): return

        component = ComponentWindow(self.nozzle_type)
        component.show()
        r = component.return_para()
        if r:
            if component.nozzle_component is not None:
                self.nozzle_container[component.nozzle_component.name] = component.nozzle_component
        self.update_geometry()

    def modify_component(self):
        if not self.check_beam_mode(): return

        text = None
        item = self.listComponents.currentItem()
        idx = self.listComponents.currentRow()
        if item is not None:
            label_widget = self.listComponents.itemWidget(item)
            label = label_widget.get_label()
            text = label.text()
        
        component = ComponentWindow(self)
        component.template = self.nozzle_container[text]
        component.show(True)
        r = component.return_para()
        if r:
            if component.nozzle_component is not None:
                self.nozzle_container.pop(text)
                self.nozzle_container[text] = component.nozzle_component
        self.update_geometry()

    def delete_component(self):
        if not self.check_beam_mode(): return

        text = None
        item = self.listComponents.currentItem()
        idx = self.listComponents.currentRow()
        if item is not None:
            label_widget = self.listComponents.itemWidget(item)
            label = label_widget.get_label()
            text = label.text()

        self.nozzle_container.pop(text)

        self.update_geometry()

    def add_field(self, reset=False):
        widget = QWidget()
        gridlayout = QGridLayout(widget)
        if self.nozzle_type == var.FBRT1:
            parameters = ['1st Scatterer', '2nd Scatterer', 'Range Modulator', 'Stop Position', 'Beam Energy', 'Range in patients', 'SOBP', 'SSD', 'BCM']
        elif self.nozzle_type == var.GTR2:
            parameters = ['1st Scatterer', '2nd Scatterer', 'Range Modulator', 'Stop Position', 'Beam Energy', 'Range in patients', 'SOBP', 'SSD', 'BCM']
        elif self.nozzle_type == var.GTR3:
            parameters = ['Beam Energy']
        else:
            return

        if reset:
            self.tabParameters.clear()
            self.field_container.clear()

        self.field_container[f"Field{len(self.field_container)+1}"] = {para:[] for para in parameters}

        def update_parameter(tab):
            field = tab.tabText(tab.currentIndex())
            #field_number = tab.currentIndex() + 1
            layout = tab.currentWidget().layout()
            for irow in range(layout.rowCount()):
                label = layout.itemAtPosition(irow, 0).widget()
                name = layout.itemAtPosition(irow, 0).widget().text()
                value = layout.itemAtPosition(irow, 1).widget().text()
                delimiter = ''
                if ',' in value:
                    delimiter = ','
                elif ' ' in value:
                    delimiter = ' '
                elif ';' in value:
                    delimiter = ';'
                else:
                    delimiter = '\n'
                value = value.split(delimiter)
                self.field_container[field][name] = []
                for val in value:
                    val = val.replace(',','').replace(';','').replace(' ','')
                    if any(i == val for i in ['',' ',';','\n']): continue
                    self.field_container[field][name].append(val)

        for idx, para in enumerate(parameters):
            label = QLabel(para)
            line = QLineEdit()
            gridlayout.addWidget(label, idx, 0, 1, 1)
            if 'energy' in para.lower():
                label2 = QLabel('MeV')
                gridlayout.addWidget(line, idx, 1, 1, 1)
                gridlayout.addWidget(label2, idx, 2)
            else:
                gridlayout.addWidget(line, idx, 1, 1, 2)
            line.textChanged.connect(lambda: update_parameter(self.tabParameters))
            line.returnPressed.connect(lambda: update_parameter(self.tabParamters))

        self.tabParameters.addTab(widget, f"Field{len(self.field_container)}")
        self.tabParameters.setCurrentIndex(self.tabParameters.count()-1)

    def update_scorer(self):
        if len(self.scorer_container) < 1: return
        for run, scorers in self.scorer_container.items():
            widget = QWidget()
            gridlayout = QGridLayout(widget)

            for idx, scorer in enumerate(scorers):
                for idx2, name in enumerate(scorer.subcomponent.keys()):
                    if name == "Basis": continue
                    label = QLabel(name)
                    print("Label:", label.text())
                    gridlayout.addWidget(label, idx2, 0, 1, 1)
        
            if len(self.filter_container) > 0:
                filters = self.filter_container[run]
                for idx, filter in enumerate(filters):
                    if filter is not None:
                        label = QLabel(filter['name'])
                        gridlayout.addWidget(label, idx2+idx, 0, 1, 1)

            self.tabScorer.addTab(widget, f"{run}")
            self.tabScorer.setCurrentIndex(self.tabScorer.count()-1)

    def new_scorer(self):
        if not self.check_beam_mode(): return
        
        scorer = ScorerWindow(self, self.nozzle_type, len(self.field_container.keys()), self.nozzle_container.keys())
        scorer.show()
        r = scorer.return_para()
        if r:
            self.scorer_container = OrderedDict(scorer.scorer_container)
            self.filter_container = OrderedDict(scorer.filter_container)
            self.field_checklist = OrderedDict(scorer.field_checklist)

        # TODO
        # Update scorer geometry
        self.update_scorer()
        self.update_geometry()

    # Functions
    def set_beam_mode(self, ngtr):
        if self.nozzle_type == ngtr: return
        else:
            self.nozzle_type = ngtr

        if self.tabParameters.count() == 0:
            self.add_field()
        else:
            self.add_field(reset=True)

    def check_beam_mode(self):
        if self.nozzle_type is None:
            QMessageBox.warning(self, "Warning", "Please, select nozzle type")
            return False
        else:
            return True
    
    def patient_setup(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Patient CT directory")
        if directory == "": return
        var.G_PATIENT.patient_setup(directory)
        self.linePatientDir.setText(var.G_PATIENT.directory)
        for f in var.G_PATIENT.CT:
            self.listPatientCT.addItem(QListWidgetItem(str(f)))
        self.lineRTS.setText(var.G_PATIENT.RTS)
        self.lineRTP.setText(var.G_PATIENT.RTP)
        self.lineRD.setText(var.G_PATIENT.RD)
        
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
            self.linePatientDir.setText(var.G_PATIENT.directory)
            self.listPatientCT.clear()
            for f in var.G_PATIENT.CT:
                self.listPatientCT.addItem(QListWidgetItem(str(f)))
            self.lineRTS.setText(var.G_PATIENT.RTS)
            self.lineRTP.setText(var.G_PATIENT.RTP)
            self.lineRD.setText(var.G_PATIENT.RD)

    def run(self):
        if not self.check_beam_mode(): return
        run = RunWindow(self.outdir, self.nozzle_type, self.field_checklist, self.field_container, self.nozzle_container, self.scorer_container, self.filter_container)
        run.show()
        r = run.return_para()
        if r:
            del run

    def load_convalgo(self):
        pass
        """
        fname = QFileDialog.getOpenFileName(self, filter = var.G_EXCEL_EXTENSION[0])[0]
        if fname == '': return
    
        #if self.nozzle_type is not var.FBRT1: return
        # FIXME
        #setup_convalgo(fname=fname)

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
        """