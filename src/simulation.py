import os, sys
import copy
from dataclasses import dataclass, field, InitVar
import pydicom as dicom

import data

@dataclass
class CTinfo:
    ID: int = None

@dataclass
class RTPinfo:
    ID: int = None

@dataclass
class RTSinfo:
    ID: int = None

class Simulation():
    def __init__(self, outdir='', nozzle=None, patient=None, convalgo=None):
        self.name = "New Simulation"
        self.outdir = outdir

        self.nbeams = 1
        self.nparallel = 1

        self.workable = False
        self.requirements = {'Nozzle':[None, None]}
        if nozzle is not None:
            self.requirements['Nozzle'] = [nozzle, nozzle]
  
        # For TOPAS Inputs
        self.keys = ["Read","Record","Others"]
        tmp = data.Component(btype="tmp", phase=True)
        self.tkeys = list(tmp.component_list().keys()) + self.keys
        del tmp

        self.imported = {i:[] for i in self.keys}
        self.writting = {}
        self.templates = {}
        self.components = {i:None for i in self.tkeys}

        self.CT = []
        self.RTP = []
        self.RTS = []

        self.phases = {i:[] for i in self.keys}
        self.filters = [{'OutName':'','RawText':''}]
        self.contours = [{'OutName':'','RawText':''}]

    def is_workable(self):
        workable = True
        requirements = [] # variable name : set up(T/F)
        
        for key, value in self.requirements.items():
            if value[1] is None: requirements.append(False)
            elif value[0] == '': requirements.append(False)
            else: requirements.append(True)

        if any(not i for i in requirements): self.workable = False
        else: self.workable = True

        return self.workable

    def set_requirement(self, vtype, vname, vari):
        if not any(vtype == key for key in self.requirements.keys()):
            return
        self.requirements[vtype][0] = vname
        self.requirements[vtype][1] = vari
        self.is_workable()

    def number_of_beams(self):
        patient = self.requirements['Patient'][1]
        if patient.directory == '': return
        if patient.RTP is None:
            self.nbeams = 1
        else:
            RTP = dicom.dcmread(os.path.join(self.patient.directory, self.patient.RTP))
            self.nbeams = RTP.FractionGroupSequence[0].NumberOfBeams

    def number_of_parallels(self):
        patient = self.requirements['Patient'][1]
        if patient.directory == '': return
        if patient.RTS is None:
            self.nparallel = 1
        else:
            RTS = dicom.dcmread(os.path.join(self.patient.directory, self.patient.RTS))
            self.nparallel = len(RTS.ROIContourSequence)

    def set_import_files(self, key, lst):
        self.imported[key] = lst
        
    def set_templates(self, writting, templates):
        self.writting = writting

        self.templates = {}
        for name, template in templates.items():
            if not any(template.ctype == key for key in self.templates.keys()):
                self.templates[template.ctype] = []
            self.templates[template.ctype].append(template)

    def read_CT(self, patient):
        if len(patient.CT) == 0: return
        #CT = CTinfo()
        # Write yourself.
        # You can add variable into CTinfo like
        #     CT.varname = value
        # or write CTinfo dataclass directly.
        # After reading, you should write save part like,
        #     self.CT.append(CT)

    def read_RTP(self, patient, ibeam):
        if patient.RTP is None: return
        #RTP = RTPinfo()
        # Write yourself.
        # After reading, you should write save part like,
        #     self.RTP.append(RTP)

    def read_RTS(self, patient):
        if patient.RTS is None: return
        #RTS = RTSinfo()
        # Write yourself.
        # After reading, you should write save part like,
        #     self.RTS.append(RTS)

    def calculate_parameters(self, ibeam):
        kwargs = {}
        # Write yourself.
        # After calculation, you should write return part like,
        return kwargs

    def save_filters(self, ibeam):
        # Write yourself.
        pass

    def save_phase(self, **kwargs):
        if not self.workable: return
        for key in self.keys:
            phase = data.Component(self.requirements['Nozzle'][1])
            for ctype, templates in self.templates.items():
                if not any(ctype == i[0] for i in self.writting[key]): continue
                for template in templates:
                    if not any(template.name == i[1] for i in self.writting[key]): continue
                    component = copy.deepcopy(template)
                    for subname, subcomp in component.subcomponent.items():
                        for para in subcomp.parameters:
                            if any(para.fullname == name for name in kwargs.keys()):
                                para.value = kwargs[name]
                            para.draw = True
                    phase.modify_subcomponent(subname=ctype, paras=subcomp.parameters)
            phase.ctype = key
            for item in self.imported[key]:
                phase.modify_file(item)

            self.phases[key] = phase

    def run(self):
        if "Patient" in self.requirements:
            patient = self.requirements['Patient'][1]
            if not self.workable: return
            if patient is not None:
                self.read_CT(patient)
                for ibeam in range(self.nbeams):
                    self.read_RTP(patient, ibeam)
                self.read_RTS(patient)
        
        for ibeam in range(self.nbeams):
            kwargs = self.calculate_parameters(ibeam)
            filters = self.save_filters(ibeam)
            if filters is not None: self.filters += filters
            self.save_phase(**kwargs)
        
        return self.phases, self.filters