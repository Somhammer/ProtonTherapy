import yaml
import copy

from PySide6.QtWidgets import *
from PySide6.QtCore import *

from src.variables import *
from src.data import *

from src.ui_scorerwindow import Ui_ScorerWindow
from src.data import *
from src.painter import *
from src.item import *
from src.classreader import Proton
from src.modifyparameter import ModifyParameter

class ScorerWindow(QDialog, Ui_ScorerWindow):
    def __init__(self, outdir, nozzle_type, nfields, components):
        super(ScorerWindow, self).__init__()
        self.setupUi(self)

        self.outdir = outdir

        self.scorer_container = {}

        self.nozzle_type = nozzle_type
        self.nfields = nfields
        self.component_names = components # only names

        self.instance = None
        self.templates = {}
        self.components = {}
        self.field_checklist = {}
        self.scorer_container = {}
        self.filter_container = {}
        self.set_action()
        #self.show()

    def set_action(self):
        #self.pushLoad.clicked.connect(lambda: self.load_cfg(push=True))

        self.pushMake.clicked.connect(self.write_output)
        self.pushClear.clicked.connect(self.clear_all)
        self.pushCancel.clicked.connect(self.click_cancel)
        self.pushAddNewPara.clicked.connect(self.add_element)
        self.pushAppendComp.clicked.connect(self.add_template)
        
        self.comboMacro.addItem('Select')
        self.comboMacro.addItem('New')
        self.comboMacro.addItem('Open')
        self.comboMacro.addItem('Save')
        self.comboMacro.currentTextChanged.connect(self.open_macro)

        self.tabAddBtn = QToolButton()
        self.tabAddBtn.setAutoRaise(True)
        self.tabAddBtn.setIcon(QIcon(os.path.join(var.BASE_PATH,"icons/new.png")))
        self.tabAddBtn.clicked.connect(lambda: self.add_run())

        self.tabAddBtn2 = QToolButton()
        self.tabAddBtn2.setAutoRaise(True)
        self.tabAddBtn2.setIcon(QIcon(os.path.join(var.BASE_PATH,"icons/new.png")))
        self.tabAddBtn2.clicked.connect(lambda: self.add_run())

        self.tabRun.setCornerWidget(self.tabAddBtn, Qt.TopRightCorner)
        self.tabRequirement.setCornerWidget(self.tabAddBtn2, Qt.TopRightCorner)

        if self.tabRun.count() == 0: self.add_run()

        self.comboComp.addItem('Select')
        self.comboComp.addItem('New')
        self.comboComp.insertSeparator(3)
        temp = Component(self.nozzle_type)
        for name in temp.component_list(True).keys():
            self.comboComp.addItem(name)
        del temp
        self.comboComp.currentTextChanged.connect(lambda: self.new_template(self.comboComp.currentText()))

        self.listTemplates.setContextMenuPolicy(Qt.ActionsContextMenu)
        actionShow = QAction("Show", self.listTemplates)
        actionShow.triggered.connect(self.show_component)
        actionAdd = QAction("Add", self.listTemplates)
        actionAdd.triggered.connect(self.add_component)        
        self.listTemplates.addAction(actionAdd)
        self.listTemplates.addAction(actionShow)
        self.listTemplates.itemDoubleClicked.connect(self.add_component)

    def clear_all(self):
        self.instance = None
        self.templates = {}
        self.components = {}
        self.scorer_container = {}
        self.tabRequirement.clear()
        self.tabRun.clear()
        self.listTemplates.clear()
        self.tabScorer.clear()

    def open_macro(self):
        if self.comboMacro.currentText() == 'Select': return

        if self.comboMacro.currentText() == 'Save':
            self.save_cfg()
            return

        if self.comboMacro.currentText() == 'Open':
            fname = QFileDialog.getOpenFileName(self, 'Open', os.path.join(var.BASE_PATH,'plugin'), filter = "Python files (*.py)")[0]
            if fname == "": return
        elif self.comboMacro.currentText() == 'New':
            fname = 'simulation.py'
        else:
            fname = f'{self.comboMacro.currentText().lower()}.py'

        self.clear_all()

        proton = Proton()
        proton.load(fname)
        cls_name = proton.name(fname)
        self.instance = proton.process(proton.name(fname))(outdir=var.G_OUTDIR, nozzle=var.G_NOZZLE_TYPE, patient=var.G_PATIENT, parameters=var.G_PARAMETER)
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

        for key in self.instance.keys:
            if self.comboComp.findText(key) < 0:
                self.comboComp.addItem(key)
            self.add_run(key)

        for key in self.instance.keys:
            listComponent = QListWidget()
            listComponent.setContextMenuPolicy(Qt.ActionsContextMenu)
            actionDel = QAction("Delete", listComponent)
            actionDel.triggered.connect(self.delete_component)
            listComponent.addAction(actionDel)
            listComponent.itemDoubleClicked.connect(self.delete_component)
            self.tabScorer.addTab(listComponent, key)

        self.load_cfg(fname)

    def save_cfg(self):
        if self.comboMacro.currentText() == 'Select': return

        fname = QFileDialog.getSaveFileName(self, 'Save', os.path.join(var.BASE_PATH, 'plugin'), filter="Nozzle files (*.nzl)")[0]
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
        for idx in range(self.tabScorer.count()):
            name = self.tabScorer.tabText(idx)
            widget = self.tabScorer.widget(idx)
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
            if fname == '': return

        with open(os.path.join(var.BASE_PATH, 'plugin', fname.replace('.py', '.nzl')), 'r') as f:
            cfg = yaml.load(f, Loader=yaml.FullLoader)
        for name, comp_info in cfg['Template'].items():
            template = Component(nozzle_type=self.nozzle_type, phase=True)
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

        for idx in range(self.tabScorer.count()):
            tabname = self.tabScorer.tabText(idx)
            widget = self.tabScorer.widget(idx)
            if not tabname in cfg: continue
            for text in cfg[tabname]:
                witem = QListWidgetItem(widget)
                item = Item()
                item.add_label(text)
                widget.setItemWidget(witem, item)
                widget.addItem(witem)
                witem.setSizeHint(item.sizeHint())

    def set_requirement(self):
        for idx in range(self.listRequirement.count()):
            item = self.listRequirement.itemWidget(self.listRequirement.item(idx))
            vtype = item.label.text()
            vari = None
            if vtype.lower() == "patient":
                var.G_PATIENT.patient_setup(item.lineValue.text())
                vname = var.G_PATIENT.directory
                vari = var.G_PATIENT
            else:
                vname = item.lineValue.text()
                vari = item.lineValue.text()
            self.instance.set_requirement(vtype=vtype, vname=vname, vari=vari)

    def set_field(self, field_name):
        idx = self.tabRequirement.currentIndex()
        run_name = self.tabRun.tabText(idx)
        self.field_checklist[run_name] = field_name
        print(self.field_checklist)

    def add_run(self, run_name=''):
        if run_name == '':
            self.scorer_container[f"Run{len(self.scorer_container)}"] = self.component_names
        else:
            self.scorer_container[run_name] = self.component_names

        widgetRequirement = QWidget()
        gridRequirement = QGridLayout(widgetRequirement)
        labelField = QLabel("Field:")
        comboField = QComboBox()
        comboField.addItem(f"")
        for idx in range(self.nfields):
            comboField.addItem(f"Field{idx+1}")
        comboField.currentTextChanged.connect(lambda: self.set_field(comboField.currentText()))

        gridRequirement.addWidget(labelField, 0, 0, 1, 1)
        gridRequirement.addWidget(comboField, 0, 1, 1, 2)
        gridRequirement.setAlignment(Qt.AlignLeft)

        widgetRun = QWidget()
        gridlayout = QGridLayout(widgetRun)
        for idx, component in enumerate(self.component_names):
            item = Item()
            item.add_checkbox(component)
            gridlayout.addWidget(item, idx, 0, 1, 1)
        gridlayout.setAlignment(Qt.AlignLeft)

        empty_widget = QWidget()
        empty_list_widget = QListWidget()
        empty_list_widget.itemDoubleClicked.connect(self.delete_component)
        vboxlayout = QVBoxLayout(empty_widget)
        vboxlayout.addWidget(empty_list_widget)

        if run_name == '':
            self.tabRequirement.addTab(widgetRequirement, f"Run{len(self.scorer_container)}")
            self.tabRun.addTab(widgetRun, f"Run{len(self.scorer_container)}")
            self.tabScorer.addTab(empty_widget, f"Run{len(self.scorer_container)}")
        else:
            self.tabRequirement.addTab(widgetRequirement, f"{run_name}")
            self.tabRun.addTab(widgetRun, f"{run_name}")
            self.tabScorer.addTab(empty_widget, f"{run_name}")

        self.tabRequirement.setCurrentIndex(self.tabRequirement.count()-1)
        self.tabRun.setCurrentIndex(self.tabRun.count()-1)
        self.tabScorer.setCurrentIndex(self.tabScorer.count()-1)

    def new_template(self, cname):
        if cname == '' or cname == 'Select': return
        self.tabComp.clear()

        if cname == "New":
            self.tabComp.clear()
            template = Component(nozzle_type=self.nozzle_type)
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
            listPara.itemDoubleClicked.connect(self.modify_element)
        elif self.instance is not None and any(cname == i for i in self.instance.keys):
            self.tabComp.clear()
            template = Component(nozzle_type=self.nozzle_type)
            template.name = cname
            template.ctype = cname
            listPara = QListWidget()
            listPara.setContextMenuPolicy(Qt.ActionsContextMenu)
        
            actions = {"Modify":self.modify_element, "Delete":self.delete_element}
            for key, value in actions.items():
                action = QAction(key, listPara)
                action.triggered.connect(value)
                listPara.addAction(action)
            listPara.itemDoubleClicked.connect(self.modify_element)
            self.tabComp.addTab(listPara, template.name)
            self.templates[template.name] = template
        else:
            dirname = os.path.join(var.BASE_PATH, 'data/components', self.comboComp.currentText())
            for f in os.listdir(dirname):
                template = Component(nozzle_type=self.nozzle_type, phase=True)
                template.load(fname=os.path.join(dirname, f))
                template.ctype = cname
                listPara = QListWidget()
                listPara.setContextMenuPolicy(Qt.ActionsContextMenu)
        
                actions = {"Modify":self.modify_element, "Delete":self.delete_element}

                for key, value in actions.items():
                    action = QAction(key, listPara)
                    action.triggered.connect(value)
                    listPara.addAction(action)
                listPara.itemDoubleClicked.connect(self.modify_element)

                paras = [i for i in template.subcomponent['Basis'].parameters]
                for para in paras:
                    name = f'{para.vtype}:{para.category}/{para.directory}/{para.name}'
                    witem = QListWidgetItem(listPara)
                    item = Item()
                    item.add_lineedit(name, para.value)
                    item.lineValue.textChanged.connect(self.modify_element)
                    item.lineValue.returnPressed.connect(self.modify_element)
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

    def show_component(self):
        pass

    def add_component(self):
        list_widget = self.tabScorer.currentWidget().findChildren(QListWidget)[0]
        witem = QListWidgetItem(list_widget)
        item = Item()
        i = self.listTemplates.itemWidget(self.listTemplates.currentItem())
        item.add_label(i.label.text())
        list_widget.setItemWidget(witem, item)
        list_widget.addItem(witem)
        witem.setSizeHint(item.sizeHint())
    
    def delete_component(self):
        widget = self.tabScorer.currentWidget().findChildren(QListWidget)[0]
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
        
    def modify_element(self):
        # FIXME
        widget = self.tabComp.currentWidget()
        idx = widget.currentRow()
        item = widget.itemWidget(widget.item(idx))
        if item is None: return
        subcomp = self.tabComp.tabText(self.tabComp.currentIndex())
        name = self.templates[subcomp].subcomponent['Basis'].parameters[idx].fullname()
        print(self.templates[subcomp])
        value = item.lineValue.text()
        self.templates[subcomp].modify_parameter('Basis', {name:value})
        item.lineValue.setText(value)
        print(self.templates[subcomp])
        
    def write_output(self):
        if self.instance is not None:
            if not self.instance.is_workable():
                QMessageBox.warning(self, "Message", "Please, Fill requirements", QMessageBox.Ok)
                return
            tmp_dict = {i:[] for i in self.instance.keys}
            for idx in range(self.tabRun.count()):
                name = self.tabRun.tabText(idx)
                widget = self.tabRun.widget(idx)
                tmp = []
                for idx2 in range(widget.count()):
                    item = widget.itemWidget(widget.item(idx2))
                    if item.checkbox.isChecked():
                        text = item.label.text()[1:-1]
                        tmp.append(text)
                self.instance.set_import_files(name, tmp)
            
                widget = self.tabScorer.widget(idx)
                for idx2 in range(widget.count()):
                    item = widget.itemWidget(widget.item(idx2))
                    text = item.label.text()
                    tmp = text.replace(' - ','-').split('-')
                    tmp = (tmp[0], tmp[1])
                    tmp_dict[name].append(tmp)

            self.instance.set_templates(tmp_dict, self.components)
            self.scorer_container, self.filter_container = self.instance.run()
        else:
            from plugin.simulation import Simulation
            self.instance = Simulation(outdir=self.outdir, nozzle_type=self.nozzle_type)
            self.instance.nbeams = self.tabRun.count()
            tmp_dict = {}
            for idx in range(self.tabRun.count()):
                run_name = self.tabRun.tabText(idx)
                self.instance.update_keys(run_name)
                tmp_dict[run_name] = []

                runWidget = self.tabRun.widget(idx)
                tmp = []
                widgets = runWidget.findChildren(Item)
                for item in widgets:
                    checkbox = item.get_checkbox()
                    if checkbox.isChecked():
                        text = checkbox.text()#[1:-1]
                        tmp.append(text)
                self.instance.set_import_files(run_name, tmp)

                scrWidget = self.tabScorer.widget(idx)
                lstWidget = scrWidget.findChild(QListWidget)
                for idx2 in range(lstWidget.count()):
                    item = lstWidget.itemWidget(lstWidget.item(idx2))
                    text = item.label.text()
                    tmp = text.replace(' - ','-').split('-')
                    tmp = (tmp[0], tmp[1])
                    tmp_dict[run_name].append(tmp)
            self.instance.set_templates(tmp_dict, self.components)

            self.scorer_container, self.filter_container = self.instance.run()

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
