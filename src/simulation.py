import os, sys
from abc import *
class Simulation(metaclass=ABCMeta):
    def __init__(self, parameters, outdir):
        self.name = 'Simulation' # Simulation name
        #self.allcomponents = components # All components generated from MainWindow
        self.allparameters = parameters # All Parameters generated from MainWindow
        self.parameters = {
          # Parameters of which the values are changed by other files(convalgo, dicom).
          # Shape: {component:{subcomponent:{parameter name:value, ...}, ...}, ...}
        }
        
        self.base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        sys.path.append(self.base_path)
        
        self.outdir = outdir
        self.nozzle = os.path.join(self.outdir, 'nozzle')
        self.patient = os.path.join(self.outdir, 'patient')
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)
        if not os.path.exists(self.nozzle):
            os.makedirs(self.nozzle)
        if not os.path.exists(self.patient):
            os.makedirs(self.patient)
            
    @abstractclassmethod
    def get_convalgo_and_dicoms(self, conv, dicom):
        import getconvalgo
        tmp = conv.split('/')
        conv_dir = '/'.join(i for i in tmp[:-1])
        conv_name = tmp[-1]
        self.convalgo = getconvalgo.GetParaFromConvAlgo(conv_dir, conv_name)
        
        import pydicom as dicom
        self.RTP = None
        self.RTS = None
        self.RD = None
        self.CT = []
        for i in os.listdir(os.path.join(dicom)):
            if not i.endswith('.dcm'): continue
            if i.startswith('RN'): self.RTP = i
            elif i.startswith('RS'): self.RTS = i
            elif i.startswith('RD'): self.RD = i            
            else: self.CT.append(i)
        self.CT.sort()
    
    @abstractclassmethod
    def set_nozzle_parameters(self):
        pass
    
    @abstractclassmethod
    def set_patient_parameters(self):
        pass
    
    @abstractclassmethod
    def generate_topas_input(self):
        # if len(self.parameters) > 0 -> Matching and change
        # Then write topas input files for each components
        # Lastly, write main file which should contain all files
        pass
        
    @abstractclassmethod
    def generate_topas_script(self):
        # Write topas script for each beam step
        pass
    
    @abstractclassmethod
    def do_postprocess(self):
        # Post process after running
        pass