import os, sys
from datetime import datetime
base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(base_path)

import src.config as cfg

parameters = {
  "virtualSID":230,
  "DoseScalingF":10000,
  "nNodes":0,
  "nHistory":2000,
  "PhaseReuse":5,
  # Relative path from data directory
  "DicomDirectory":"Patient_real",
  "ConvAlgo":"patient.xls",
  # Relative path from prod directory
  "Output":datetime.today().strftime('%y%m%d')
}

proton = cfg.Proton()
proton.load('dose_backup')
instance = proton.process('DoseSimulation')(parameters)
instance.set_parameters()
para, script = instance.write_scripts()

topas = cfg.Topas()
with open(script,'r') as f:
    cmd = f.readlines()
topas.run(cmd)

files = [f
        for f in os.listdir(os.path.join(base_path, 'prod', parameters['Output'])) 
        if f.endswith('csv')]
scales = instance.calculate_sobp(files)
instance.postprocess(para, scales)
