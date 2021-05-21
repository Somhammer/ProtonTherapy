import os, sys, stat
import simulation as sim
from dataclasses import dataclass, field
from datetime import datetime
import math
import numpy as np
import pandas as pd
import pydicom as dicom
import copy

import data

class DoseSimulation(sim.Simulation):
    # Naming convention in data classes follows the pydicom's one.
    @dataclass
    class CTinfo:
        PixelSpacing: list = field(default_factory=list)
        Position: list = field(default_factory=list)
        Center: float = None
        Thickness: float = None
        Rows: int = None
        Cols: int = None
        Manufacturer: str = None

    @dataclass
    class RTPinfo:
        Snout: self.Snout()
        Aperture: self.Aperture()
        Compensator: self.Compensator()
        GantryAngle: float = None
        Isocenter: list = field(default_factory=list)
        
    @dataclass
    class Snout:
        ID: str = None
        Position: float = None

    @dataclass
    class Aperture:
        Thickness: float = None
        Isocenter: float = None
        Data: list = field(default_factory=list)
        Points: int = None
        AirGap: float = None

    @dataclass
    class Compensator:
        Isocenter: float = None
        Milling: float = None
        Rows: int = None
        Cols: int = None
        PixelSpacing: list = field(default_factory=list)
        PS: list = field(default_factory=list)
        Thickness: list = field(default_factory=list)
        MaxThickness: float = None

        RelThickness: list = field(default_factory=list)
        RelRows: list = field(default_factory=list)
        RelCols: list = field(default_factory=list)
        RelX: list = field(default_factory=list) 
        RelY: list = field(default_factory=list)

    @dataclass
    class RTSinfo:
        TargetPosition = list = field(default_factory=list)
        Parallel: list = field(default_factory=list)

    @dataclass
    class Parallel: 
        Index: int = None
        Include: bool = None
        Density: float = None
        Contour: list = field(default_factory=list)

    @dataclass
    class Contour:
        Index: int = None
        Size: int = None
        Polygons: list = field(default_factory=list)
        
    def __init__(self):
        super().__init__(parameters, outdir)
        self.name = 'DoseSimulation'

        self.workable = False
        self.convalgo = None
        self.patient = None
        self.paras = {
          "VirtualSID": None,
          "nNodes": None,
          "nHistories": None,
          "PhaseReuse": None
        }

        self.firstCT = None
        self.lastCT = None
        self.RTP = []
        self.RTS = None

    def requirement(self):
        requirement = ["ConvAlgo", "Patient"] + list(self.paras.keys())
        return requirement

    def is_workable(self):
        if any(i is not None for i in [self.convalgo, self.patient]):
            if any(i is not None for i in self.paras.values()):
                self.workable = True
        return self.workable

    def set_convalgo(self, conv):
        self.convalgo = conv
        return self.is_workable()

    def set_patient(self, patient):
        self.patient = patient
        return self.is_workable()

    def set_paras(self, **kwargs):
        for key, value in kwargs:
            self.paras[key] = value
        return self.is_workable()

    def preview(self):
        return

    def set_parameters(self, g_component):
        if not self.workable: return
        
        self.read_CT()
        RTP = dicom.dcmread(self.patient.RTP)
        RTS = dicom.dcmread(self.patient.RTS)

        nbeam = RTP.FractionGroupSequence[0].NumberOfBeams
        for ibeam in range(nbeam):
            self.RTP.append(self.read_RTP(RTP, ibeam))
        self.read_RTS(RTS)
    

    def read_CT(self):
        imageZ = len(self.patient.CT)
        firstCT = dicom.dcmread(self.patient.CT[0])
        lastCT = dicom.dcmread(self.patient.CT[-1])
        
        instance = firstCT.InstanceNumber
        img_thick = firstCT.SliceThickness
        if img_thick is None: img_thick = 0.0

        self.firstCT = self.CTinfo(
          position = firstCT.ImagePositionPatient,
          thickness = float(img_thick),
          pixel_spacing = firstCT.PixelSpacing,
          row = firstCT.Rows,
          col = firstCT.Columns,
          manufacturer = firstCT.Manufacturer
        )
        self.lastCT = copy.deepcopy(self.firstCT)
        self.lastCT.position = lastCT.ImagePositionPatient

        if self.firstCT.position[-1] < self.firstCT.position[-1]:
            self.firstCT.position[2] = self.firstCT.position[2] + (instance - 1) * img_thick
            self.lastCT.position[2] = self.firstCT.position[2] - (imageZ - instance) * img_thick
        else:
            self.firstCT.position[2] = self.firstCT.position[2] - (imageZ - instance) * img_thick
            self.lastCT.position[2] = self.firstCT.position[2] - (instance - 1) * img_thick

    def read_RTP(self, RTP, ibeam):
        sequence = RTP.IonBeamSequence[ibeam]
        dir_aper = sequence.IonBlockSequence[0]
        dir_compen = sequence.IonRangeCompensatorSequence[0]

        SAD_data = float(self.paras['VirtualSID']) * 10

        snout = self.Snout(
          ID = sequence.SnoutSequence[0].SnoutID.replace(' ','').replace('Snout',''),
          Position = sequence.IonControlPointSequence[0].SnoutPosition
        )

        aperture = self.Aperture(
          Thickness = dir_aper.BlockThickness,
          Data = dir_aper.BlockData,
          Isocenter = dir_aper.IsocenterToBlockTrayDistance, 
          Points = dir_aper.BlockNumberOfPoints
        )
        aperture.AirGap = 1 - (aperture.IsocenterToBTD - aperture.Thickness) / SAD_data
        
        compensator = self.Compensator(
          Isocenter = dir_compen.IsocenterToCompensatorTrayDistance,
          Milling = dir_compen.CompensatorMillingToolDiameter,
          Thickness = dir_compen.CompensatorThicknessData,
          PixelSpacing = dir_compen.CompensatorPixelSpacing,
          Rows = dir_compen.CompensatorRows,
          Cols = dir_compen.CompensatorColumns
        )
        tmp = (SAD_data - compensator.Isocenter) / SAD_data
        compensator.PS = [tmp, tmp]
        compensator.Thickness = np.array(compensator.Thickness)
        compensator.Thickness = np.reshape(compensator.Thickness, (compensator.Rows, compensator.Cols))
        compensator.MaxThickness = np.amax(compensator.Thickness)

        tmp_rows = [0,0]

        for i in range(compensator.Cols):
            for j in range(compensator.Rows):
                if compensator.Thickness[j][i] != compensator.MaxThickness:
                    tmp_rows[0] = i + 1
                    break
            if tmp_rows[0] != 0: break
            
        for i in range(compensator.Cols-1,0,-1):
            for j in range(compensator.Rows-1, 0, -1):
                if compensator.Thickness[j][i] != compensator.MaxThickness:
                    tmp_rows[1] = i
                    break
            if tmp_rows[1] != 0: break

        tmp_cols1 = [0 for i in range(0,compensator.Cols)]
        tmp_cols2 = [0 for i in range(0,compensator.Cols)]
        row, col = np.where(compensator.Thicknesshick[:compensator.Rows, (tmp_rows[0]-1):(tmp_rows[1]+1)] != compensator.MaxThickness)
        uni, cnt = np.unique(col, return_counts = True)

        for i in range(len(cnt)):
            tmp_cols1[i] = cnt[i]

        for i in range(tmp_rows[0]-1,tmp_rows[1]+1):
            for j in range(0,compensator.Rows):
                if compensator.Thickness[j][i] != compensator.MaxThickness:
                    tmp_cols2[i] = j
                    break
        
        rel_x = []
        rel_y = []
        rel_thi = []
        tmp_cols = []
        pos = dir_compen.CompensatorPosition

        for i in range(tmp_rows[0]-1, tmp_rows[1]+1):
            rel_x.append((-pos[0] - (i * compensator.PixelSpacing[0])) * compensator.PS[0])
            rel_y.append((pos[1] - (tmp_cols2[i] * compensator.PixelSpacing[1])) * compensator.PS[1])
            tmp = []
            for j in range(tmp_cols2[i], tmp_cols2[i]+tmp_cols1[i-(tmp_rows[0]-1)]):
                tmp.append(compensator.MaxThickness - compensator.Thickness[j][i])
            rel_thi.append(tmp)
            tmp_cols.append((tmp_cols1[i], tmp_cols2[i], tmp_cols2[i] + tmp_cols1[i-(tmp_rows[0]-1)]))

        compensator.RelX = rel_x
        compensator.RelY = rel_y
        compensator.RelRows = tmp_rows
        compensator.RelCols = tmp_cols
        compensator.RelThickness = rel_thi

        RTP = self.RTPinfo(
          Snout = snout,
          Aperture = aperture,
          Compensator = compensator,
          GantryAngle = sequence.IonControlPointSequence[0].GantryAngle,
          Isocenter = sequence.IonControlPointSequence[0].IsocenterPosition
        )

        return RTP

    def read_RTS(self, RTS):
        if self.firstCT is None: return
        if self.lastCT is None: return

        target_pos = [
              (2 * self.firstCT.Position[0] + (self.firstCT.Rows - 1) * self.firstCT.PixelSpacing[0]) / 2 - RTP.Isocenter[0], # x
              (2 * self.firstCT.Position[1] + (self.firstCT.Cols - 1) * self.firstCT.PixelSpacing[1]) / 2 - RTP.Isocenter[1], # y
              self.firstCT.Center - RTP.Isocenter[2] # z
        ]

        parallel = []
        for iparallel in range(len(RTS.ROIContourSequence)):
            sequence = RTS.ROIContourSequence[iparallel]
            observation = RTS.RTROIObservationsSequence[iparallel]
            try:
                density = float(observation.ROIPhysicalPropertiesSequence[0].ROIPhysicalPropertyValue)
                include = True
            except:
                density = 0.0
                include = False

            idx = 0
            contour = []
            if sequence.ContourSequence is not None:
                for icontour in range(len(sequence.ContourSequence)):
                    csequence = sequence.ContourSequence[icontour]
                    contour.append(self.Contour(
                    Index = icontour,
                    Size = csequence.NumberOfContourPoints,
                    Polygons = csequence.ContourData
                    ))

            parallel.append(self.Parallel(
              Index = iparallel,
              Include = include,
              Density = density,
              Contour = contour
            ))
        self.RTS = self.RTSinfo(Parallel=parallel, TargetPosition=target_pos)

    def nozzle_template(self, ibeam, tname):
        pass

    def save_nozzle(self, ibeam, g_component):
        output = data.Component()
        pass

    def save_patient(self, iparallel):
        output = data.Component()
        if self.patient.is_real:
            pass
        else:
            pass

"""
    def add_subcomponent(self):
        if not self.comboComp.currentText() == "Load":
            newtab = NewTab(self, self.template.component_list()[self.template.ctype])
        else:
            newtab = NewTab(self, [])
        r = newtab.return_para()
        if r:
            subcomp = newtab.comboSubcomp.currentText()
            tabname = newtab.lineTabName.text()
            fname = os.path.join(base_path,'data/components',self.comboComp.currentText(),subcomp+'.tps')
            self.template.load(fname=fname)
            self.template.modify_subname(subcomp, tabname)
            index = self.draw_para_widget(tabname=tabname)
            self.tabComp.setCurrentIndex(index)
"""