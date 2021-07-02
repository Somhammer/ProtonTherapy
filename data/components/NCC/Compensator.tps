includeFile = /home/seohyeon/work/ProtonTherapy/data/components/NCC/ConstantsForNozzles.tps
includeFile = /home/seohyeon/work/ProtonTherapy/data/components/NCC/N08_SNT.tps
includeFile = /home/seohyeon/work/ProtonTherapy/data/components/NCC/Aperture.tps

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
