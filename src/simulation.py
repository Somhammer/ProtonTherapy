import os, sys
from abc import *
class Simulation(metaclass=ABCMeta):
    def __init__(self, convalgo, patient):
        """
        self.name: simulation name. It is displayed in simulation window
        self.convalgo: nozzle parameter. It containes
          Number of Beams, Scatterer, Modulator, Stop Position, Energy, BCM
        self.patient: get Patient class
        """
        self.name = 'Simulation' # Simulation name
        self.convalgo = convalgo
        self.patient = patient

    def make_component(parameters, variables):
        component = ""
        for para in parameters:
            args = para.split("%")[1:]
            vars = {}
            for key, value in variables.items():
                if any("("+key+")" in i for i in args): vars[key] = value
            if len(args) == len(vars): component += para % vars 
    
        return component

    @abstractclassmethod
    def requirement(self):
        pass

    @abstractclassmethod
    def preview(self):
        """
        return requirement, simple information about parameters
        """
        pass
    
    @abstractclassmethod
    def set_parameters(self):
        pass