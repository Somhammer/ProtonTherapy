# Magnet Field X
s:Ge/ScanningMagnetX/Type = "TsBox"
s:Ge/ScanningMagnetX/Parent = "World"
s:Ge/ScanningMagnetX/Material = "World"
d:Ge/ScanningMagnetX/HLX = 20 cm
d:Ge/ScanningMagnetX/HLY = 10 cm
d:Ge/ScanningMagnetX/HLZ = 10 cm
d:Ge/ScanningMagnetX/TransZ = -190 cm
s:Ge/ScanningMagnetX/Field = "DipoleMagnet"
u:Ge/ScanningMagnetX/MagneticFieldDirectionX= 0.0
u:Ge/ScanningMagnetX/MagneticFieldDirectionY= Tf/MagnetXdir/Value
u:Ge/ScanningMagnetX/MagneticFieldDirectionZ= 0.0
d:Ge/ScanningMagnetX/MagneticFieldStrength = 1.0 tesla * Tf/MagnetXmag/Value

# Magnet Field Y
s:Ge/ScanningMagnetY/Type = "TsBox"
s:Ge/ScanningMagnetY/Parent = "World"
s:Ge/ScanningMagnetY/Material = "World"
d:Ge/ScanningMagnetY/HLX = 10 cm
d:Ge/ScanningMagnetY/HLY = 20 cm
d:Ge/ScanningMagnetY/HLZ = 10 cm
d:Ge/ScanningMagnetY/TransZ = -230 cm
s:Ge/ScanningMagnetY/Field = "DipoleMagnet"
u:Ge/ScanningMagnetY/MagneticFieldDirectionX= Tf/MagnetYdir/Value
u:Ge/ScanningMagnetY/MagneticFieldDirectionY= 0.0
u:Ge/ScanningMagnetY/MagneticFieldDirectionZ= 0.0
d:Ge/ScanningMagnetY/MagneticFieldStrength = 1.0 tesla * Tf/MagnetYmag/Value
