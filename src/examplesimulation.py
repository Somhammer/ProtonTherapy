import os, sys
import copy
from dataclasses import dataclass, field, InitVar
import simulation as sim

@dataclass
class CTinfo(sim.CTinfo):
    pass

@dataclass
class RTPinfo(sim.RTPinfo):
    @dataclass
    class Snout():
        ID: int = None

    snout: InitVar[Snout] = Snout()
    arr: list = field(default_factory=list)

@dataclass
class RTSinfo(sim.RTSinfo):
    pass

class ExampleSimulation(sim.Simulation):
    def __init__(self, outdir='', nozzle=None, patient=None, convalgo=None):
        super().__init__()
    
    def is_workable(self):
        super().is_workable()

    def set_requirement(self, vtype, vname, vari):
        super().set_requirement()

    def number_of_beams(self):
        super().number_of_beams()
    
    def number_of_pparallels(self):
        super().number_of_parallels()

    def set_import_files(self, key, lst):
        super().set_import_files()

    def set_templates(self, writting, templates):
        super().set_templates()

    def read_CT(self, patient, ibeam):
        super().read_CT()

    def read_RTP(self, patient, ibeam):
        super().read_RTP()

    def read_RTS(self, patient, ibeam):
        super().read_RTS()
        
    def calculate_parameters(self, ibeam):
        super().calculate_parameters()

    def save_filters(self, ibeam):
        super().save_filters()

    def save_phase(self, **kwargs):
        super().save_phase()

    def run(self):
        super().run()