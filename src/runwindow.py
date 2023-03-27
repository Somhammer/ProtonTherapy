import subprocess
import logging

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

from src.classreader import *
import src.variables as var
from src.ui_runwindow import Ui_RunWindow

class LogStringHandler(logging.Handler):
    def __init__(self, target_widget):
        super().__init__()
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt="%H:%M:%S")
        self.setFormatter(formatter)
        self.target_widget = target_widget

    def emit(self, record):
        self.format(record)
        self.target_widget.append(f'[{record.asctime}][{record.levelname}]: {record.getMessage()}')

class RunWindow(QDialog, Ui_RunWindow):
    def __init__(self, outdir, nozzle_type, field_list, fields, nozzles, scorers, filters):
        super(RunWindow, self).__init__()
        self.setupUi(self)

        self.outdir = outdir
        self.topas = Topas()

        self.nozzle_type = nozzle_type
        self.field_checklist = field_list
        self.fields = fields
        self.nozzles = nozzles
        self.scorers = scorers
        self.filters = filters

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        handler = LogStringHandler(self.textLog)
        self.logger.addHandler(handler)

        self.set_action()
    
    def set_action(self):
        self.pushOk.clicked.connect(self.click_ok)

    def show(self):
        super().show()
        self.run()
 
    def run(self):
        self.logger.info("Generate topas input files")
        try:
            dirs = ['nozzle', 'aperture', 'compensator', 'parallels']
            for i in dirs:
                if not os.path.exists(os.path.join(self.outdir,i)):
                    os.makedirs(os.path.join(self.outdir,i))
            for name, component in self.nozzles.items():
                self.logger.info(f"Generate Nozzle Component: {name}")
                outname = os.path.join(self.outdir, dirs[0], name)
                if not '.tps' in outname:
                    outname = outname + '.tps'
                f = open(outname,'w')
                f.write(component.fulltext())
            
            for run, scorers in self.scorers.items():
                field = self.fields[self.field_checklist[run]]
                for scorer in scorers:
                    self.logger.info(f"Generate Scorer: {run} ")
                    for subname, comp in scorer.subcomponent.items():
                        for para in comp.parameters:
                            for key in field.keys():
                                if key in para.value:
                                    field_value = field[key]
                                    str_fvalue = ' '.join(i for i in field_value)
                                    vtype = para.vtype
                                    name = para.fullname()
                                    value = para.value
                                    value = value.replace(key,"")
                                    value = value.format(str_fvalue)
                                    newpara = {name:value}
                                    scorer.modify_parameter(subname, newpara, delete=False)
                    outname = os.path.join(self.outdir, run)
                    if not '.tps' in outname:
                        outname = outname + '.tps'
                    f = open(outname,'w')
                    nozzle_path = os.path.join(self.outdir, dirs[0]).replace("\\","/")
                    f.write(scorer.fulltext().replace("includeFile = ", f"includeFile = {nozzle_path}/"))        
        except BaseException as err:
            self.textLog.append(str(err))
            self.textLog.append("Generation is failed.")                            
        return
            
    """
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
    """ 
    
    def click_ok(self):
        self.accept()

    def return_para(self):
        logging.shutdown()
        self.logger.disabled = True
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
            handler.close()
        return super().exec_()
