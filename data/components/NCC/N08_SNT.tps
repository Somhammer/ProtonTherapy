includeFile = /home/seohyeon/work/ProtonTherapy/data/components/NCC/ConstantsForNozzles.tps
#Snout:
##################################################
s:Ge/Snout/Type = "Group"
s:Ge/Snout/Parent = "World"
d:Ge/Snout/TransX = 0. m
d:Ge/Snout/TransY = 0. m
d:Ge/Snout/TransZ = 50. cm
d:Ge/Snout/RotX = 0. deg
d:Ge/Snout/RotY = 0. deg
d:Ge/Snout/RotZ = 0. deg
s:Ge/Snout/Message = "ConstructingSnout"

d:Ge/Snout/SNT100R1 = 55 mm
d:Ge/Snout/SNT180R1 = 90 mm
d:Ge/Snout/SNT250R1 = 135 mm
d:Ge/Snout/SNT100R2 = 90 mm
d:Ge/Snout/SNT180R2 = 125 mm
d:Ge/Snout/SNT250R2 = 160 mm

d:Ge/Snout/SNTTypeR1 = Ge/Snout/SNT100R1 mm
d:Ge/Snout/SNTTypeR2 = Ge/Snout/SNT100R2 mm

#Snout:
s:Ge/Snout/Block/Parent = "Snout"
s:Ge/Snout/Block/Type = "TsBox"
s:Ge/Snout/Block/Material = "Brass"
d:Ge/Snout/Block/HLX = 20.0 cm
d:Ge/Snout/Block/HLY = 20.0 cm
d:Ge/Snout/Block/HLZ = 3.25 cm
d:Ge/Snout/Block/TransX = 0. cm
d:Ge/Snout/Block/TransY = 0. cm
d:Ge/Snout/Block/TransZ = 0. cm
d:Ge/Snout/Block/RotX = 0. deg
d:Ge/Snout/Block/RotY = 0. deg
d:Ge/Snout/Block/RotZ = 0. deg
s:Ge/Snout/Block/DrawingStyle = "Solid"
d:Ge/Snout/Block/LowerEdge = Ge/Snout/Block/HLZ cm

#Snout:HoleinBrassBlock
s:Ge/Snout/Hole/Parent = "Snout/Block"
s:Ge/Snout/Hole/Type = "TsCylinder"
s:Ge/Snout/Hole/Material = "NiGas"
d:Ge/Snout/Hole/RMin = 0.0 cm
d:Ge/Snout/Hole/RMax = Ge/Snout/SNTTypeR1 mm
#d:Ge/Snout/Hole/HL = 6.75 cm
d:Ge/Snout/Hole/HL = 3.25 cm
d:Ge/Snout/Hole/TransX = 0.0 cm
d:Ge/Snout/Hole/TransY = 0.0 cm
d:Ge/Snout/Hole/TransZ = 0.0 cm
d:Ge/Snout/Hole/RotX = 0.0 deg
d:Ge/Snout/Hole/RotY = 0.0 deg
d:Ge/Snout/Hole/RotZ = 0.0 deg
d:Ge/Snout/Hole/SPhi = 0.0 deg
d:Ge/Snout/Hole/DPhi = 360.0 deg
s:Ge/Snout/Hole/DrawingStyle = "Solid"

#Snout:BrassCone
s:Ge/Snout/BrassCone/Parent = "Snout"
s:Ge/Snout/BrassCone/Type = "TsCylinder"
s:Ge/Snout/BrassCone/Material = "Brass"
#d:Ge/Snout/BrassCone/RMin = 5.5 cm
d:Ge/Snout/BrassCone/RMin = Ge/Snout/SNTTypeR1 mm
d:Ge/Snout/BrassCone/RMax = Ge/Snout/SNTTypeR2 mm
d:Ge/Snout/BrassCone/HL = 12.0 cm
d:Ge/Snout/BrassCone/TransX = 0.0 cm
d:Ge/Snout/BrassCone/TransY = 0.0 cm
d:Ge/Snout/BrassCone/TransZ = Ge/Snout/Block/LowerEdge + Ge/Snout/BrassCone/HL cm
d:Ge/Snout/BrassCone/RotX = 0.0 deg
d:Ge/Snout/BrassCone/RotY = 0.0 deg
d:Ge/Snout/BrassCone/RotZ = 0.0 deg
d:Ge/Snout/BrassCone/SPhi = 0.0 deg
d:Ge/Snout/BrassCone/DPhi = 360.0 deg
s:Ge/Snout/BrassCone/DrawingStyle = "Solid"
d:Ge/Snout/BrassCone/LowerEdge = Ge/Snout/BrassCone/TransZ + Ge/Snout/BrassCone/HL cm

##################################################
#Aperture
##################################################
s:Ge/Aperture/Type = "TsAperture"
s:Ge/Aperture/Parent = "Snout"
s:Ge/Aperture/InputFile = "ApertureFileIn.ap"
s:Ge/Aperture/FileFor mat = "XYCoordinates"
b:Ge/Aperture/PrintPoints = "True"
s:Ge/Aperture/Material = "Brass"
d:Ge/Aperture/RMax = 20.0 cm
d:Ge/Aperture/HL = 2.0 cm
d:Ge/Aperture/TransX = 0.0 cm
d:Ge/Aperture/TransY = 0.0 cm
d:Ge/Aperture/TransZ = Ge/Snout/BrassCone/LowerEdge + Ge/Aperture/HL cm
d:Ge/Aperture/RotX = 0.0 deg
d:Ge/Aperture/RotY = 0.0 deg
d:Ge/Aperture/RotZ = 90.0 deg
d:Ge/Aperture/LowerEdge = Ge/Aperture/TransZ + Ge/Aperture/HL cm
s:Ge/Aperture/Message = "ConstructingAperture"
b:Ge/Aperture/Invisible = "True"
#b:Ge/Aperture/IsParallel = "True"

##################################################
#Compensator
##################################################
s:Ge/Compensator/Type = "TsCompensator"
s:Ge/Compensator/Parent = "Snout"
s:Ge/Compensator/Material = "CompensatorLucite"
d:Ge/Compensator/RMax = 20 cm
d:Ge/Compensator/TransX = 0. cm
d:Ge/Compensator/TransY = 0. mm
dc:Ge/Compensator/Thickness = 0. cm #will be reset to actual thickness when compensator is read in
d:Ge/Compensator/HL = 0.5 * Ge/Compensator/Thickness cm
d:Ge/Compensator/TransZ = Ge/Aperture/LowerEdge + Ge/Compensator/HL cm
d:Ge/Compensator/LowerEdge = Ge/Compensator/TransZ + Ge/Compensator/HL cm
d:Ge/Compensator/RotX = 0. deg
d:Ge/Compensator/RotY = 0. deg
d:Ge/Compensator/RotZ = 90. deg
s:Ge/Compensator/InputFile = "CompensatorFileInRowsDepths.rc"
s:Ge/Compensator/FileFormat = "RowsAndDepths"
s:Ge/Compensator/Method = "ExtrudedSolid"#Polyhedra,ExtrudedSolid,SubtractionCylindersorUnionCylinders
#d:Ge/Compensator/XTolerance = 10.mm
#d:Ge/Compensator/YTolerance = 10.mm
b:Ge/Compensator/PrintPoints = "F"
#s:Ge/Compensator/Message = "ConstructingCompensator"
#b:Ge/Compensator/IsParallel = "True"
#s:Ge/Compensator/DrawingStyle = "Solid"

#########################
#Phasespacevolu me
#########################
s:Ge/ZPhaseSpaceVol/Type = "TsBox"
s:Ge/ZPhaseSpaceVol/Parent = "Snout"
s:Ge/ZPhaseSpaceVol/Material = "Parent"
d:Ge/ZPhaseSpaceVol/HLX = 20. cm
d:Ge/ZPhaseSpaceVol/HLY = 20. cm
d:Ge/ZPhaseSpaceVol/HLZ = 0.05 mm
d:Ge/ZPhaseSpaceVol/TransX = 0. m
d:Ge/ZPhaseSpaceVol/TransY = 0. m
d:Ge/ZPhaseSpaceVol/TransZ = 0.025 + Ge/Compensator/LowerEdge cm
#d:Ge/ZPhaseSpaceVol/TransZ = 20 cm
d:Ge/ZPhaseSpaceVol/RotX = 0. deg
d:Ge/ZPhaseSpaceVol/RotY = 0. deg
d:Ge/ZPhaseSpaceVol/RotZ = 0. deg
