s:Ge/SmallWheel/Type = "TsRangeModulator"
s:Ge/SmallWheel/Material = "Parent"
s:Ge/SmallWheel/Parent = "RangeModulator"
d:Ge/SmallWheel/TransX = 0.0 cm
d:Ge/SmallWheel/TransY = 0.0 cm
d:Ge/SmallWheel/TransZ = 0.0 mm
d:Ge/SmallWheel/RotX = 0.0 deg
d:Ge/SmallWheel/RotY = 0.0 deg
d:Ge/SmallWheel/RotZ = 0.0 deg
b:Ge/SmallWheel/Invisible = "TRUE"
b:Ge/SmallWheel/PrintInformation = "false"

d:Ge/SmallWheel/HeightOfUpper = 0.0 mm
d:Ge/SmallWheel/HeightOfMiddle = 0.0 mm
d:Ge/SmallWheel/HeightOfLower = 0.0 mm

d:Ge/SmallWheel/Shell/Rin = 0.0 cm
d:Ge/SmallWheel/Shell/Rout = 0.0 cm
s:Ge/SmallWheel/Shell/Material = "Aluminum"
s:Ge/SmallWheel/Shell/Color = "grey"
s:Ge/SmallWheel/Shell/DrawingStyle = "Solid"
i:Ge/SmallWheel/Shell/VisSegsPerCircle = 360

d:Ge/SmallWheel/Hub/Rin = 0.0 cm
d:Ge/SmallWheel/Hub/Rout = 0.0 cm
s:Ge/SmallWheel/Hub/Material = "Aluminum"
s:Ge/SmallWheel/Hub/Color = "grey"
s:Ge/SmallWheel/Hub/DrawingStyle = "Solid"
i:Ge/SmallWheel/Hub/VisSegsPerCircle = 360

dv:Ge/SmallWheel/Upper/RadialDivisions = 2 10 13 cm
s:Ge/SmallWheel/Upper/Track1/Pattern = "UpperBlockT1"
s:Ge/SmallWheel/Upper/Track2/Pattern = "UpperBlockT2"
s:Ge/SmallWheel/Upper/Track3/Pattern = "UpperBlockT3"

dv:Ge/SmallWheel/Middle/RadialDivisions = 1 15 cm
s:Ge/SmallWheel/Middle/Track1/Pattern = "InterfaceDisk"
s:Ge/SmallWheel/Middle/Track2/Pattern = "InterfaceDisk"

dv:Ge/SmallWheel/Lower/RadialDivisions = 2 10 13 cm
s:Ge/SmallWheel/Lower/Track1/Pattern = "LowerBlockT1"
s:Ge/SmallWheel/Lower/Track2/Pattern = "LowerBlockT2"
s:Ge/SmallWheel/Lower/Track3/Pattern = "LowerBlockT3"

d:Ge/UpperBlockT1/Offset = 0 deg
dv:Ge/UpperBlockT1/Angles = 1 0.0 deg
dv:Ge/UpperBlockT1/Heights = 1 0.0 mm
sv:Ge/UpperBlockT1/Materials=1 "Air" 

dv:Ge/InterfaceDisk/Angles = 1 0.0 deg
dv:Ge/InterfaceDisk/Heights = 1 0.0 mm
sv:Ge/InterfaceDisk/Materials = 1 "AlZnMgCu"

dv:Ge/HoleTrackDisk/Angles = 2 90 110 deg
dv:Ge/HoleTrackDisk/Heights = 2 0 1 mm
sv:Ge/HoleTrackDisk/Materials = 2 "NULL" "Aluminum"

d:Ge/LowerBlockT1/Offset = 0 deg
dv:Ge/LowerBlockT1/Angles = 1 0.0 deg
dv:Ge/LowerBlockT1/Heights = 1 0.0 mm
sv:Ge/LowerBlockT1/Materials = 1 "Air" 

d:Ge/UpperBlockT2/Offset = 0 deg
dv:Ge/UpperBlockT2/Angles = 1 0.0 deg
dv:Ge/UpperBlockT2/Heights = 1 0.0 mm
sv:Ge/UpperBlockT2/Materials = 1 "Air" 

d:Ge/LowerBlockT2/Offset = 0 deg
dv:Ge/LowerBlockT2/Angles = 1 0.0 deg
dv:Ge/LowerBlockT2/Heights = 1 0.0 mm
sv:Ge/LowerBlockT2/Materials = 1 "Air"

d:Ge/UpperBlockT3/Offset = 0 deg
dv:Ge/UpperBlockT3/Angles = 1 0.0 deg
dv:Ge/UpperBlockT3/Heights = 1 0.0 mm
sv:Ge/UpperBlockT3/Materials = 1 "Air" 

d:Ge/LowerBlockT3/Offset = 0 deg
dv:Ge/LowerBlockT3/Angles = 1 0.0 deg
dv:Ge/LowerBlockT3/Heights = 1 0.0 mm
sv:Ge/LowerBlockT3/Materials = 1 "Air"
