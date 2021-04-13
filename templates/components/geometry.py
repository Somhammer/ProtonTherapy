# Geometry Components

import src.utils as ut

# Parameters
geometry_parameters = [
"""s:Ge/%(name)s/Parent = "%(Parent)s"\n""",
"""s:Ge/%(name)s/Type = "%(Type)s"\n""",
"""s:Ge/%(name)s/Material = "%(Material)s"\n""",
"""d:Ge/%(name)s/HLX = %(HLX)s\n""",
"""d:Ge/%(name)s/HLY = %(HLY)s\n""",
"""d:Ge/%(name)s/HLZ = %(HLZ)s\n""",
"""d:Ge/%(name)s/TransX = %(TransX)s\n""",
"""d:Ge/%(name)s/TransY = %(TransY)s\n""",
"""d:Ge/%(name)s/TransZ = %(TransZ)s\n""",
"""d:Ge/%(name)s/RotX = %(RotX)s\n""",
"""d:Ge/%(name)s/RotY = %(RotY)s\n""",
"""d:Ge/%(name)s/RotZ = %(RotZ)s\n""",
"""dv:Ge/%(name)s/Off1 = %(nOff1)i %(Off1)s\n""",
"""dv:Ge/%(name)s/Off2 = %(nOff2)i %(Off2)s\n""",
"""u:Ge/%(name)s/Scale1 = %(Scale1)f\n""",
"""u:Ge/%(name)s/Scale2 = %(Scale2)f\n""",
"""s:Ge/%(name)s/ParallelWorldName = "%(ParaName)s"\n""",
"""b:Ge/%(name)s/IsParallel = "%(IsParallel)s"\n""",
# For specialized components
"""s:Ge/%(name)s/InputFile = "%(InputFile)s"\n""",
"""s:Ge/%(name)s/FileFormat = "%(Format)s"\n""",
"""d:Ge/%(name)s/Units = "%(Units)s"\n""",
"""b:Ge/%(name)s/PrintPoints = "%(PrintPoints)s"\n""",
"""s:Ge/%(name)s/Method = "%(Method)s"\n""",
]

world_variables = {
  "name":"World", "Material":"NiGas",
  "HLX":"1.0 m", "HLY":"1.0 m", "HLZ":"3.0 m"
}
world = ut.make_component(geometry_parameters, world_variables)

# Beam
### Range Modulator Wheel
rmw = """\
d:Ge/RMW/Track/zero_angle = Ge/RMW/Track{RM_data} - Ge/RMW/Small/Track{RM_track_re} deg
Ge/RMW_{RM_track}/RotZ = Tf/RMW_Rotation/Value deg
Ge/RMW/Track = -1 * Ge/RMW/Track{RM_data} deg
"""

### Scatterer
scatterer1 = "Ge/Scatterer1/Lollipop{S1Number} = Ge/Scatterer1/RotZ_InBeam deg"
scatterer2 = "Ge/Scatterer2/Holder/Rotz = Ge/Scatterer2/RotZForS{S2Angle} deg"

### Collimater

### Snout 
snout = """\
Ge/Snout/TransZ = {TransZ} mm
Ge/Snout/SNTTypeR1 = Ge/Snout/SNT{SnoutID}R1 mm
Ge/Snout/SNTTypeR2 = Ge/Snout/SNT{SnoutID}R2 mm\n\
"""

# Patient
### Aperture
aperture = """\
Ge/Aperture/InputFile = "{ApertureFile}"\
"""
### Compensator

### Phantom
##### Single
water_phantom_variables = {
  "name":"WaterPhantom",
  "Parent":"Gantry", "Type":"TsBox", "Material":"G4_WATER", 
  "HLX":"10.0 cm", "HLY":"10.0 cm", "HLZ":"10.0 cm",
  "TransX":"0.0 cm", "TransY":"0.0 cm", "TransZ":"0.0 cm",
  "RotX":"0.0 deg", "RotY":"0.0 deg", "RotZ":"0.0 deg",
}

water_phantom = ut.make_component(geometry_parameters, water_phantom_variables) + """\
d:Ge/WaterPhantom/MaxStepSize = 0.5 mm
"""

pdd_variables = {
  "name":"PDD",
  "Parent":"WaterPhantom", "Type":"TsBox", "Material":"G4_WATER",
  "HLX":"0.5 cm", "HLY":"0.5 cm", "HLZ":"Ge/WaterPhantom/HLZ cm",
  "TransX":"0.0 cm", "TransY":"0.0 cm", "TransZ":"0.0 cm",
  "RotX":"0.0 deg", "RotY":"0.0 deg", "RotZ":"0.0 deg",
}

pdd = ut.make_component(geometry_parameters, pdd_variables) + """\
i:Ge/PDD/XBins = 1
i:Ge/PDD/YBins = 1
i:Ge/PDD/ZBins = 200
"""
box_variables = {
  "name":"PhantomBox",
  "Type":"Group", "Material":"G4_WATER",
  "TransX":"0 mm", "TransY":"0 mm", "TransZ":"0 mm",
  "RotX":"0 deg", "RotY":"-90 deg", "RotZ":"{RotZ} deg"
}

box = ut.make_component(geometry_parameters, box_variables)

patient_variables = {
  "name":"Patient",
  "Type":"TsDicomPatient", "Parent":"PhantomBox", "Material":"G4_WATER",
  "TransX":"{TransX} mm", "TransY":"{TransY} mm", "TransZ":"{TransZ} mm",
  "RotX":"0 deg", "RotY":"0 deg", "RotZ":"0 deg"
}

patient = ut.make_component(geometry_parameters, patient_variables) + """\
s:Ge/Patient/DicomDirectory = "{DicomDirectory}"
"""

##### Parallel
parallel_patients_variables = {
        "name":"PatientParallel{Number}", "Parent":"PhantomBox", 
  "Type":"Group", "Material":"Contour{Number}",
  "TransX":"{TransX} mm", "TransY":"{TransY} mm", "TransZ":"{TransZ} mm",
  "ParaName":"PatientParallel{Number}", "IsParallel":"True",
}

parallel_patients = ut.make_component(geometry_parameters, parallel_patients_variables)

### Contour
contour_variables = {
  "name":"Contour{ContourNumber}",
  "Type":"G4ExtrudedSolid", "Parent":"Patient", "Material":"Contour{ParallelNumber}",
  "HLZ":"{HLZ} mm", "TransX":"0 mm", "TRansY":"0 mm", "TransZ":"{TransZ} mm",
  "ParaName":"PatientParallel{ParallelNumber}", "IsParallel":"True",
  "nOff1":2, "Off1":"0 0 mm", "nOff2":2, "Off2":"0 0 mm",
  "Scale1":1, "Scale2":1
}

contour = ut.make_component(geometry_parameters, contour_variables) + """\
dv:Ge/Contour{ContourNumber}/Polygons = {Size} {Polygons}
"""
