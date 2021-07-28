import subprocess

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

from src.classreader import *
import src.variables as var
from src.ui_runwindow import Ui_RunWindow

class RunWindow(QDialog, Ui_RunWindow):
    def __init__(self, parent):
        super(RunWindow, self).__init__(parent)
        self.setupUi(self)

        self.topas = Topas()

        self.set_action()
        self.show()
        self.run()

    def set_action(self):
        self.pushOk.clicked.connect(self.click_ok)
    
    def run(self):
        self.textLog.append("...Generate topas input files")
        try:
            lst = []
            if var.G_NOZZLE_TYPE == 'scanning': lst = ['nozzle', 'parallels']
            else: lst = ['nozzle', 'aperture', 'compensator', 'parallels']
            for i in lst:
                if not os.path.exists(os.path.join(var.G_OUTDIR,i)):
                    os.makedirs(os.path.join(var.G_OUTDIR,i))

            self.textLog.append("......Generate topas files")
            for component in var.G_COMPONENT:
                f = open(os.path.join(component.outname),'w')
                f.write(component.fulltext())

            self.textLog.append("......Generate filter files")
            for fil in var.G_FILTER:
                f = open(os.path.join(var.G_OUTDIR, fil['OutName']), 'w')
                f.write(fil['RawText'])

            self.textLog.append("......Generate phase files")
            for key, values in list(var.G_PHASE.items()):
                if key.lower() != 'patient': continue
                for value in values:
                    f = open(os.path.join(value.outname), 'w')
                    f.write(value.fulltext())
                del var.G_PHASE[key]
                 
            for key, phases in var.G_PHASE.items():
                for ibeam, phase in enumerate(phases):
                    f = open(os.path.join(phase.outname), 'w')
                    f.write(phase.fulltext())
                    for i in phase.imported:
                        name = i.split('/')[-1]
                        if any(name in j for j in os.listdir(os.path.join(var.G_OUTDIR,'nozzle'))): continue
                        if any(name in j for j in os.listdir(os.path.join(var.G_OUTDIR,'parallels'))): continue
                        for (path, directories, files) in os.walk(var.BASE_PATH, 'data/components'):
                            for f in files:
                                if f == name:
                                    cmd = ['cp', os.path.join(path, f), os.path.join(var.G_OUTDIR, 'nozzle', f)]
                                    subprocess.call(cmd)

            self.textLog.append("Topas input files are generated.")
        except BaseException as err:
            self.textLog.append(str(err))
            self.textLog.append("Generation is failed.")
            
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
        return super().exec_()
