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

        self.tick = 1 # mm
        self.selected_component = None
        self.field_count = 1

        self.widgetNozzle = Painter()
        self.gridLayout_2.addWidget(self.widgetNozzle,1,0)

        self.comp_to_table_map = {}
        self.macros = []

        self.container = Container()

        self.container.nozzle_type = None
        self.field_checklist = []
        self.container.fields = OrderedDict()
        self.container.components = OrderedDict()
        self.scorer_container = OrderedDict()
        self.filter_container = OrderedDict()
        self.ct_directory = ""

        self.set_icons()
        self.set_actions()

        self.show()

    def keyPressEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            if any(i == event.key() for i in [Qt.Key_Right, Qt.Key_Left, Qt.Key_Up, Qt.Key_Down]):
                self.move_component(event.key())
        elif event.modifiers() == Qt.ShiftModifier:
            if any(i == event.key() for i in [Qt.Key_Up, Qt.Key_Down]):
                self.modify_tick(event.key())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.position()
            widget = self.childAt(QPoint(pos.x(), pos.y()))
            if widget == self.widgetNozzle:
                self.selected_component = self.widgetNozzle.find_component(QPoint(pos.x(), pos.y()))
                self.update_statusbar()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.position()
            widget = self.childAt(QPoint(pos.x(), pos.y()))
            if widget == self.widgetNozzle:
                self.widgetNozzle.show3D(QPoint(pos.x(), pos.y()))
                self.update_statusbar()

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
        def run_locally(checkLocal):
            if checkLocal.isChecked():
                var.G_TOPAS_LOCAL = True
            else:
                var.G_TOPAS_LOCAL = False
        self.checkLocal.clicked.connect(lambda: run_locally(self.checkLocal))
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
        
        # Statusbar
        labelForMoving = QLabel(f"Component: {self.selected_component}, Tick: {self.tick} mm")
        self.statusbar.addPermanentWidget(labelForMoving)

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

        # Field parameters
        self.tabAddBtn = QToolButton()
        self.tabFields.setCornerWidget(self.tabAddBtn, Qt.TopRightCorner)
        self.tabFields.setContextMenuPolicy(Qt.ActionsContextMenu)
        actions = {"Delete":self.delete_field}
        for key, value in actions.items():
            action = QAction(key, self.tabFields)
            action.triggered.connect(value)
            self.tabFields.addAction(action)
        self.tabAddBtn.setAutoRaise(True)
        self.tabAddBtn.setIcon(QIcon(os.path.join(var.BASE_PATH,"icons/new.png")))
        self.tabAddBtn.clicked.connect(self.add_field)

        self.tabScorer.tabBar().setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

    def new_simulation(self):
        reply = QMessageBox.question(self, "Message", "Are you sure to remove all?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.clear_all()
        else:
            return

    # TODO
    def save_cfg(self):
        fname = QFileDialog.getSaveFileName(self, 'Save', os.path.join(var.BASE_PATH,'prod'), filter="Nozzle files (*.nzl)")[0]
        if not fname.endswith('.nzl'):
            fname = fname + '.nzl'
        fout = open(fname, 'w')
        fout.write(f"Nozzle: {self.container.nozzle_type}\n")
        for name, component in self.container.components.items():
            fulltext = component.fulltext().split('\n')
            for idx, text in enumerate(fulltext):
                fulltext[idx] = '  ' + text
            fulltext = '\n'.join(t for t in fulltext)
            fout.write(f"{name}: >\n{fulltext}\n\n")
        fout.close()

    def open_cfg(self):
        fname = QFileDialog.getOpenFileName(self, 'Open', os.path.join(var.BASE_PATH,'data'), filter = "Nozzle files (*.nzl)")[0]
        if fname == '' or fname is None: return
        if not fname.endswith('.nzl'): return
        with open(fname, 'r') as f:
            self.clear_all()
            cfg = yaml.load(f, Loader=yaml.FullLoader)
        
        self.container.nozzle_type = int(cfg['Nozzle'])
        if self.container.nozzle_type == var.FBRT1: self.radioFBRT1.setChecked(True)
        if self.container.nozzle_type == var.GTR2: self.radioGTR2.setChecked(True)
        if self.container.nozzle_type == var.GTR3: self.radioGTR3.setChecked(True)

        if self.tabFields.count() == 0:
            self.add_field()

        for name, filename in cfg.items():
            if name == 'Nozzle': continue
            component = Component(filename=name)
            component.get_variables_from_textfile(filename=filename, initialize=True)
            self.container.components[name] = component

        self.update_geometry()

    def clear_all(self):
        self.container.nozzle_type = None

        for key in self.container.components.keys():
            del self.container.components[key]
        for key in self.container.fields.keys():
            del self.container.fields[key]
        for key in self.scorer_container.keys():
            del self.scorer_container[key]
        for key in self.filter_container.keys():
            del self.filter_container[key]

        self.radioFBRT1.setCheckable(False)
        self.radioGTR2.setCheckable(False)
        self.radioGTR3.setCheckable(False)
        self.radioFBRT1.setCheckable(True)
        self.radioGTR2.setCheckable(True)
        self.radioGTR3.setCheckable(True)

        self.listComponents.clear()

        self.tabFields.clear()

        self.tableComp.setRowCount(0)
        self.widgetNozzle.trigger_refresh(self.container.components.values())

    def update_geometry(self):
        if not self.check_beam_mode(): return
        if len(self.container.components) < 1: return

        self.listComponents.clear()
        self.tableComp.setRowCount(0)

        for name, component in self.container.components.items():
            item = QListWidgetItem(self.listComponents)
            f = Item()
            f.add_label(name)
            self.listComponents.setItemWidget(item, f)
            self.listComponents.addItem(item)
            item.setSizeHint(f.sizeHint())
            geometry_info = component.get_geometry()

            row_count = self.tableComp.rowCount()
            self.tableComp.setRowCount(row_count + 1)
            row = self.tableComp.rowCount()
            self.tableComp.setItem(row-1, 0, QTableWidgetItem(str(name)))
            self.tableComp.setItem(row-1, 1, QTableWidgetItem(str(geometry_info['Type'])))

            for icol in range(self.tableComp.columnCount()):
                colname = self.tableComp.horizontalHeaderItem(icol).text()
                if colname in geometry_info.keys():
                    value = geometry_info[colname]
                    self.tableComp.setItem(row-1, icol, QTableWidgetItem(str(value)))

        self.tableComp.resizeColumnsToContents()
        self.widgetNozzle.trigger_refresh(self.container.components.values())

    def new_component(self):
        if not self.check_beam_mode(): return

        cwindow = ComponentWindow(self.container.nozzle_type)
        r = cwindow.return_para()
        if r:
            self.container.components[cwindow.component.file_name] = cwindow.component
        
        self.update_geometry()

    def modify_component(self):
        if not self.check_beam_mode(): return

        text = None
        item = self.listComponents.currentItem()
        if item is not None:
            label_widget = self.listComponents.itemWidget(item)
            label = label_widget.get_label()
            text = label.text()
        
        component = self.container.components.pop(text)

        cwindow = ComponentWindow(self.container.nozzle_type)
        cwindow.load(component)
        r = cwindow.return_para()
        if r:
            self.container.components[cwindow.component.file_name] = cwindow.component
        self.update_geometry()

    def delete_component(self):
        if not self.check_beam_mode(): return

        text = None
        item = self.listComponents.currentItem()
        if item is not None:
            label_widget = self.listComponents.itemWidget(item)
            label = label_widget.get_label()
            text = label.text()

        self.container.components.pop(text)
        item = self.listComponents.takeItem(self.listComponents.currentRow())
        del item
        self.update_geometry()

    def add_field(self, reset=False):
        widget = QWidget()
        gridlayout = QGridLayout(widget)
        if self.container.nozzle_type == var.FBRT1:
            parameters = ['1st Scatterer', '2nd Scatterer', 'Range Modulator', 'Stop Position', 'Beam Energy', 'Range in patients', 'SOBP', 'SSD', 'BCM']
        elif self.container.nozzle_type == var.GTR2:
            parameters = ['1st Scatterer', '2nd Scatterer', 'Range Modulator', 'Stop Position', 'Beam Energy', 'Range in patients', 'SOBP', 'SSD', 'BCM']
        elif self.container.nozzle_type == var.GTR3:
            parameters = ['Beam Energy']
        else:
            return

        if reset:
            self.tabFields.clear()
            self.container.fields.clear()

        field_name = f"Field{self.field_count}"
        self.field_count += 1
        self.container.fields[field_name] = {para:[] for para in parameters}

        def update_parameter(tab):
            field = tab.tabText(tab.currentIndex())
            field_number = tab.currentIndex() + 1
            layout = tab.currentWidget().layout()
            for irow in range(layout.rowCount()):
                name = layout.itemAtPosition(irow, 0).widget().text()
                value = layout.itemAtPosition(irow, 1).widget().text()
                value = re.sub(r'\s+', ' ', value)
                items = [item for item in re.split('[,;.\s]', value) if item != ""]
                self.container.fields[field][name] = items
                    
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
            line.textChanged.connect(lambda: update_parameter(self.tabFields))
            line.returnPressed.connect(lambda: update_parameter(self.tabFields))

        self.tabFields.addTab(widget, field_name)
        self.tabFields.setCurrentIndex(self.tabFields.count()-1)

    def delete_field(self):
        current_index = self.tabFields.currentIndex()
        current_name = self.tabFields.tabText(current_index)
        del self.container.fields[current_name]
        self.tabFields.removeTab(current_index)

    # TODO
    def new_scorer(self):
        if not self.check_beam_mode(): return
        
        scorer = ScorerWindow(self, self.container.nozzle_type, len(self.container.fields.keys()), self.container.components.keys())
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

    # TODO
    def update_scorer(self):
        if len(self.scorer_container) < 1: return
        for run, scorers in self.scorer_container.items():
            widget = QWidget()
            vblayout = QVBoxLayout(widget)

            for idx, scorer in enumerate(scorers):
                for idx2, name in enumerate(scorer.subcomponent.keys()):
                    if name == "Basis": continue
                    label = QLabel(name)
                    vblayout.addWidget(label)

        
            if len(self.filter_container) > 0:
                filters = self.filter_container[run]
                for idx, filter in enumerate(filters):
                    if filter is not None:
                        label = QLabel(filter['name'])
                        vblayout.addWidget(label)
            vblayout.addStretch(1)

            self.tabScorer.addTab(widget, f"{run}")
            self.tabScorer.setCurrentIndex(self.tabScorer.count()-1)

    # Functions
    def set_beam_mode(self, ngtr):
        if self.container.nozzle_type == ngtr: return
        else:
            self.container.nozzle_type = ngtr

        if self.tabFields.count() == 0:
            self.add_field()
        else:
            self.add_field(reset=True)

    def check_beam_mode(self):
        if self.container.nozzle_type is None:
            QMessageBox.warning(self, "Warning", "Please, select nozzle type")
            return False
        else:
            return True

    def run(self):
        if not self.check_beam_mode(): return
        run = RunWindow(self.outdir, self.container.nozzle_type, self.field_checklist, self.container.fields, self.container.components, self.scorer_container, self.filter_container)
        run.show()
        r = run.return_para()
        if r:
            del run

    # TODO!
    def find_component(self, x, y):
        pass

    def update_statusbar(self):
        pass

    def move_component(self, key):
        pass

    def modify_tick(self, key):
        pass