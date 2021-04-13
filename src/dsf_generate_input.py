import os, sys, stat
from dataclasses import dataclass, field
from datetime import datetime
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pydicom as dicom

import src.utils as ut
import src.abclass as abcls
import src.getconvalgo as convalgo

class GenerateDSFInput(abcls.GenerateInput):
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

    def __init__(self, para):
        self.base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        sys.path.append(self.base_path)
        
        self.outdir = os.path.join(self.base_path, 'prod', datetime.today().strftime('%Y%m%d'))
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)
        if not os.path.exists(os.path.join(self.outdir, 'contours')):
            os.makedirs(os.path.join(self.outdir, 'contours'))

        self.para = para
        self.para['DicomDirectory'] = os.path.join(self.base_path, 'data', self.para['DicomDirectory'])
        
        empty_parameters = []
        for key, value in self.para.items():
            if value is None: empty_parameters.append(key)
        if len(empty_parameters) > 0:
            print("Please, fill the empty parameter:", empty_parameters)
            exit(0)
        
        self.conv = convalgo.GetParaFromConvAlgo(os.path.join(self.base_path,'data'), self.para['ConvAlgo'])
                
        tmp = []
        for i in os.listdir(self.para['DicomDirectory']):
            if not i.endswith('.dcm'): continue
            if i.startswith('RN'):
                self.RTP = i
            elif i.startswith('RS'):
                self.RTS = i
            elif i.startswith('RD'):
                continue
            else:
                tmp.append(i)

        files = pd.Series(tmp)
        numbers = files.str.split('.').apply(lambda x: pd.Series(x))
        criteria = -1
        for i in range(len(numbers.columns)):
            if i == 0 or i == len(numbers.columns)-1: continue
            if numbers[i][1] == numbers[i][2]: continue
            else:
                criteria = i

        df = pd.DataFrame({'name':files, 'number':numbers[criteria]})
        df = df.astype({'number':'int64'})
        self.firstCT = df['name'][df[df['name'].str.contains('CT')]['number'].idxmin()]
        self.lastCT = df['name'][df[df['name'].str.contains('CT')]['number'].idxmax()]
        self.imageZ = df['name'][df['name'].str.contains('CT')].size
        
        print("First CT:", self.firstCT)
        print("Last CT:", self.lastCT)
        print("RT Plan:", self.RTP)
        print("RT Structure:", self.RTS)

        del [[df]]

        self.geometry = []
        self.snout = []
        self.aperture = []
        self.compensator = []
        self.parallel = []

    def set_parameters(self):
        imageZ = self.imageZ
        firstCT = dicom.dcmread(os.path.join(self.para['DicomDirectory'], self.firstCT))
        lastCT = dicom.dcmread(os.path.join(self.para['DicomDirectory'], self.lastCT))
        RTP = dicom.dcmread(os.path.join(self.para['DicomDirectory'], self.RTP))
        RTS = dicom.dcmread(os.path.join(self.para['DicomDirectory'], self.RTS))

        # Computed Tomography(CT)
        firstCT_pos = firstCT.ImagePositionPatient
        lastCT_pos = lastCT.ImagePositionPatient
        instance = firstCT.InstanceNumber

        img_thick = firstCT.SliceThickness
        if img_thick is None:
            img_thick = 0.0
        
        img_row = firstCT.Rows
        img_col = firstCT.Columns
        img_pixel = firstCT.PixelSpacing
                
        if lastCT_pos[-1] < firstCT_pos[-1]:
            firstCT_z = firstCT_pos[2] + (instance - 1) * img_thick
            lastCT_z = firstCT_pos[2] - (imageZ - instance) * img_thick
        else:
            lastCT_z = firstCT_pos[2] - (instance - 1) * img_thick
            firstCT_z = firstCT_pos[2] - (imageZ - instance) * img_thick

        CT_center = (firstCT_z + lastCT_z) / 2.0
       
        print("===== CT information =====")
        print("Instance Number(Z):", instance)
        print("Image (row, column): (%d, %d)"% (img_row, img_col))
        print("Pixel Spacing:", img_pixel)
        print("SliceThickness:", img_thick)
        print("Manufacturer:", firstCT.Manufacturer)
        print("imageZ:", imageZ)
        print("First CT positions:", firstCT_pos)
        print("Last CT Z position:", lastCT_pos[-1])
        print("Reorganized Z position of first CT:", firstCT_z)
        print("Reorganized Z position of last CT:", lastCT_z)
        print("Center of CT:", CT_center)
        print("==========================")
        
        # Radio Therapy Plan(RTP)
        nbeam = RTP.FractionGroupSequence[0].NumberOfBeams
        print("===== RTP information =====")
        print("Number of beam sequences:", nbeam)
        
        SAD_data = float(self.para['virtualSID'])*10

        for ibeam in range(nbeam):
            print("--------- %i beam ---------" % ibeam)
            sequence = RTP.IonBeamSequence[ibeam]

            ### Compensator
            compen_dir = sequence.IonRangeCompensatorSequence[0]
            compen_iso = compen_dir.IsocenterToCompensatorTrayDistance
            compen_thick = compen_dir.CompensatorThicknessData
            compen_mill = compen_dir.CompensatorMillingToolDiameter
            compen_pos = compen_dir.CompensatorPosition
            compen_pixel = compen_dir.CompensatorPixelSpacing
            compen_rows = compen_dir.CompensatorRows
            compen_cols = compen_dir.CompensatorColumns
            
            compen_thick = compen_dir.CompensatorThicknessData
            compen_thick = np.array(compen_thick)
            compen_thick = np.reshape(compen_thick, (compen_rows, compen_cols))
            compen_maxthick = np.amax(compen_thick)
            
            ### Snout
            snout_id = sequence.SnoutSequence[0].SnoutID.replace(' ','').replace('Snout','')
            snout_pos = sequence.IonControlPointSequence[0].SnoutPosition

            # Gantry angle
            gantry_angle = sequence.IonControlPointSequence[0].GantryAngle

            # Isocenter
            isocenter = sequence.IonControlPointSequence[0].IsocenterPosition
            # Cumulative meterset weight
            meterset = sequence.IonControlPointSequence[0].CumulativeMetersetWeight
            
            # Source to isocenter distance
            source_to_isocenter_dist = sequence.VirtualSourceAxisDistances
 
            # Aperture
            aperture_dir = sequence.IonBlockSequence[0]
            aper_thick = aperture_dir.BlockThickness
            aper_data = aperture_dir.BlockData
            aper_ibd = aperture_dir.IsocenterToBlockTrayDistance
            naper = aperture_dir.BlockNumberOfPoints           
            
            self.geometry.append(self.Geometry(
              gantry_angle = gantry_angle,
              isocenter = isocenter, manufacturer = firstCT.Manufacturer 
            ))
            
            self.snout.append(self.Snout(id = snout_id, position = snout_pos))

            print("Isocenter to compensator tray distance:", compen_iso)
            print("Number of compensator thickness data:", len(compen_thick))
            print("Compensator (row, col): (", compen_rows, ",", compen_cols, ")")
            print("Maximum thickness of compensator:", compen_maxthick)
            print("Compensator milling thickness:", compen_mill)
            print("Compensator position:", compen_pos)
            print("Compensator pixel spacing:", compen_pixel)
            print("Snout ID:", snout_id)
            print("Snout Position:", snout_pos)
            print("Gantry angle:", gantry_angle)
            print("Isocenter:(%f, %f, %f)" % (isocenter[0], isocenter[1], isocenter[2]))
            print("Source to Isocenter distance:", source_to_isocenter_dist)
            print("Meterset:", meterset)
            print("Number of apperture data:", naper)
            print("Apperture thickness:", aper_thick)
            print("Isocenter to block tray distance:", aper_ibd)

            ps = (SAD_data - compen_iso) / SAD_data
            compen_ps = [ps, ps]

            tmp_rows = [0,0]
            for i in range(compen_cols):
                for j in range(compen_rows):
                    if compen_thick[j][i] != compen_maxthick:
                        tmp_rows[0] = i+1
                        break
                if tmp_rows[0] != 0:
                    break
            for i in range(compen_cols-1,0,-1):
                for j in range(compen_rows-1, 0, -1):
                    if compen_thick[j][i] != compen_maxthick:
                        tmp_rows[1] = i
                        break
                if tmp_rows[1] != 0:
                    break

            tmp_cols1 = [0 for i in range(0,compen_cols)]
            tmp_cols2 = [0 for i in range(0,compen_cols)]
            row, col = np.where(compen_thick[:compen_rows, (tmp_rows[0]-1):(tmp_rows[1]+1)] != compen_maxthick)
            uni, cnt = np.unique(col, return_counts = True)
            for i in range(len(cnt)):
                tmp_cols1[i] = cnt[i]
            for i in range(tmp_rows[0]-1,tmp_rows[1]+1):
                for j in range(0,compen_rows):
                    if compen_thick[j][i] != compen_maxthick:
                        tmp_cols2[i] = j
                        break
        
            x_pos = []
            y_pos = []
            relthi = []
            tmp_cols = []

            for i in range(tmp_rows[0]-1, tmp_rows[1]+1):
                x_pos.append((-compen_pos[0] - (i * compen_pixel[0])) * compen_ps[0])
                y_pos.append((compen_pos[1] - (tmp_cols2[i] * compen_pixel[1])) * compen_ps[1])
                tmp = []
                for j in range(tmp_cols2[i], tmp_cols2[i]+tmp_cols1[i-(tmp_rows[0]-1)]):
                    tmp.append(compen_maxthick - compen_thick[j][i])
                relthi.append(tmp)
                tmp_cols.append((tmp_cols1[i], tmp_cols2[i], tmp_cols2[i] + tmp_cols1[i-(tmp_rows[0]-1)]))

            self.compensator.append(self.Compensator(
              isocenter = compen_iso,
              milling = compen_mill, max_thickness = compen_maxthick, rel_thickness = relthi,
              x = x_pos, y = y_pos, rows = tmp_rows, cols = tmp_cols, pixel = compen_pixel, ps = compen_ps 
            ))

            airgap = 1 - (aper_ibd - aper_thick) / SAD_data

            self.aperture.append(self.Aperture(
              aper_num = naper, 
              thickness = aper_thick, iso_dist = aper_ibd, airgap = airgap, data = aper_data
            ))
       
            target_pos = [
              (2 * firstCT_pos[0] + (img_row - 1)*img_pixel[0])/2 - isocenter[0], # x
              (2 * firstCT_pos[1] + (img_col - 1)*img_pixel[1])/2 - isocenter[1], # y
              CT_center - isocenter[2], # z
            ]
            print("--------------------------")
        
        print("===========================")
        print("===== RTP information =====")

        # Radio Therapy Structure(RTS)
        # ROI: Region of Interset
        # parallel_num target_pos number density size thickness polygons
        
        nparallel = len(RTS.ROIContourSequence)
        ncontour = len(RTS.ROIContourSequence[0].ContourSequence)
        print("Number of parallel:", nparallel)
        for iparallel in range(len(RTS.ROIContourSequence)):
            print("------- %i parallel -------" % iparallel)
            sequence = RTS.ROIContourSequence[iparallel]
            observation = RTS.RTROIObservationsSequence[iparallel]
            try:
                print("Number of contour:",len(sequence.ContourSequence))
            except:
                continue
            
            try:
                density = float(observation.ROIPhysicalPropertiesSequence[0].ROIPhysicalPropertyValue)
                include = True
            except:
                density = 0.0
                include = False

            idx = 0
            contour = []
            for icontour in range(len(sequence.ContourSequence)):
                contour_seq = sequence.ContourSequence[icontour]
                contour.append(self.Contour(
                  contour_num = icontour,
                  size = contour_seq.NumberOfContourPoints,
                  polygons = contour_seq.ContourData
                ))

            self.parallel.append(self.Parallel(
              parallel_num = iparallel,
              include = include,
              target_pos = target_pos,
              iso_z = self.geometry[0].isocenter[2],
              ct_center = CT_center,
              density = density,
              img_thickness = img_thick,
              contour = contour
            ))

            print("--------------------------")
        
        print("===========================")

    def write_scripts(self):
        import templates.dsf as dsf
        import templates.record as record
        import templates.read as read
        import templates.components.materials as ma
        import templates.components.geometry as ge
       
        tps = ['calculateDSF_beam%i.tps', 'recordPhaseSpace_beam%i.tps', 'readPhaseSpace_beam%i.tps']
        for ibeam in range(len(self.compensator)):
            compen_name = os.path.join(self.outdir,'CompensatorFileInRowsDepths%d.rc' % ibeam)
            f_compensator = open(compen_name, 'w')
            out_template = """{rows}\n{maxcom}\n{milling}\n{value}\n0 0"""
        
            row_min = self.compensator[ibeam].rows[0]
            row_max = self.compensator[ibeam].rows[1]
            cols = self.compensator[ibeam].cols
            pixel = self.compensator[ibeam].pixel
            ps = self.compensator[ibeam].ps
            x = self.compensator[ibeam].x
            y = self.compensator[ibeam].y
            relthi = self.compensator[ibeam].rel_thickness

            value = ''
            for i in range(len(x)):
                str_pos = f'{cols[i][0]:.5g} {(-pixel[0]*ps[0]):.5g} {y[i]:.5g} {x[i]:.5g}\n'
                str_relthi = ''
                for item in relthi[i]:
                    str_relthi += f'{item:.5g} ' 
                value += str_pos + str_relthi + '\n'
            f_compensator.write(out_template.format(
              rows = (row_max - row_min + 2),
              maxcom = f'{self.compensator[ibeam].max_thickness:.5g}',
              milling = f'{self.compensator[ibeam].milling:.5g}', value = value))
            f_compensator.close()

            aper_name = os.path.join(self.outdir, 'ApertureFileIn%d.ap' % ibeam)
            f_aperture = open(aper_name, 'w')
            airgap = self.aperture[ibeam].airgap
            data = self.aperture[ibeam].data
            out_str = str(self.aperture[ibeam].aper_num) + '\n'
            for i in range(0, self.aperture[ibeam].aper_num):
                out_str += f'{-data[2*i]*airgap:.5g}, {data[2*i+1]*airgap:.5g}\n'
            f_aperture.write(out_str)
            f_aperture.close()

            path = os.path.join(self.base_path, 'data', 'components')
            if not path.endswith('/'):
                path += '/'
            time = ' '.join(f'{i:.5g}' for i in self.conv.time)
            bcm = '0 0 0 '+' '.join(str(self.conv.bcm[i]) for i in range(3,len(self.conv.bcm)))
 
            energy = float(self.conv.energy)
            spread = (1.0289 - 0.0008 * (math.log(energy) - 3.432) / 0.5636) / energy * 100
            rm_data = float(self.conv.modulator)
            lollipop = ge.scatterer1.format(S1Number = int(self.conv.fscatterer[ibeam])) + "\n"
           
            transz = -self.compensator[ibeam].isocenter - self.compensator[ibeam].max_thickness - 312.5 
           
            fout = open(os.path.join(self.outdir, tps[0] % ibeam), 'w')
            
            template = dsf.template.format(
              path = path,
              nNodes = self.para['nNodes'], 
              stop = f'{self.conv.stop/256*100:.5g}', nSequentialTimes = int(self.conv.stop), 
              nHistory = self.para['nHistory'],
              BCM = bcm, BWT = time,
              RM_data = int(self.conv.modulator), 
              RM_track = int((self.conv.modulator + 2) / 3),
              RM_track_re = int((self.conv.modulator + 2) % 3),
              Energy = f'{energy:.5g}', EnergySpread = f'{spread:.5g}',
              Scatterer1= lollipop, S2Angle = int(self.conv.sscatterer),
              TransZ = f'{transz:.5g}', SnoutID = self.snout[ibeam].id,
              ApertureFile = aper_name,
              output = os.path.join(self.outdir, 'DSF_beam'+str(ibeam)), outType = 'csv' 
            )
            
            fout.write(template)
            fout.close()

            fout = open(os.path.join(self.outdir, tps[1] % ibeam), 'w')
            phase_out = os.path.join(self.outdir, 'Phase_beam'+str(ibeam))
            
            template = record.template.format(
              path = path,
              nNodes = self.para['nNodes'],
              stop = f'{self.conv.stop/256*100:.5g}', nSequentialTimes = int(self.conv.stop), 
              nHistory = self.para['nHistory'],
              BCM = bcm, BWT = time,
              RM_data = int(self.conv.modulator), 
              RM_track = int((self.conv.modulator + 2) / 3),
              RM_track_re = int((self.conv.modulator + 2) % 3),
              Energy = f'{energy:.5g}', EnergySpread = f'{spread:.5g}',
              Scatterer1= lollipop, S2Angle = int(self.conv.sscatterer),
              TransZ = f'{transz:.5g}', SnoutID = self.snout[ibeam].id,
              ApertureFile = aper_name, CompensatorFile = compen_name,
              output = phase_out
            )
            
            fout.write(template)
            fout.close()

            fout = open(os.path.join(self.outdir, tps[2] % ibeam), 'w')
           
            for i in range(len(self.parallel)):
                if self.parallel[i].include:
                    contour = os.path.join(self.outdir, 'contours', 'contour_parallel%i.tps' % i)
                    fout.write("includeFile = " + contour + "\n")

            template = read.template.format(
              path = path,
              manu = self.geometry[ibeam].manufacturer[0],
              nNodes = self.para['nNodes'],
              PSFile = phase_out, PSMulti = self.para['PhaseReuse'],
              RotZ = f'{-90.0 + self.geometry[ibeam].gantry_angle:.5g}',
              TransX = f'{self.parallel[0].target_pos[0]:.5g}',
              TransY = f'{self.parallel[0].target_pos[1]:.5g}',
              TransZ = f'{self.parallel[0].target_pos[2]:.5g}',
              DicomDirectory = self.para['DicomDirectory'],
              output = os.path.join(self.outdir, "doseAtPhantom_beam%i" % ibeam),
              Scale = self.para['DoseScalingF']
            )
            fout.write(template)
            fout.close()
        
        for iparallel in self.parallel:
            fout = open(os.path.join(
              self.outdir, 'contours', 'contour_parallel%i.tps' % iparallel.parallel_num), 'w')
            
            material = ma.contour.format(
              Number = iparallel.parallel_num,
              Density = f'{iparallel.density:.5g}'
            )
            
            parallel = ge.parallel_patients.format(
              Number = iparallel.parallel_num,
              TransX = f'{iparallel.target_pos[0]:.5g}',
              TransY = f'{iparallel.target_pos[1]:.5g}',
              TransZ = f'{-iparallel.iso_z:.5g}'
            )

            fout.write(material + "\n" + parallel + "\n")
            for icontour in iparallel.contour:
                idx = np.arange(0, icontour.size*3, 3) + 2
                z = icontour.polygons[2]
                polygons = np.delete(np.array(icontour.polygons), idx)
                polygons = ' '.join(f'{i:.5g}' for i in polygons) + ' mm'
                contour = ge.contour.format(
                  ContourNumber = icontour.contour_num,
                  ParallelNumber = iparallel.parallel_num,
                  HLZ = f'{iparallel.img_thickness/2.0:.5g}',
                  TransZ = f'{z - iparallel.ct_center:.5g}',
                  Size = icontour.size*2,
                  Polygons = polygons
                )
                fout.write(contour + "\n")

            fout.close()

        script = os.path.join(self.outdir, 'script.sh')
        f = open(script, 'w')
        for para in tps:
            text = ''
            for ibeam in range(len(self.compensator)):
                text += f'topas {self.outdir}/' + tps[0] % ibeam +'\n'
            f.write(text+'\n')
        st = os.stat(script)
        os.chmod(script, st.st_mode | stat.S_IEXEC)
        f.close()

        return script 
