import os, sys, stat
from dataclasses import dataclass, field, InitVar
from datetime import datetime
import math
import numpy as np
import pandas as pd
import pydicom as dicom
import copy

import plugin.simulation as sim
import src.data as data
    
# Naming convention follows the pydicom's one.
@dataclass
class CTinfo(sim.CTinfo):
    PixelSpacing: list = field(default_factory=list)
    Position: list = field(default_factory=list)
    Thickness: float = None
    Rows: int = None
    Cols: int = None
    Manufacturer: str = None
    Center: float = None

@dataclass
class RTPinfo(sim.RTPinfo):
    @dataclass
    class Snout():
        ID: int = None
        Position: float = None

    @dataclass
    class Aperture():
        Thickness: float = None
        Isocenter: float = None
        Data: list = field(default_factory=list)
        Points: int = None
        AirGap: float = None

        RawText: str = None
        OutName: str = None

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

        RawText: str = None
        OutName: str = None

    Snout: InitVar[Snout] = Snout()
    Aperture: InitVar[Aperture] = Aperture()
    Compensator: InitVar[Compensator] = Compensator()
    GantryAngle: float = None
    Isocenter: list = field(default_factory=list)

@dataclass
class RTSinfo(sim.RTSinfo):
    @dataclass
    class Parallel:
        ID: int = None
        Include: bool = None
        Density: float = None
        Contours: list = field(default_factory=list)

    @dataclass
    class Contour:
        ID: int = None
        Size: int = None
        Polygons: list = field(default_factory=list)

    TargetPosition: list = field(default_factory=list)
    Parallels: list = field(default_factory=list)

class DoseSimulation(sim.Simulation):
    def __init__(self, outdir=None, nozzle=None, patient=None, convalgo=None):
        super().__init__(outdir=outdir, nozzle=nozzle, patient=patient, convalgo=convalgo)
        self.requirements['Patient'] = []
        self.requirements['Convalgo'] = [None,None]
        if patient is not None:
            self.requirements['Patient'] = [patient.directory, patient]
        if convalgo is not None:
            self.requirements['Convalgo'] = [convalgo['File'], patient]
        self.order = {"Others":0,"Record":1,"Read":2}

    def is_workable(self):
        return super().is_workable()

    def set_requirement(self, vtype, vname, vari):
        super().set_requirement(vtype, vname, vari)

    def number_of_beams(self):
        super().number_of_beams()
    
    def number_of_pparallels(self):
        super().number_of_parallels()

    def set_import_files(self, key, lst):
        super().set_import_files(key, lst)

    def set_templates(self, writting, templates):
        super().set_templates(writting, templates)

    def read_CT(self, patient):
        if len(patient.CT) == 0: return
        self.dicom = patient.directory
        imageZ = len(patient.CT)
        firstCT_file = dicom.dcmread(os.path.join(patient.directory, patient.CT[0]))
        lastCT_file = dicom.dcmread(os.path.join(patient.directory, patient.CT[-1]))
        
        instance = firstCT_file.InstanceNumber
        img_thick = firstCT_file.SliceThickness
        if img_thick is None: img_thick = 0.0

        firstCT = CTinfo(
          Position = firstCT_file.ImagePositionPatient,
          Thickness = float(img_thick),
          PixelSpacing = firstCT_file.PixelSpacing,
          Rows = firstCT_file.Rows,
          Cols = firstCT_file.Columns,
          Manufacturer = firstCT_file.Manufacturer
        )
        lastCT = copy.deepcopy(firstCT)
        lastCT.position = lastCT_file.ImagePositionPatient

        if firstCT.Position[-1] < firstCT.Position[-1]:
            firstCT.Position[2] = firstCT.Position[2] + (instance - 1) * img_thick
            lastCT.Position[2] = firstCT.Position[2] - (imageZ - instance) * img_thick
        else:
            firstCT.Position[2] = firstCT.Position[2] - (imageZ - instance) * img_thick
            lastCT.Position[2] = firstCT.Position[2] - (instance - 1) * img_thick
        firstCT.Center = (firstCT.Position[2] + lastCT.Position[2]) / 2.0

        self.CT.append(firstCT)
        self.CT.append(lastCT)

    def read_RTP(self, patient, ibeam):
        RTP_file = dicom.dcmread(os.path.join(patient.directory, patient.RTP))
        sequence = RTP_file.IonBeamSequence[ibeam]
        aperture_dir = sequence.IonBlockSequence[0]
        compensator_dir = sequence.IonRangeCompensatorSequence[0]

        convalgo = self.requirements['Convalgo'][1]
        SAD_data = 230 * 10

        RTP = RTPinfo(
          GantryAngle = sequence.IonControlPointSequence[0].GantryAngle,
          Isocenter = sequence.IonControlPointSequence[0].IsocenterPosition
        )

        RTP.Snout.ID = sequence.SnoutSequence[0].SnoutID.replace(' ','').replace('Snout','')
        RTP.Snout.Position = sequence.IonControlPointSequence[0].SnoutPosition

        RTP.Aperture.Thickness = aperture_dir.BlockThickness
        RTP.Aperture.Data = aperture_dir.BlockData
        RTP.Aperture.Isocenter = aperture_dir.IsocenterToBlockTrayDistance
        RTP.Aperture.Points = aperture_dir.BlockNumberOfPoints
        RTP.Aperture.AirGap = 1 - (RTP.Aperture.Isocenter - RTP.Aperture.Thickness) / SAD_data
        
        RTP.Compensator.Isocenter = compensator_dir.IsocenterToCompensatorTrayDistance
        RTP.Compensator.Milling = compensator_dir.CompensatorMillingToolDiameter
        RTP.Compensator.Thickness = compensator_dir.CompensatorThicknessData
        RTP.Compensator.PixelSpacing = compensator_dir.CompensatorPixelSpacing
        RTP.Compensator.Rows = compensator_dir.CompensatorRows
        RTP.Compensator.Cols = compensator_dir.CompensatorColumns

        tmp = (SAD_data - RTP.Compensator.Isocenter) / SAD_data
        RTP.Compensator.PS = [tmp, tmp]
        RTP.Compensator.Thickness = np.array(RTP.Compensator.Thickness)
        RTP.Compensator.Thickness = np.reshape(RTP.Compensator.Thickness, (RTP.Compensator.Rows, RTP.Compensator.Cols))
        RTP.Compensator.MaxThickness = np.amax(RTP.Compensator.Thickness)

        tmp_rows = [0,0]

        for i in range(RTP.Compensator.Cols):
            for j in range(RTP.Compensator.Rows):
                if RTP.Compensator.Thickness[j][i] != RTP.Compensator.MaxThickness:
                    tmp_rows[0] = i + 1
                    break
            if tmp_rows[0] != 0: break
            
        for i in range(RTP.Compensator.Cols-1,0,-1):
            for j in range(RTP.Compensator.Rows-1, 0, -1):
                if RTP.Compensator.Thickness[j][i] != RTP.Compensator.MaxThickness:
                    tmp_rows[1] = i
                    break
            if tmp_rows[1] != 0: break

        tmp_cols1 = [0 for i in range(0,RTP.Compensator.Cols)]
        tmp_cols2 = [0 for i in range(0,RTP.Compensator.Cols)]
        row, col = np.where(RTP.Compensator.Thickness[:RTP.Compensator.Rows, (tmp_rows[0]-1):(tmp_rows[1]+1)] != RTP.Compensator.MaxThickness)
        uni, cnt = np.unique(col, return_counts=True)

        for i in range(len(cnt)):
            tmp_cols1[i] = cnt[i]

        for i in range(tmp_rows[0]-1,tmp_rows[1]+1):
            for j in range(0,RTP.Compensator.Rows):
                if RTP.Compensator.Thickness[j][i] != RTP.Compensator.MaxThickness:
                    tmp_cols2[i] = j
                    break
        
        rel_x = []
        rel_y = []
        rel_thi = []
        tmp_cols = []
        pos = compensator_dir.CompensatorPosition

        for i in range(tmp_rows[0]-1, tmp_rows[1]+1):
            rel_x.append((-pos[0] - (i * RTP.Compensator.PixelSpacing[0])) * RTP.Compensator.PS[0])
            rel_y.append((pos[1] - (tmp_cols2[i] * RTP.Compensator.PixelSpacing[1])) * RTP.Compensator.PS[1])
            tmp = []
            for j in range(tmp_cols2[i], tmp_cols2[i]+tmp_cols1[i-(tmp_rows[0]-1)]):
                tmp.append(RTP.Compensator.MaxThickness - RTP.Compensator.Thickness[j][i])
            rel_thi.append(tmp)
            tmp_cols.append((tmp_cols1[i], tmp_cols2[i], tmp_cols2[i] + tmp_cols1[i-(tmp_rows[0]-1)]))

        RTP.Compensator.RelX = rel_x
        RTP.Compensator.RelY = rel_y
        RTP.Compensator.RelRows = tmp_rows
        RTP.Compensator.RelCols = tmp_cols
        RTP.Compensator.RelThickness = rel_thi

        temp = str(RTP.Aperture.Points) + '\n'
        for i in range(0, RTP.Aperture.Points):
            temp += f'{-RTP.Aperture.Data[2*i] * RTP.Aperture.AirGap:.5g}, {RTP.Aperture.Data[2*i+1] * RTP.Aperture.AirGap:.5g}\n'
        RTP.Aperture.RawText = temp
        RTP.Aperture.OutName = f'aperture/ApertureFileIn{ibeam}.ap'

        temp = f'{RTP.Compensator.RelRows[1] - RTP.Compensator.RelRows[0] + 2}\n{RTP.Compensator.MaxThickness:.5g}\n{RTP.Compensator.Milling:.5g}\n'
        for i in range(len(RTP.Compensator.RelX)):
            pos = f'{RTP.Compensator.RelCols[i][0]:.5g} {-RTP.Compensator.PixelSpacing[0] * RTP.Compensator.PS[0]:.5g} {RTP.Compensator.RelY[i]:.5g} {RTP.Compensator.RelX[i]:.5g}\n'
            relthi = ''
            for j in RTP.Compensator.RelThickness[i]:
                relthi += f'{j:.5g} '
            temp += pos + relthi + '\n'
        temp +='0 0'
        RTP.Compensator.RawText = temp
        RTP.Compensator.OutName = f'compensator/CompensatorFileInRowsepths{ibeam}.rc'

        self.RTP.append(RTP)

    def read_RTS(self, patient):
        if len(self.CT) < 2: return
        RTS_file =  dicom.dcmread(os.path.join(patient.directory, patient.RTS))

        target_pos = [
              (2 * self.CT[0].Position[0] + (self.CT[0].Rows - 1) * self.CT[0].PixelSpacing[0]) / 2 - self.RTP[0].Isocenter[0], # x
              (2 * self.CT[0].Position[1] + (self.CT[0].Cols - 1) * self.CT[0].PixelSpacing[1]) / 2 - self.RTP[0].Isocenter[1], # y
              self.CT[0].Center - self.RTP[0].Isocenter[2] # z
        ]

        RTS = RTSinfo(TargetPosition=target_pos)

        parallel = []
        for iparallel in range(len(RTS_file.ROIContourSequence)):
            sequence = RTS_file.ROIContourSequence[iparallel]
            observation = RTS_file.RTROIObservationsSequence[iparallel]
            try:
                len(sequence.ContourSequence)
            except:
                continue

            try:
                density = float(observation.ROIPhysicalPropertiesSequence[0].ROIPhysicalPropertyValue)
                include = True
            except:
                density = 0.0
                include = False

            contours = []
            if sequence.ContourSequence is not None:
                for icontour in range(len(sequence.ContourSequence)):
                    csequence = sequence.ContourSequence[icontour]
                    contours.append(RTS.Contour(
                        ID = icontour,
                        Size = csequence.NumberOfContourPoints,
                        Polygons = csequence.ContourData
                    ))
            RTS.Parallels.append(RTS.Parallel(
              ID = iparallel,
              Include = include,
              Density = density,
              Contours = contours
            ))
        self.RTS = RTS
        
    def set_parameters(self, ibeam):
        def set_value(value, ibeam):
            if str(type(value)) == "<class 'list'>":
                return value[ibeam]
            else:
                return value

        convalgo = self.requirements['Convalgo'][1]
        patient = self.requirements['Patient'][1]

        kwargs = {
          'nNodes':f'0', 
          'nSize':f'{len(convalgo["BCM"][0])}',
          'Stop':f'{convalgo["Stop Position"][0]/256*100:.5g}',
          'BCM':'0 0 0 '+' '.join(str(convalgo['BCM'][0][i]) for i in range(3,len(convalgo['BCM'][0]))), 
          'BWT':' '.join(f'{i:.5g}' for i in convalgo['BWT'][0]),
          'S1Number':int(set_value(convalgo['1st Scatterer'][0], ibeam)),
          'S2Angle':int(set_value(convalgo['2nd Scatterer'][0], ibeam)),
          'SnoutID':f'{self.RTP[ibeam].Snout.ID}',
          'SnoutTransZ':f'{-self.RTP[ibeam].Compensator.Isocenter - self.RTP[ibeam].Compensator.MaxThickness - 312.5:.5g}',
          'PhaseSpaceOutput':os.path.join(self.outdir, f'PhaseSpace_beam{ibeam}'),
          'PDDOutput':os.path.join(self.outdir, f'PDD_beam{ibeam}'),
          'DoseAtPhantomOutput':os.path.join(self.outdir, f'DoseAtPhantom_beam{ibeam}'),
          'nSequentialTimes':int(set_value(convalgo['Stop Position'][0], ibeam)),
          'DicomDirectory': patient.directory,
          'ApertureFile':os.path.join(self.outdir, self.RTP[ibeam].Aperture.OutName),
          'CompensatorFile':os.path.join(self.outdir, self.RTP[ibeam].Compensator.OutName),
          'Energy':f'{set_value(convalgo["Energy"][0], ibeam):.5g}',
          'RMTrack':int(set_value(convalgo['Modulator'][0], ibeam))
        }
        espread = (1.0289 - 0.0008 * (math.log(set_value(convalgo['Energy'][0], ibeam)) - 3.432) / 0.5636) / set_value(convalgo['Energy'][0], ibeam) * 100
        kwargs['EnergySpread'] = f'{espread:.5g}'
        kwargs['RMSmallTrack'] = int((kwargs['RMTrack'] + 2) % 3)
        kwargs['RMSmallWheel'] = int((kwargs['RMTrack'] + 2) / 3)

        kwargs['nParallels'] = len(self.RTS.Parallels)
        parallels = ""
        for parallel in self.RTS.Parallels:
            parallels += f"PatientParallel{parallel.ID} "
        kwargs['ParallelName'] = parallels

        return kwargs

    def change_parameters(self, template, **kwargs):
        return super().change_parameters(template, **kwargs)

    def save_filters(self, ibeam):
        RTP = self.RTP[ibeam]
        aperture = {'OutName':RTP.Aperture.OutName, 'RawText':RTP.Aperture.RawText}
        compensator = {'OutName':RTP.Compensator.OutName, 'RawText':RTP.Compensator.RawText}
        outlist = []
        outlist.append(aperture)
        outlist.append(compensator)
        return outlist

    def save_phase(self, ibeam, **kwargs):
        if not "Patient" in self.phases:
            self.phases["Patient"] = []
        for parallel in self.RTS.Parallels:
            parallel_template = copy.deepcopy(self.templates['Parallel'][0])
            kwargs = {
                "PatientParallelName":f"PatientParallel{parallel.ID}",
                "Material":"Contour",
                "ParallelTransX":f'{self.RTS.TargetPosition[0]:.5g}',
                "ParallelTransY":f'{self.RTS.TargetPosition[1]:.5g}',
                "ParallelTransZ":f'{self.RTS.TargetPosition[2]:.5g}',
            }
            patient = self.change_parameters(parallel_template, **kwargs)

            contours = []
            for contour in parallel.Contours:
                contour_template = copy.deepcopy(self.templates['Contour'][0])
                idx = np.arange(0, contour.Size*3, 3) + 2
                z = contour.Polygons[2]
                polygons = np.delete(np.array(contour.Polygons), idx)
                polygons = " ".join(f'{i:.5g}' for i in contour.Polygons) + ' mm'
                kwargs = {
                  "ContourName": f"Contour{contour.ID}",
                  "Material":"Contour",
                  "ContourHLZ":f'{self.CT[0].Thickness/2.0:.5g}',
                  'ContourTransZ':f'{z - self.CT[0].Center:.5g}',
                  'nPolygons':f'{contour.Size}',
                  'Polygons':f'{polygons}',
                  'ParallelWorldName':parallel_template.name
                }
                contours.append(self.change_parameters(contour_template, **kwargs))
            
            for contour in contours:
                patient.modify_subcomponent(kwargs['ContourName'], contour.subcomponent['Basis'].parameters)
            patient.outname = os.path.join(self.outdir, 'parallels', f'PatientParallel{parallel.ID}.tps')
            self.phases['Patient'].append(patient)

            kwargs = self.set_parameters(ibeam)
            super().save_phase(ibeam, **kwargs)

    def run(self):
        return super().run()