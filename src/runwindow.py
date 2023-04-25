import subprocess
import logging
import shutil

import paramiko
from scp import SCPClient
from datetime import datetime
import yaml


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
        self.target_widget.append(f'[{record.asctime}][{record.levelname}]:{record.getMessage()}')

class RunThread(QThread):
    logger_signal = Signal(str, str)
    progressbar_signal = Signal(float)

    def __init__(self, outdir, nozzle_type, field_list, fields, nozzles, scorers, filters):
        super().__init__()
        self.outdir = outdir

        self.nozzle_type = nozzle_type
        self.field_checklist = field_list
        self.fields = fields
        self.nozzles = nozzles
        self.scorers = scorers
        self.filters = filters

    def run(self):
        self.progressbar_signal.emit(0)
        ### Generate TOPAS input text files
        self.logger_signal.emit("INFO", "Generate topas input files")
        if os.path.exists(self.outdir):
            shutil.rmtree(self.outdir)
        try:
            dirs = ['nozzle', 'aperture', 'compensator', 'parallels']
            for i in dirs:
                if not os.path.exists(os.path.join(self.outdir,i)):
                    os.makedirs(os.path.join(self.outdir,i))
            for name, component in self.nozzles.items():
                self.logger_signal.emit("INFO", f"Generate Nozzle Component: {name}")
                outname = os.path.join(self.outdir, dirs[0], name)
                if not '.tps' in outname:
                    outname = outname + '.tps'
                f = open(outname,'w')
                f.write(component.fulltext())
            self.progressbar_signal.emit(10)
            total_run = len(self.scorers)
            i = 1
            for run, scorers in self.scorers.items():
                field = self.fields[self.field_checklist[run]]
                for scorer in scorers:
                    self.logger_signal.emit("INFO", f"Generate Scorer: {run}")
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
                    if i < total_run: i += 1
                    self.progressbar_signal.emit(50*(i/total_run))
        except BaseException as err:
            self.logger_signal.emit("ERROR", f"{str(err)}: Generation is failed.")
            return
        
        ### Send generated files to NCC Server
        self.logger_signal.emit("INFO", "Connect to server and transfer files")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        from ProtonTherapy import BASE_PATH
        with open(os.path.join(BASE_PATH, 'server_info.yaml'), 'r') as f:
            info = yaml.safe_load(f)

        if info['key'].startswith("./"):
            key_path = os.path.join(BASE_PATH, info['key'].replace('./', ''))
        else:
            key_path = info['key']

        key = paramiko.RSAKey.from_private_key_file(key_path)
        try:
            ssh.connect(info['IP'], port=info['port'], username=info['username'], pkey=key)
            self.ssh = ssh
        except paramiko.AuthenticationException:
            self.logger_signal.emit("ERROR", 'Authorification Failed.')
            return
        except paramiko.SSHException:
            self.logger_signal.emit("ERROR", f'Cannot connect to {info["IP"]}:{info["port"]}.')
            return

        self.progressbar_signal.emit(60)

        ### check TOPAS installation
        topas_cmd = info['topas']
        stdin, stdout, stderr = ssh.exec_command(topas_cmd)
        error = stderr.read().decode('utf-8')
        if 'command not found' in error:
            self.logger_signal.emit("WARNING", f'TOPAS is not installed.')
        self.progressbar_signal.emit(65)
        # TODO
        ## Modify this job submit process. Slurm must run TOPAS using singularity.
        ### Generate Slurm shell script file and transfer
        #for run, scorers in self.scorers.items():
        with SCPClient(self.ssh.get_transport()) as scp:
            scp.get("/data/ProtonTherapy_data/submit.sh", self.outdir)
        today = datetime.now().strftime("%y%m%d")
        for run in self.scorers.keys():
            with open(os.path.join(self.outdir, 'submit.sh'), 'r', newline='') as f:
                script = f.read()
                script = script.format(username=info['username'], date=today)
            script = script.replace("\r\n", "\n")
            with open(os.path.join(self.outdir, 'submit.sh'), 'w', newline='\n') as f:
                f.write(script)
        
        self.progressbar_signal.emit(75)

        try:
            with SCPClient(self.ssh.get_transport()) as scp:
                scp.put(self.outdir, info['dest'], recursive=True)
        except:
            self.logger_signal.emit("ERROR", f'Transfer is failed.')
            return

        ### Slurm Job Submit
        command_list = []
        for run in self.scorers.keys():
            # TODO
            #if run has dependency:
            # command = f"sbatch submit.sh --dependency=afterok:{previous_run} {topas_cmd} {run}"
            command_list.append(f"sbatch submit.sh {topas_cmd} {run}.tps")

        for command in command_list:
            self.logger_signal.emit("INFO", command)
            stdin, stdout, stderr = ssh.exec_command(f'cd {info["dest"]}/{today} && {command}')
            #stdin, stdout, stderr = ssh.exec_command(f'cd {info["dest"]} && ls')

            print(f'cd {info["dest"]} && {command}')
            out = stdout.read().decode('utf-8')
            error = stderr.read().decode("utf-8")
            print("ERROR: ", error, len(error))
            if error is not None and len(error) > 0:
                self.logger_signal.emit("ERROR", error)
            else:
                self.logger_signal.emit("INFO", out)

        self.progressbar_signal.emit(100)

class RunWindow(QDialog, Ui_RunWindow):
    def __init__(self, outdir, nozzle_type, field_list, fields, nozzles, scorers, filters):
        super(RunWindow, self).__init__()
        self.setupUi(self)
        self.runthread = RunThread(outdir, nozzle_type, field_list, fields, nozzles, scorers, filters)

        self.outdir = outdir

        self.nozzle_type = nozzle_type
        self.field_checklist = field_list
        self.fields = fields
        self.nozzles = nozzles
        self.scorers = scorers
        self.filters = filters

        self.set_action()

    def set_action(self):
        self.pushOk.clicked.connect(self.click_ok)
        self.runthread.logger_signal.connect(self.update_log)
        self.runthread.progressbar_signal.connect(self.update_progress)

    def show(self):
        super().show()
        self.runthread.start()

    @Slot(str, str)
    def update_log(self, level, message):
        if not any(isinstance(h, LogStringHandler) for h in logging.getLogger().handlers):
            self.logger = logging.getLogger()
            self.logger.setLevel(logging.INFO)
            handler = LogStringHandler(self.textLog)
            self.logger.addHandler(handler)
    
        if level == 'DEBUG':
            self.logger.debug(message)
        elif level == 'INFO':
            self.logger.info(message)
        elif level == 'WARNING':
            self.logger.warning(message)
        elif level == 'ERROR':
            self.logger.error(message)
        elif level == 'CRITICAL':
            self.logger.critical(message)

    @Slot(float)
    def update_progress(self, value):
        self.progressBar.setValue(value)
    
    def click_ok(self):
        self.accept()

    def return_para(self):
        if any(isinstance(h, LogStringHandler) for h in logging.getLogger().handlers):
            logging.shutdown()
            self.logger.disabled = True
            for handler in self.logger.handlers[:]:
                self.logger.removeHandler(handler)
                handler.close()

        return super().exec_()