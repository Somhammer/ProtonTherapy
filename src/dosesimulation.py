import os, sys, stat
from dataclasses import dataclass, field, InitVar
from datetime import datetime
import math
import numpy as np
import pandas as pd
import pydicom as dicom
import copy

import simulation as sim
import data
    
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
    def __init__(self, outdir='', nozzle=None, patient=None, convalgo=None):
        super().__init__()
        self.requirements['Patient'] = []
        self.requirements['Convalgo'] = []
        if patient is not None:
            self.requirements['Patient'] = [patient.directory, patient]
        if convalgo is not None:
            self.requirements['Convalgo'] = [convalgo['File'], patient]

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

    def read_CT(self, patient):
        if len(patient.CT) == 0: return
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

        self.CT.append(firstCT, lastCT)

    def read_RTP(self, patient, ibeam):
        RTP_file = dicom.dcmread(os.path.join(patient.directory, patient.RTP))
        sequence = RTP_file.IonBeamSequence[ibeam]
        aperture_dir = sequence.IonBlockSequence[0]
        compensator_dir = sequence.IonRangeCompensatorSequence[0]

        convalgo = self.requirements['Convalgo'][1]
        SAD_data = float(convalgo['VirtualSID']) * 10

        RTP = RTPinfo(
          GantryAngle = sequence.IonControlPointSequence[0].GantryAngle,
          Isocenter = sequence.IonControlPointSequence[0].IsocenterPosition
        )

        RTP.Snout.ID = sequence.SnoutSequence[0].SnoutID.replace(' ','').replace('Snout',''),
        RTP.Snout.Position = sequence.IonControlPointSequence[0].SnoutPosition

        RTP.Aperture.Thickness = aperture_dir.BlockThickness
        RTP.Aperture.Data = aperture_dir.BlockData,
        RTP.Aperture.Isocenter = aperture_dir.IsocenterToBlockTrayDistance, 
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

        RTS = RTSinfo(TargetPosition=target_pos)

        target_pos = [
              (2 * self.CT[0].Position[0] + (self.CT[0].Rows - 1) * self.CT[0].PixelSpacing[0]) / 2 - self.RTP[0].Isocenter[0], # x
              (2 * self.CT[0].Position[1] + (self.CT[0].Cols - 1) * self.CT[0].PixelSpacing[1]) / 2 - self.RTP[0].Isocenter[1], # y
              self.CTcenter - self.RTP[0].Isocenter[2] # z
        ]

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
                        Index = icontour,
                        Size = csequence.NumberOfContourPoints,
                        Polygons = csequence.ContourData
                    ))
            RTS.Parallels.append(RTS.Parallel(
              ID = iparallel,
              Include = include,
              Density = density,
              Contour = contours
            ))
        self.RTS = RTS
        
    def calculate_parameters(self, ibeam):
        super().calculate_parameters()

    def save_filters(self, ibeam):
        RTP = self.RTP[ibeam]
        aperture = {'OutName':RTP.Aperture.OutName, 'RawText':RTP.Aperture.RawText}
        compensator = {'OutName': RTP.Compensator.OutName, 'RawText':RTP.Compensator.RawText}

        return [aperture, compensator]

    def save_phase(self, **kwargs):
        super().save_phase()

    def run(self):
        super().run()

    def set_parameters(self, g_component):
        if not self.workable: return
        
        self.read_CT()
        RTP = dicom.dcmread(os.path.join(self.patient.directory, self.patient.RTP))
        RTS = dicom.dcmread(os.path.join(self.patient.directory, self.patient.RTS))

        nbeam = RTP.FractionGroupSequence[0].NumberOfBeams
        for ibeam in range(nbeam):
            self.RTP.append(self.read_RTP(RTP, ibeam))
        self.read_RTS(RTS)
    
        for ibeam in range(nbeam):
            self.save_nozzle(ibeam, g_component)

        for iparallel in range(len(self.RTS.Parallel)):
            self.output['Parallels'].append(self.save_parallel(iparallel))

    def nozzle_template(self, category, **kwargs):
        name = kwargs['Name']
        if category.lower() == "control":
            return {
              "Ts/PauseBeforeSequence":'"False"',
              "i:Ts/ShowHistoryCountAtInterval":"0",
              "i:Ts/NumberOfThreads":f"{kwargs['nNodes']}",
              "i:Ts/MaxInteruptedHistories":"10000000",
            }
        elif category.lower() == "time":
            return {
              "d:Tf/TimelineEnd":f"{kwargs['Stop']} ms",
              "i:Tf/NumberOfSequentialTimes":f"{kwargs['nSequentialTimes']}",
              "dv:Tf/BeamWeight/Times":f"{kwargs['nSize']} {kwargs['BWT']} ms",
              "iv:Tf/BeamWeight/Values":f"{kwargs['nSize']} {kwargs['BCM']}",
              "s:Tf/BeamCurrent/Function":'"Step"',
              "dv:Tf/BeamCurrent/Times":"1 100 ms",
              "iv:Tf/BeamCurrent/Values":"1 2000",
            }
        elif name.lower() == "phase":
            return {
              "s:So/PhaseSpace/Type":'"PhaseSpace"',
              's:So/PhaseSpace/Component':'"World"',
              's:So/PhaseSpace/PhaseSpaceFileName':f"{kwargs['PSFile']}",
              'i:So/PhaseSpace/PhaseSpaceMultipleUse':'5'
            }
        elif category.lower() == "rmw" or category.lower() == 'rangemodulator':
            return {
              f"s:Tf/{kwargs['Name']}_Rotation/Function":'"Linear deg"',
              f"d:Tf/{kwargs['Name']}_Rotation/Rate":"3.6 deg/ms",
              f"d:Tf/{kwargs['Name']}_Rotation/StartValue":f"Ge/{kwargs['Name']}/Track/zero_angle deg",
              f"d:Tf/{kwargs['Name']}_Rotation/RepetitionInterval":"100.0 ms",
              f"d:Ge/{kwargs['Name']}/Track/zero_angle":f"Ge/{kwargs['Name']}/Track{kwargs['RMTrack']} - Ge/{kwargs['Name']}/Small/Track{kwargs['RMSmallTrack']} deg",
              f"Ge/{kwargs['Name']}/SmallWheel{kwargs['RMSmallWheel']}/RotZ":f"Tf/{kwargs['Name']}_Rotation/Value deg",
              f"Ge/{kwargs['Name']}/Track":f"-1 * Ge/{kwargs['Name']}/Track{kwargs['RMTrack']} deg"
            }
        elif category.lower() == "scatterer1":
            return {
              f"Ge/{kwargs['Name']}/Lollipop{kwargs['S1Number']}":f"Ge/{kwargs['Name']}/RotZ_InBeam deg"
            }
        elif category.lower() == "scatterer2":
            return {
              f"Ge/{kwargs['Name']}/Holder/Rotz":f"Ge/{kwargs['Name']}/RotZForS{kwargs['S2Angle']} deg"
            }
        elif category.lower() == "snout":
            return {
              f"Ge/{kwargs['Name']}/TransZ":f"{kwargs['SnoutTransZ']:.5g} mm",
              f"Ge/{kwargs['Name']}/SNTTypeR1":f"Ge/{kwargs['Name']}/SNT{kwargs['SnoutID']}R1 mm",
              f"Ge/{kwargs['Name']}/SNTTypeR2":f"Ge/{kwargs['Name']}/SNT{kwargs['SnoutID']}R2 mm"
            }
        elif category.lower() == 'aperture':
            return {
              'Ge/Aperture/InputFile':f'"{kwargs["ApertureFile"]}"'
            }
        elif category.lower() == 'compensator':
            return {
              'Ge/Compensator/InputFile':f'"{kwargs["CompensatorFile"]}"'
            }
        elif category.lower() == 'other':
            return {
              'Ge/CheckForOverlaps':'"True"',
              'b:Ge/QuitIfOverlapDetected':'"False"'
            }
        else:
            return False

    def save_nozzle(self, ibeam, g_component):
        def set_value(value, ibeam):
            if str(type(value)) == "<class 'list'>":
                return value[ibeam]
            else:
                return value
        kwargs = {
          'Name':'',
          'nNodes':self.paras['nNodes'], 
          'nSize':len(self.convalgo['BCM'][0]),
          'Stop':f'{self.convalgo["Stop Position"][0]/256*100:.5g}',
          'BCM':'0 0 0 '+' '.join(str(self.convalgo['BCM'][0][i]) for i in range(3,len(self.convalgo['BCM'][0]))), 
          'BWT':' '.join(f'{i:.5g}' for i in self.convalgo['BWT'][0]),
          'S1Number':set_value(self.convalgo['1st Scatterer'][0], ibeam),
          'S2Angle':int(set_value(self.convalgo['2nd Scatterer'][0], ibeam)),
          'SnoutID':self.RTP[ibeam].Snout.ID,
          'SnoutTransZ':-self.RTP[ibeam].Compensator.Isocenter - self.RTP[ibeam].Compensator.MaxThickness - 312.5,
          'PSFile':os.path.join(self.outdir, f'PhaseSpace_beam{ibeam}'),
          'nSequentialTimes':int(set_value(self.convalgo['Stop Position'][0], ibeam)),
          'ApertureFile':os.path.join(self.outdir, self.RTP[ibeam].Aperture.OutName),
          'CompensatorFile':os.path.join(self.outdir, self.RTP[ibeam].Compensator.OutName)
        }
        kwargs['Energy'] = set_value(self.convalgo['Energy'][0], ibeam)
        kwargs['EnergySpread'] = (1.0289 - 0.0008 * (math.log(kwargs['Energy']) - 3.432) / 0.5636) / kwargs['Energy'] * 100
        kwargs['RMTrack'] = int(set_value(self.convalgo['Modulator'][0], ibeam))
        kwargs['RMSmallTrack'] = int((kwargs['RMTrack'] + 2) % 3)
        kwargs['RMSmallWheel'] = int((kwargs['RMTrack'] + 2) / 3)

        dsf = data.Component(btype='scattering')
        record = data.Component(btype='scattering')
        read = data.Component(btype='scattering')

        dsf_keys = ['other', 'control', 'time', 'rangemodulator', 'scatterer1','scatterer2','snout','aperture','compensator']
        record_keys = ['other','control','time','rangemodulator',  'scatterer1', 'scatterer2', 'aperture', 'compensator']
        read_keys = ['control','nigas','world','phase']

        for f in self.imported['DSF'][1]:
            dsf.modify_file(f)
        for f in self.imported['Record'][1]:
            record.modify_file(f)
        for f in self.imported['Read'][1]:
            read.modify_file(f)

        # Dose Scale Factor Calculation
        for key in dsf_keys:
            for component in g_component:
                if key in component.ctype.lower():
                    kwargs['Name'] = component.subcomponent['Basis'].parameters[0].directory
                    continue
            re = self.nozzle_template(category=key, **kwargs)
            if re:
                dsf.modify_parameter(subname='Basis', paras=re)
        dsf.load("Beam/Distribution")
        paras = {
          'd:So/Beam/BeamEnergy':f'{kwargs["Energy"]:.5g} MeV',
          'u:So/Beam/BeamEnergySpread':f'{kwargs["EnergySpread"]:.5g}',
          's:So/Beam/BeamPositionDistribution':'"Gaussian"',
          's:So/Beam/BeamPositionCutoffShape':'"Ellipse"',
          'i:So/Beam/NumberOfHistoriesInRun':'Tf/BeamCurrent/Value * Tf/BeamWeight/Value'
        }
        dsf.modify_parameter(subname='Basis', paras=paras)
        dsf.load("Phantom/WaterPhantom")
        paras = {
          'd:Ge/WaterPhantom/HLX':'10.0 cm',
          'd:Ge/WaterPhantom/HLY':'10.0 cm',
          'd:Ge/WaterPhantom/HLZ':'10.0 cm',
          'd:Ge/WaterPhantom/MaxStepSize':'0.5 mm'
        }
        dsf.modify_parameter(subname='Basis', paras=paras)
        dsf.load("Phantom/PDD")
        paras = {
          'd:Ge/PDD/HLX':'0.5 cm',
          'd:Ge/PDD/HLY':'0.5 cm',
          'd:Ge/PDD/HLZ':'Ge/WaterPhantom/HLZ cm',
          'i:Ge/PDD/XBins':'1',
          'i:Ge/PDD/YBins':'1',
          'i:Ge/PDD/ZBins':'200',
          's:Sc/PDD/OutputFile':f'"{os.path.join(self.outdir, "DSF_beam"+str(ibeam))}"'
        }
        dsf.modify_parameter(subname='Basis', paras=paras)
        dsf.subcomponent['Basis'].draw = True
        for para in dsf.subcomponent['Basis'].parameters:
            para.draw = True
        dsf.name = f'CalculateDoseScaleFactor{ibeam}'

        # Recording Phase Space
        for key in record_keys:
            for component in g_component:
                if component.ctype.lower() == key:
                    kwargs['Name'] = component.subcomponent['Basis'].parameters[0].directory
                    continue
            re = self.nozzle_template(category=key, **kwargs)
            if re:
                record.modify_parameter(subname='Basis', paras=re)
        record.load("Beam/Distribution")
        paras = {
          'd:So/Beam/BeamEnergy':f'{kwargs["Energy"]:.5g} MeV',
          'u:So/Beam/BeamEnergySpread':f'{kwargs["EnergySpread"]:.5g}',
          's:So/Beam/BeamPositionDistribution':'"Gaussian"',
          's:So/Beam/BeamPositionCutoffShape':'"Ellipse"',
          'i:So/Beam/NumberOfHistoriesInRun':'Tf/BeamCurrent/Value * Tf/BeamWeight/Value'
        }
        record.modify_parameter(subname='Basis',paras=paras)
        record.load('PhaseSpace/PhaseSpaceOutput')
        print(record.subcomponent['Basis'].parameters)
        paras = {
          's:Sc/PhaseSpaceOutput/OutputFile':f'"{kwargs["PSFile"]}"'
        }
        record.modify_parameter(subname='Basis',paras=paras)
        record.subcomponent['Basis'].draw = True
        for para in record.subcomponent['Basis'].parameters:
            para.draw = True
        record.name = f'RecordPhaseSpace{ibeam}'
        print(record.subcomponent['Basis'].parameters)

        # Read Phase Space
        for i in range(len(self.RTS.Parallel)):
            if self.RTS.Parallel[i].Include:
                contour = os.path.join(self.outdir, 'contours', 'PatientParallel%i.tps' % i)
                read.modify_file(contour)

        if any(self.firstCT.Manufacturer[0] == i for i in ['G','S']):
            name = 'G'
        else:
            name = self.firstCT.Manufacturer[0]
        print(name)
        manufacturer = os.path.join(self.outdir, 'nozzle', 'HUtoMaterialSchneider_'+str(name)+'.tps')
        read.modify_file(manufacturer)
        for key in read_keys:
            for component in g_component:
                if component.ctype.lower() == key:
                    kwargs['Name'] = component.name
                    continue
            re = self.nozzle_template(category=key, **kwargs)
            if re:
                read.modify_parameter(subname='Basis', paras=re)
        paras = {
          'sv:Ma/NiGas/Components':'1 "Nitrogen"',
          'uv:Ma/NiGas/Fractions':'1 1.0',
          'd:Ma/NiGas/Density':'0.001251 g/cm3',

          's:Ge/World/Material':'"NiGas"',
          'd:Ge/World/HLX':'1.0 m',
          'd:Ge/World/HLY':'1.0 m',
          'd:Ge/World/HLZ':'3.0 m'
        }
        read.modify_parameter(subname='Basis',paras=paras)
        read.load('Phantom/Basis')
        paras = {
          'd:Ge/Phantom/RotY':'-90 deg',
          'd:Ge/Phantom/RotZ':'-45 deg'
        }
        read.modify_parameter(subname='Basis', paras=paras)
        paras = {'s:Ge/Phantom/DicomDirectory':'""'}
        read.modify_parameter(subname='Basis', paras=paras, delete=True)
        read.load('Phantom/Patient')
        paras = {
          'd:Ge/Patient/TransX':'-58.706 mm',
          'd:Ge/Patient/TransY':'-76.114 mm',
          'd:Ge/Patient/TransZ':'8.1396 mm',
          's:Ge/Patient/DicomDirectory':f'"{self.patient.directory}"'
        }
        read.modify_parameter(subname='Basis',paras=paras)
        read.load('Phantom/DoseAtPhantom')
        paras = {
          's:Sc/DoseAtPhantom/OutputFile':f'"{os.path.join(self.outdir, "DoseAtPhantom_beam"+str(ibeam))}"'
        }
        read.modify_parameter(subname='Basis', paras=paras)
        read.load('Physics/Basis')
        read.subcomponent['Basis'].draw = True
        for para in read.subcomponent['Basis'].parameters:
            para.draw = True
        read.name = f'ReadPhaseSpace{ibeam}'

        self.output['DSF'].append(dsf)
        self.output['Record'].append(record)
        self.output['Read'].append(read)

    def save_parallel(self, iparallel):
        out = ""
        parallel = data.Component(btype='scattering')
        parallel.load('Contour/Material')
        material = parallel.subcomponent['Basis'].parameters[0].directory
        parallel.load('Contour/Parallel')
        paras = {
          's:Ge/PatientParallel/Material':material,
          'd:Ge/PatientParallel/TransX':f'{self.RTS.TargetPosition[0]:.5g}',
          'd:Ge/PatientParallel/TransY':f'{self.RTS.TargetPosition[1]:.5g}',
          'd:Ge/PatientParallel/TransZ':f'{self.RTS.TargetPosition[2]:.5g}'
        }
        parallel.modify_parameter(subname='Basis',paras=paras)
        for para in parallel.subcomponent['Basis'].parameters:
            name = para.fullname()
            parallel.modify_paraname('Basis', name, name.replace('PatientParallel', f'PatientParallel{iparallel}'))
        parallel.name = f'PatientParallel{iparallel}'

        out += '\n'.join(f'{para.fullname()} = {para.value}' for para in parallel.subcomponent['Basis'].parameters)
        for contour in self.RTS.Parallel[iparallel].Contour:
            idx = np.arange(0, contour.Size*3, 3) + 2
            z = contour.Polygons[2]
            polygons = np.delete(np.array(contour.Polygons), idx)
            polygons = ' '.join(f'{i:.5g}' for i in contour.Polygons) + ' mm'
            paras = {
              f's:Ge/Contour{contour.Index}/Parent':'"Patient"',
              f's:Ge/Contour{contour.Index}/Type':'"G4ExtrudedSolid"',
              f's:Ge/Contour{contour.Index}/Material':material,
              f'd:Ge/Contour{contour.Index}/HLZ':f'{self.firstCT.Thickness/2.0:.5g}',
              f'd:Ge/Contour{contour.Index}/TransX':'0.0 mm',
              f'd:Ge/Contour{contour.Index}/TransZ':f'{z - self.CTcenter:.5g}',
              f'dv:Ge/Contour{contour.Index}/Off1':'2 0 0 mm',
              f'dv:Ge/Contour{contour.Index}/Off2':'2 0 0 mm',
              f'u:Ge/Contour{contour.Index}/Scale1':'1.0',
              f'u:Ge/Contour{contour.Index}/Scale2':'1.0',
              f'dv:Ge/Contour{contour.Index}/Polygons':f'{contour.Size} {polygons}',
              f's:Ge/Contour{contour.Index}/ParallelWorldName':parallel.name,
              f'b:Ge/Contour{contour.Index}/IsParallel':"True"
            }
            out += '\n'.join(f'{key} = {value}' for key, value in paras.items())
        
        return (parallel.name+'.tps', out)