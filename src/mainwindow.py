import yaml

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
from src.simulationwindow import SimulationWindow
from src.runwindow import RunWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.widgetNozzle = Painter()
        self.gridLayout_2.addWidget(self.widgetNozzle,1,0)

        self.comp_to_table_map = {}
        self.macros = []

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
        self.actionTempNew.setIcon(new)
        self.actionTempModify.setIcon(write)
        self.actionTempDelete.setIcon(delete)
        self.actionCompAdd.setIcon(new)
        self.actionCompModify.setIcon(write)
        self.actionCompDelete.setIcon(delete)
        self.actionPatientSetup.setIcon(opn)
        self.actionPatientView.setIcon(view)
        self.actionSimLoad.setIcon(opn)

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

        # Parameters
        self.tabAddBtn = QToolButton()
        self.tabParameters.setCornerWidget(self.tabAddBtn, Qt.TopRightCorner)
        self.tabAddBtn.setAutoRaise(True)
        self.tabAddBtn.setIcon(QIcon(os.path.join(var.BASE_PATH,"icons/new.png")))
        self.tabAddBtn.clicked.connect(self.add_field)

        # Component
        self.tableComp.setEditTriggers(QAbstractItemView.NoEditTriggers)
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
        previous = var.G_NOZZLE_TYPE
        if self.radioScattering.isChecked(): var.G_NOZZLE_TYPE = "scattering"
        if self.radioScanning.isChecked(): var.G_NOZZLE_TYPE = "scanning"
        if self.tabParameters.count() == 0:
            self.add_field()
        if previous != var.G_NOZZLE_TYPE:
            self.add_field(reset=True)

    def check_beam_mode(self):
        if var.G_NOZZLE_TYPE is None:
            QMessageBox.warning(self, "Warning", "Please, select nozzle type")
            return False
        else:
            return True

    def clear_all(self):
        var.G_NOZZLE_TYPE = None
        var.G_TEMPLATE = []
        var.G_COMPONENT = []
        var.G_PATIENT = Patient()
        var.G_PHASE = {}
        var.G_PARAMETER = {}

        self.radioScattering.setCheckable(False)
        self.radioScanning.setCheckable(False)
        self.radioScattering.setCheckable(True)
        self.radioScanning.setCheckable(True)

        self.listTemplates.clear()

        self.tabParameters.clear()

        self.tableComp.setRowCount(0)
        self.widgetNozzle.trigger_refresh()

        self.linePatientDir.clear()
        self.listPatientCT.clear()
        self.lineRTS.clear()
        self.lineRTP.clear()
        self.lineRD.clear()
        self.lineMacro.clear()

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
        fout.write(f"Nozzle: {var.G_NOZZLE_TYPE}\n")
        for component in var.G_COMPONENT:
            fulltext = component.fulltext().split('\n')
            for idx, text in enumerate(fulltext):
                fulltext[idx] = '  ' + text
            fulltext = '\n\n'.join(t for t in fulltext)
            fout.write(f"{component.name}: >\n{fulltext}\n\n")
        fout.close()

    def open_cfg(self):
        fname = QFileDialog.getOpenFileName(self, 'Open', os.path.join(var.BASE_PATH,'prod'), filter = "Nozzle files (*.nzl)")[0]
        if fname == '' or fname is None: return
        if not fname.endswith('.nzl'): return
        with open(fname, 'r') as f:
            self.clear_all()
            cfg = yaml.load(f, Loader=yaml.FullLoader)
        var.G_NOZZLE_TYPE = cfg['Nozzle'].lower()
        if var.G_NOZZLE_TYPE == 'scattering': self.radioScattering.setChecked(True)
        elif var.G_NOZZLE_TYPE == 'scanning': self.radioScanning.setChecked(True)
        if self.tabParameters.count() == 0:
            self.add_field()

        for name, text in cfg.items():
            if name == 'Nozzle': continue
            component = Component(var.G_NOZZLE_TYPE)
            component.load(text, load=True, draw_all=True)
            component.name = name
            var.G_TEMPLATE.append(component)
            item = QListWidgetItem(self.listTemplates)
            f = Item()
            f.add_label(component.name)
            self.listTemplates.setItemWidget(item, f)
            self.listTemplates.addItem(item)
            item.setSizeHint(f.sizeHint())
            self.add_component()

    def generate_template(self, name, idx=-999):
        replace = False
        if any(name == i.name for i in var.G_TEMPLATE[:-1]):
            reply = QMessageBox.question(self, "Message", f'Are you sure to replace {name}?',
              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                replace = True
            else:
                return

        if replace:
            item = self.listTemplates.itemWidget(self.listTemplates.item(idx))
            item.name = name
            item.label.setText(name)
        else:
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
            template = var.G_TEMPLATE[-1]
            self.generate_template(template.name)

    def modify_template(self):
        if not self.check_beam_mode(): return
        if len(var.G_TEMPLATE) < 1: return
        idx = self.listTemplates.currentRow()

        template = ComponentWindow(self, fname=idx)
        r = template.return_para()
        if r:
            template = var.G_TEMPLATE[-1]
            var.G_TEMPLATE[idx] = template
            del var.G_TEMPLATE[-1]
            self.generate_template(template.name, idx)
    
    def delete_template(self):
        if not self.check_beam_mode(): return

        if len(var.G_TEMPLATE) < 1: return
        idx = self.listTemplates.currentRow()
        var.G_TEMPLATE.pop(idx)      
        self.listTemplates.takeItem(idx)

    def add_field(self, reset=False):
        widget = QWidget()
        gridlayout = QGridLayout(widget)
        if var.G_NOZZLE_TYPE == 'scattering':
            parameters = ['1st Scatterer', '2nd Scatterer', 'Range Modulator', 'Stop Position', 'Beam Energy', 'Range in patients', 'SOBP', 'SSD', 'BCM']
        elif var.G_NOZZLE_TYPE == 'scanning':
            parameters = ['Beam Energy']
        else:
            return

        if reset:
            self.tabParameters.clear()
            var.G_PARAMETER = {}

        var.G_PARAMETER[len(var.G_PARAMETER)] = {para:[] for para in parameters}

        def update_parameter(tab):
            field_number = tab.currentIndex()
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
                var.G_PARAMETER[field_number][name] = []
                for val in value:
                    val = val.replace(',','').replace(';','').replace(' ','')
                    if any(i == val for i in ['',' ',';','\n']): continue
                    var.G_PARAMETER[field_number][name].append(val)

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

        self.tabParameters.addTab(widget, f"Field{len(var.G_PARAMETER)}")
        self.tabParameters.setCurrentIndex(self.tabParameters.count()-1)

    def add_component(self):
        if not self.check_beam_mode(): return

        template_id = self.listTemplates.currentRow()
        if len(var.G_TEMPLATE) < template_id: return

        replace = False
        if len(var.G_COMPONENT) > 1:
            if any(var.G_TEMPLATE[template_id].name == i.name for i in var.G_COMPONENT):
                reply = QMessageBox.question(self, "Message", f'Are you sure to replace {var.G_TEMPLATE[template_id].name}?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    replace = True
                else:
                    return

        if replace and len(var.G_COMPONENT) > 1:
            for idx, component in enumerate(var.G_COMPONENT):
                if var.G_TEMPLATE[template_id].name == component.name:
                    component_id = idx
                    break
            var.G_COMPONENT[component_id] = var.G_TEMPLATE[template_id]
        else:
            component_id = -1
            var.G_COMPONENT.append(var.G_TEMPLATE[template_id])
            var.G_COMPONENT[-1].outname = os.path.join(var.G_OUTDIR, 'nozzle', var.G_COMPONENT[-1].name+'.tps')
            component_id = len(var.G_COMPONENT) - 1

        component = var.G_COMPONENT[component_id]
        component_table = []
        for subname, subcomp in component.subcomponent.items():
            info = {'Name':'','Component':'','Parent':'',
                    'HLX':"0.0 mm",'HLY':"0.0 mm",'HLZ':"0.0 mm",
                    'RMin':"0.0 mm",'RMax':"0.0 mm",
                    'HL':"0.0 mm", 'SPhi':"0.0 deg", 'DPhi':"0.0 deg",
                    'RotX':"0.0 deg",'RotY':"0.0 deg",'RotZ':"0.0 deg",
                    'TransX':"0.0 mm",'TransY':"0.0 mm",'TransZ':"0.0 mm"}
            if subname == 'Basis':
                info['Name'] = component.name
                info['Component'] = component.ctype
            else:
                info['Name'] = f'└─{subcomp.name}'
                info['Component'] = subcomp.name
            for para in subcomp.parameters:
                if any(para.name.lower() == i.lower() for i in info.keys()):
                    info[para.name] = para.value
            component_table.append(info)

        if replace:
            row_start_id = -999
            for irow in range(self.tableComp.rowCount()):
                rowname = self.tableComp.item(irow,0).text()
                if rowname == component.name:
                    row_start_id = irow
                    break
        else:
            row_start_id = self.tableComp.rowCount()

        map_length = len(self.comp_to_table_map)
        for irow in range(row_start_id, row_start_id+len(component_table)):
            if not replace:
                self.tableComp.setRowCount(row_start_id + len(component_table))
            self.comp_to_table_map[irow] = component_id
            table_id = irow - row_start_id
            for icol in range(self.tableComp.columnCount()):
                colname = self.tableComp.horizontalHeaderItem(icol).text()
                value = component_table[table_id][colname]
                self.tableComp.setItem(irow, icol, QTableWidgetItem(str(value)))
        self.tableComp.resizeColumnsToContents()
        self.widgetNozzle.trigger_refresh()

    def modify_component(self, delete=False):
        if not self.check_beam_mode(): return

        if len(var.G_COMPONENT) < 1: return
        row = self.tableComp.currentRow()
        idx = self.comp_to_table_map[row]

        if delete:
            keys = list(var.G_COMPONENT[idx].subcomponent.keys())
            length = len(keys)
            for key in keys:
                var.G_COMPONENT[idx].modify_subcomponent(key, {}, delete=True)
        else:
            component = ComponentWindow(self, fname=idx, modify_component=True)
            r = component.return_para()
            if not r:
                return
        
        rowmin = 999
        rowmax = -999
        for key, value in self.comp_to_table_map.items():
            if not value == idx: continue
            if rowmin > key: rowmin = key
            if rowmax < key: rowmax = key

        table_length = rowmax - rowmin + 1
        while table_length != len(var.G_COMPONENT[idx].subcomponent):
            for irow in range(rowmin, rowmax+1):
                cname = self.tableComp.item(irow, 0).text()
                if not '└─' in cname:
                    cname = 'Basis'
                else:
                    cname = cname.replace('└─','')
                if not cname in var.G_COMPONENT[idx].subcomponent:
                    target = irow
                    break

            self.tableComp.removeRow(target)
            del(self.comp_to_table_map[target])
            new = {}
            for key in list(self.comp_to_table_map.keys()):
                if key < target:
                    new[key] = self.comp_to_table_map[key]
                else:
                    new[key-1] = self.comp_to_table_map[key]
            self.comp_to_table_map = new

            rowmin = 999
            rowmax = -999
            match = False
            for key, value in self.comp_to_table_map.items():
                if not value == idx: continue
                if rowmin > key: 
                    rowmin = key
                    match = True
                if rowmax < key: 
                    rowmax = key
                    match = True
            table_length = rowmax - rowmin + 1
            if not match:
                rowmin = 0
                rowmax = 0
                table_length = 0

        new = {}
        for key in sorted(self.comp_to_table_map):
            if delete:
                new[key] = self.comp_to_table_map[key] - 1
            else:
                new[key] = self.comp_to_table_map[key]
        self.comp_to_table_map = new
        if delete:
            del var.G_COMPONENT[idx]
        else:
            for irow in range(rowmin, rowmax+1):
                name = self.tableComp.item(irow, 1).text().replace('└─','')
                if not name in var.G_COMPONENT[idx].subcomponent:
                    subcomp = var.G_COMPONENT[idx].subcomponent['Basis']
                else:
                    subcomp = var.G_COMPONENT[idx].subcomponent[name]
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
        self.modify_component(delete=True)

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
