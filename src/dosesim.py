import os, sys, stat
import simulation as sim
from dataclasses import dataclass, field
from datetime import datetime
import math
import numpy as np
import pandas as pd
import pydicom as dicom

class DoseSimulation(sim.Simulation):
    @dataclass
    class CTinfo:
        pixel_spacing: list = field(default_factory=list)
        position: list = field(default_factory=list)
        thickness: float = None

    @dataclass
    class Geometry:
        manufacturer: str = None
        gantry_angle: float = None
        isocenter: list = field(default_factory=list)

    @dataclass
    class Snout:
        id: str = None
        position: float = None

    @dataclass
    class Aperture:
        aper_num: int = None
        thickness: float = None
        iso_dist: float = None
        airgap: float = None
        data: list = field(default_factory=list)
    
    @dataclass
    class Compensator:
        isocenter: float = None
        milling: float = None
        max_thickness: float = None
        rel_thickness: list = field(default_factory=list) 
        x: list = field(default_factory=list) 
        y: list = field(default_factory=list)
        rows: list = field(default_factory=list)
        cols: list = field(default_factory=list)
        pixel: list = field(default_factory=list)
        ps: list = field(default_factory=list)
        
    @dataclass
    class Parallel: 
        parallel_num: int = None
        include: bool = None
        target_pos: list = field(default_factory=list)
        ct_center: float = None
        iso_z: float = None
        density: float = None
        img_thickness: float = None
        contour: list = field(default_factory=list)

    @dataclass
    class Contour:
        contour_num: int = None
        size: int = None
        polygons: list = field(default_factory=list)
        
    def __init__(self, parameters, outdir):
        super().__init__(parameters, outdir))
        self.name = 'ExampleSimulation'
        
        print("First CT:", self.firstCT)
        print("Last CT:", self.lastCT)
        print("RT Plan:", self.RTP)
        print("RT Structure:", self.RTS)
        
        self.ct = None
        self.geometry = []
        self.snout = []
        self.aperture = []
        self.compensator = []
        self.parallel = []
        
    def get_convalgo_and_dicoms(self, conv, dicom):
        super().get_convalgo_and_dicoms(conv, dicom)
        
    def set_nozzle_parameters(self):
        return
        
    def set_patient_parameters(self):
        return 
    
    def generate_topas_input(self):
        super().generate_topas_input()
        
    def generate_topas_script(self):
        super().generate_topas_script()
        
    def do_postprocess(self):
        super().do_postprocess()