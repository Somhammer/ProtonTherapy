import yaml

from PySide6.QtWidgets import *
from PySide6.QtCore import *

from src.variables import *
from src.data import *

from src.ui_simulationwindow import Ui_SimulationWindow
from src.data import *
from src.painter import *
from src.item import *
from src.classreader import Proton
from src.modifyparameter import ModifyParameter

class SimulationWindow(QDialog, Ui_SimulationWindow):
    def __init__(self, parent):
        super(SimulationWindow, self).__init__(parent)
        self.setupUi(self)

        self.instance = None
        self.templates = {}
        self.components = {}
        self.set_action()
        self.show()

    def set_action(self):
        #self.pushLoad.clicked.connect(lambda: self.load_cfg(push=True))

        self.pushMake.clicked.connect(self.write_output)
        self.pushClear.clicked.connect(self.clear_all)
        self.pushCancel.clicked.connect(self.click_cancel)
        self.pushOpenFile.clicked.connect(self.add_import)
        self.pushAddNewPara.clicked.connect(self.add_element)
        self.pushAppendComp.clicked.connect(self.add_template)
        
        self.comboMacro.addItem('Select')
        self.comboMacro.addItem('New')
        self.comboMacro.addItem('Open')
        self.comboMacro.addItem('Save')
        self.comboMacro.currentTextChanged.connect(self.open_macro)

        self.comboComp.addItem('Select')
        self.comboComp.addItem('New')
        self.comboComp.insertSeparator(3)
        temp = Component(btype=var.G_NOZZLE_TYPE, phase=True)
        for key in temp.component_list().keys():
            self.comboComp.addItem(key)
        del temp
        self.comboComp.currentTextChanged.connect(lambda: self.new_template(self.comboComp.currentText()))

        self.listTemplates.setContextMenuPolicy(Qt.ActionsContextMenu)
        actionAdd = QAction("Add", self.listTemplates)
        actionAdd.triggered.connect(self.add_component)        
        self.listTemplates.addAction(actionAdd)
        self.listTemplates.itemDoubleClicked.connect(self.add_component)

    def clear_all(self):
        self.instance = None
        self.templates = {}
        self.components = {}
        self.listRequirement.clear()
        self.tabImport.clear()
        self.listTemplates.clear()
        self.tabComponents.clear()

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

        for key in self.instance.keys:
            listImport = QListWidget()
            listImport.setContextMenuPolicy(Qt.ActionsContextMenu)
            for component in var.G_COMPONENT:
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
            if fname == '': return

        with open(os.path.join(var.BASE_PATH, 'plugin', fname.replace('.py', '.nzl')), 'r') as f:
            cfg = yaml.load(f, Loader=yaml.FullLoader)
        for name, comp_info in cfg['Template'].items():
            template = Component(btype=var.G_NOZZLE_TYPE, phase=True)
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
        
    def add_import(self):
        if self.comboMacro.currentText() == 'Select': return

        fname = QFileDialog.getOpenFileName(self, "Import",  os.path.join(var.BASE_PATH,'data/components'), selectedFilter = var.G_TEXT_EXTENSION[0], filter='\n'.join(i for i in var.G_TEXT_EXTENSION))[0]
        if fname == '': return
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
            template = Component(btype=var.G_NOZZLE_TYPE)
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
            template = Component(btype=var.G_NOZZLE_TYPE)
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
            dirname = os.path.join(var.BASE_PATH, 'data/components', self.comboComp.currentText())
            for f in os.listdir(dirname):
                template = Component(btype=var.G_NOZZLE_TYPE, phase=True)
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
        var.G_PHASE, var.G_FILTER = self.instance.run()
        #g_order = self.instance.order
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
