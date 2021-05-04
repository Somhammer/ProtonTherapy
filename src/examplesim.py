import os, sys
import simulation as sim
class ExampleSimulation(sim.Simulation):
    def __init__(self, parameters, outdir):
        super().__init__(parameters, outdir)
        self.name = 'ExampleSimulation'
        self.components = ['Aperture','Compensator','Contour']
    
    def set_parameters_from_convalgo(self, path, conv):
        super().set_parameters_from_convalgo(path, conv)
        
    def set_parameters_from_dicoms(self, path, dicom):
        super().set_parameters_from_dicom(path, dicom)
        
    def generate_topas_input(self):
        super().generate_topas_input()
        
    def generate_topas_script(self):
        super().generate_topas_script()
        
    def do_postprocess(self):
        super().do_postprocess()