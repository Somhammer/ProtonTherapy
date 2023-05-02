from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

import src.variables as var
from src.data import *

from src.ui_newtabwindow import Ui_NewtabWindow
from src.ui_componentwindow import Ui_ComponentWindow

from src.item import *

class NewtabWindow(QDialog, Ui_NewtabWindow):
    def __init__(self, parents, components):
        super(NewtabWindow, self).__init__()
        self.setupUi(self)

        self.setWindowTitle("New tab")
        
        self.parent_name = None
        self.preset = None
        self.tab_name = None

        for item in parents:
            self.comboParent.addItem(item)

        for item in components:
            self.comboPreset.addItem(item)

        self.lineTabName.returnPressed.connect(self.click_ok)
        self.pushOk.clicked.connect(self.click_ok)
        self.pushCancel.clicked.connect(self.click_cancel)
        self.show()
        
    def click_ok(self):
        self.preset = self.comboPreset.currentText()
        self.parent_name = self.comboParent.currentText()
        self.tab_name = self.lineTabName.text()
        self.accept()
        
    def click_cancel(self):
        self.reject()
        
    def return_para(self):
        return super().exec_()

class ComponentWindow(QDialog, Ui_ComponentWindow):
    def __init__(self, nozzle_type):
        super(ComponentWindow, self).__init__()
        self.setupUi(self)

        self.newtab_count = 1
        self.nozzle_type = nozzle_type
        self.component = Component(component_name='Basic')

        self.set_action()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.click_cancel(event)

    def closeEvent(self, event):
        self.click_cancel(event)
        
    def set_action(self):
        # Preset
        self.comboPreset.addItem('Select')
        self.comboPreset.addItem("Load")
        self.comboPreset.insertSeparator(3)
        self.comboPreset.addItem('Dipole')
        self.comboPreset.addItem('Quadrupole')
        self.comboPreset.currentTextChanged.connect(lambda: self.load(component=self.comboPreset.currentText()))

        # Import
        self.pushImport.clicked.connect(self.import_component)
        self.pushImportClear.clicked.connect(self.import_clear)
        # Component Tab
        self.tabAddBtn = QToolButton()
        self.tabComp.setCornerWidget(self.tabAddBtn, Qt.TopRightCorner)
        self.tabAddBtn.setAutoRaise(True)
        self.tabAddBtn.setIcon(QIcon(os.path.join(var.BASE_PATH,"icons/new.png")))
        self.tabAddBtn.clicked.connect(lambda: self.add_tab(open_tabwindow=True))

        # Element
        ### LineEdit
        self.lineTabName.returnPressed.connect(self.change_tabname)
        ### Buttonadd_tab
        self.pushChangeTabName.clicked.connect(self.change_tabname)
        self.pushAddTab.clicked.connect(lambda: self.add_tab(open_tabwindow=True))
        self.pushDeleteTab.clicked.connect(self.delete_tab)
        self.pushDeleteAllTabs.clicked.connect(self.delete_all_tabs)

        self.pushAddVari.clicked.connect(self.add_variable_from_text)
        self.pushClearVari.clicked.connect(self.clear_line_edits)
        self.pushOk.clicked.connect(self.click_ok)
        self.pushCancel.clicked.connect(self.click_cancel)

        self.comboNewVariType.addItem("")
        for item in type_dict.keys():
            self.comboNewVariType.addItem(item)

        self.comboNewVariPrefix.addItem("")
        for item in directory_dict.keys():
            self.comboNewVariPrefix.addItem(item)

    def clear_widgets(self):
        self.comboPreset.setCurrentIndex(0)
        self.comboNewVariType.setCurrentIndex(0)
        self.comboNewVariPrefix.setCurrentIndex(0)
        self.listImport.clear()
        self.tabComp.clear()
        self.lineTabName.clear()
        self.lineNewVariName.clear()
        self.lineNewVariValue.clear()
        self.lineNewVariUnit.clear()

    def update_widgets_from_data(self):
        self.clear_widgets()
        self.lineFileName.setText(self.component.file_name)
        for imported_file in self.component.imported:
            self.import_file(path=imported_file)
        
        for name, variables in self.component.variables.items():
            self.add_tab(tab_name=name)
            for variable in variables:
                self.add_variable_from_data(name, variable)

    def update_data_from_widgets(self):
        self.component.file_name = self.lineFileName.text()
        for idx in range(self.listImport.count()):
            item = self.listImport.itemWidget(self.listImport.item(idx))
            imported = item.checkbox.text()
            if item.checkbox.isChecked():
                self.component.add_import_file(imported)
        
        for idx in range(self.tabComp.count()):
            widget = self.tabComp.widget(idx)
            for idx2 in range(widget.count()):
                item = widget.itemWidget(widget.item(idx2))
                name = item.label.text()
                value = item.lineValue.text()
                text = f"{name} {value}"
                self.component.add_variable_from_str(text)

    def show(self):
        self.update_widgets_from_data()
        super().show()

    def load(self, component=None):
        if component is None or component == "Select": return
    
        if component == "Load":
            filename = QFileDialog.getOpenFileName(self, 'Load', os.path.join(var.BASE_PATH, 'data/components'),
            selectedFilter = var.G_TEXT_EXTENSION[0], filter='\n'.join(i for i in var.G_TEXT_EXTENSION))[0]
            component = Component()
            component.file_name = os.path.basename(filename)
            component.get_variables_from_textfile(filename=filename, initialize=True)
        self.comboPreset.setCurrentIndex(0)

        if not "component" in str(type(component)).lower(): return
        self.component = component
        self.update_widgets_from_data()

    # Import
    def import_file(self, path):
        fname = os.path.basename(path)

        for idx in range(self.listImport.count()):
            item = self.listImport.itemWidget(self.listImport.item(idx))
            if fname in item.label.text(): return

        witem = QListWidgetItem(self.listImport)
        item = Item()
        item.add_checkbox(fname, path=path, layout_direction=QBoxLayout.TopToBottom)

        def modify(component, path, checkbox):
            if checkbox.isChecked():
                component.add_import_file(path)
            else:
                component.delete_import_file(path)
            print(component.imported)
        modify(self.component, path, item.checkbox)

        item.checkbox.stateChanged.connect(lambda: modify(self.component, path, item.checkbox))
        self.listImport.setItemWidget(witem, item)
        self.listImport.addItem(witem)
        witem.setSizeHint(item.sizeHint())

    def import_component(self):
        filename = QFileDialog.getOpenFileName(self, 'Import file', os.path.join(var.BASE_PATH, 'data/components'), 
            selectedFilter = var.G_TEXT_EXTENSION[0], filter='\n'.join(i for i in var.G_TEXT_EXTENSION))[0]
        if filename == "": return
        self.import_file(filename)

    def import_clear(self):
        for idx in range(self.listImport.count()):
            item = self.listImport.itemWidget(self.listImport.item(idx))
            item.checkbox.setChecked(False)
        self.listImport.clear()

    def add_tab(self, tab_name="NewTab", parent_name=None, preset=None, open_tabwindow=False):
        if open_tabwindow:
            tabwindow = NewtabWindow(list(self.component.family_relations.keys()), [])
            r = tabwindow.return_para()
            if r:
                preset = tabwindow.preset
                if tabwindow.tab_name != "" and tabwindow.tab_name is not None:
                    tab_name = tabwindow.tab_name
                if tabwindow.parent_name != "" and tabwindow.parent_name is not None:
                    parent_name = tabwindow.parent_name
            else:
                return
            
        self.component.get_variables_from_textfile(preset)

        isDuplicated = False
        for idx in range(self.tabComp.count()):
            tab = self.tabComp.tabText(idx)
            if tab_name in tab:
                isDuplicated = True
                break
        if isDuplicated and not "NewTab" in tab_name: return
        elif isDuplicated and "NewTab" in tab_name:
            tab_name = f"NewTab_{self.newtab_count+1}"
            self.newtab_count += 1

        listWidget = QListWidget()
        listWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
        actions = {"Delete":self.delete_variable}
        for key, value in actions.items():
            action = QAction(key, listWidget)
            action.triggered.connect(value)
            listWidget.addAction(action)
        #listWidget.itemDoubleClicked.connect(self.modify_variable)

        self.tabComp.addTab(listWidget, f"{tab_name}")
        self.component.add_family(parent_name=parent_name, child_name=tab_name)

    def change_tabname(self):
        if self.lineTabName.text() == "": return
        new_tabname = self.lineTabName.text()
        current_index = self.tabComp.currentIndex()
        current_name = self.tabComp.tabText(current_index)

        self.component.change_myname(current_name, new_tabname)
        self.update_data_from_widgets()
        self.update_widgets_from_data()

    def delete_tab(self):
        current_index = self.tabComp.currentIndex()
        current_name = self.tabComp.tabText(current_index)
        self.component.delete_family(current_name)
        self.update_data_from_widgets()
        self.update_widgets_from_data()

    def delete_all_tabs(self):
        for idx in range(self.tabComp.count()):
            self.component.delete_family(self.tabComp.tabText(idx))

        self.update_data_from_widgets()
        self.update_widgets_from_data()

    def add_variable_from_data(self, tabname, variable):
        text = self.component.convert_variable_to_str(tabname, variable)
        text = text.split(" = ")
        for idx in range(self.tabComp.count()):
            if tabname == self.tabComp.tabText(idx):
                listWidget = self.tabComp.widget(idx)
        witem = QListWidgetItem(listWidget)
        item = Item()
        item.add_lineedit(text[0], text[1])

        def modify(component, name, value):
            string = f"{name} = {value}"
            component.modify_variable_from_str(string)

        item.lineValue.textChanged.connect(lambda: modify(self.component, item.label.text(), item.lineValue.text()))
        item.lineValue.returnPressed.connect(lambda: modify(self.component, item.label.text(), item.lineValue.text()))
        listWidget.setItemWidget(witem, item)
        listWidget.addItem(witem)
        witem.setSizeHint(item.sizeHint())

    def add_variable_from_text(self):
        directory = self.comboNewVariPrefix.currentText()

        if directory is "": return
        tabname = self.tabComp.tabText(self.tabComp.currentIndex())
        listWidget = self.tabComp.widget(self.tabComp.currentIndex())
        vtype = self.comboNewVariType.currentText()
        family_tree = self.component.get_family_tree(tabname)
        myname = self.lineNewVariName.text()
        if family_tree in myname:
            myname = myname.replace(family_tree, "")
        value = self.lineNewVariValue.text()
        unit = self.lineNewVariUnit.text()

        if directory in family_tree:
            fullname = f"{family_tree}/{myname}"
        else:
            fullname = f"{directory}/{family_tree}/{myname}"

        if vtype != "":
            fullname = f"{vtype}:{fullname}"

        if unit != "":
            value = f"{value} {unit}"

        witem = QListWidgetItem(listWidget)
        item = Item()
        item.add_lineedit(fullname, value)

        def modify(component, name, value):
            string = f"{name} = {value}"
            component.modify_variable_from_str(string)

        item.lineValue.textChanged.connect(lambda: modify(self.component, item.label.text(), item.lineValue.text()))
        item.lineValue.returnPressed.connect(lambda: modify(self.component, item.label.text(), item.lineValue.text()))
        listWidget.setItemWidget(witem, item)
        listWidget.addItem(witem)
        witem.setSizeHint(item.sizeHint())
        self.comboNewVariType.setCurrentIndex(0)
        self.comboNewVariPrefix.setCurrentIndex(0)
        self.component.add_variable_from_str(f"{fullname} = {value}")

    def delete_variable(self):
        widget = self.tabComp.widget(self.tabComp.currentIndex())
        item = widget.itemWidget(widget.item(widget.currentRow()))
        if item is not None:
            name = item.label.text()
            value = item.lineValue.text()
            string = f"{name} = {value}"
            print(string)
            self.component.delete_variable_from_str(string)
        self.update_widgets_from_data()

    def clear_line_edits(self):
        self.lineNewVariType.clear()
        self.lineNewVariName.clear()
        self.lineNewVariValue.clear()
        self.lineNewVariUnit.clear()

    def click_ok(self):
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