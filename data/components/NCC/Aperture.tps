includeFile = /home/seohyeon/work/ProtonTherapy/data/components/NCC/ConstantsForNozzles.tps
includeFile = /home/seohyeon/work/ProtonTherapy/data/components/NCC/N08_SNT.tps

##################################################
#Aperture
##################################################
s:Ge/Aperture/Type = "TsAperture"
s:Ge/Aperture/Parent = "Snout"
s:Ge/Aperture/InputFile = "ApertureFileIn.ap"
s:Ge/Aperture/FileFormat = "XYCoordinates"
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
