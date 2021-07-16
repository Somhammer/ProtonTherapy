includeFile = /home/seohyeon/work/ProtonTherapy/data/components/NCC/ConstantsForNozzles.tps

##################################################
#Snout
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

##################################################
#HoleinBrassBlock
##################################################

s:Ge/Snout/Hole/Parent = "Snout/Block"
s:Ge/Snout/Hole/Type = "TsCylinder"
s:Ge/Snout/Hole/Material = "Air"
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

##################################################
#Snout:BrassCone
##################################################
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
s:Ge/Snout/Aperture/Type = "TsAperture"
s:Ge/Snout/Aperture/Parent = "Snout"
s:Ge/Snout/Aperture/InputFile = "ApertureFileIn.ap"
s:Ge/Snout/Aperture/FileFormat = "XYCoordinates"
b:Ge/Snout/Aperture/PrintPoints = "True"
s:Ge/Snout/Aperture/Material = "Brass"
d:Ge/Snout/Aperture/RMax = 20.0 cm
d:Ge/Snout/Aperture/HL = 3.25 cm
d:Ge/Snout/Aperture/TransX = 0.0 cm
d:Ge/Snout/Aperture/TransY = 0.0 cm
d:Ge/Snout/Aperture/TransZ = Ge/Snout/BrassCone/LowerEdge + Ge/Snout/Aperture/HL cm
d:Ge/Snout/Aperture/RotX = 0.0 deg
d:Ge/Snout/Aperture/RotY = 0.0 deg
d:Ge/Snout/Aperture/RotZ = 90.0 deg
d:Ge/Snout/Aperture/LowerEdge = Ge/Snout/Aperture/TransZ + Ge/Snout/Aperture/HL cm
s:Ge/Snout/Aperture/Message = "ConstructingAperture"
b:Ge/Snout/Aperture/Invisible = "True"
#b:Ge/Aperture/IsParallel = "True"

##################################################
#Compensator
##################################################
s:Ge/Snout/Compensator/Type = "TsCompensator"
s:Ge/Snout/Compensator/Parent = "Snout"
s:Ge/Snout/Compensator/Material = "CompensatorLucite"
d:Ge/Snout/Compensator/RMax = 20 cm
d:Ge/Snout/Compensator/TransX = 0. cm
d:Ge/Snout/Compensator/TransY = 0. mm
dc:Ge/Snout/Compensator/Thickness = 0. cm #will be reset to actual thickness when compensator is read in
d:Ge/Snout/Compensator/HL = 0.5 * Ge/Snout/Compensator/Thickness cm
d:Ge/Snout/Compensator/TransZ = Ge/Snout/Aperture/LowerEdge + Ge/Snout/Compensator/HL cm
d:Ge/Snout/Compensator/LowerEdge = Ge/Snout/Compensator/TransZ + Ge/Snout/Compensator/HL cm
d:Ge/Snout/Compensator/RotX = 0. deg
d:Ge/Snout/Compensator/RotY = 0. deg
d:Ge/Snout/Compensator/RotZ = 90. deg
s:Ge/Snout/Compensator/InputFile = "CompensatorFileInRowsDepths.rc"
s:Ge/Snout/Compensator/FileFormat = "RowsAndDepths"
s:Ge/Snout/Compensator/Method = "ExtrudedSolid" #Polyhedra, ExtrudedSolid, SubtractionCylindersorUnionCylinders
#d:Ge/Snout/Compensator/XTolerance = 10.mm
#d:Ge/Snout/Compensator/YTolerance = 10.mm
b:Ge/Snout/Compensator/PrintPoints = "F"
#s:Ge/Snout/Compensator/Message = "ConstructingCompensator"
#b:Ge/Snout/Compensator/IsParallel = "True"
#s:Ge/Snout/Compensator/DrawingStyle = "Solid"
