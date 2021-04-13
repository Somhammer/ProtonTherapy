import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import src.config as cfg

parameters = {
  "virtualSID":230,
  "DoseScalingF":10000,
  "nNodes":0,
  "nHistory":2000,
  "PhaseReuse":5,
  # Relative path from data directory
  "DicomDirectory":"Patient_real",
  "ConvAlgo":"patient.xls"
}

proton = cfg.Proton()
proton.load('dsf_generate_input')
instance = proton.process('GenerateDSFInput')(parameters)
instance.set_parameters()
script = instance.write_scripts()

topas = cfg.Topas()
with open(script,'r') as f:
    cmd = f.readlines()
topas.run(cmd)
