includeFile = /home/seohyeon/work/ProtonTherapy/data/components/NCC/Materials.tps
#All coordination information comes from TsDefaultParameters.
#IEC 61217 compliance

#Fixed Reference system (If) => World volume
#Gantry coordination system (Ig) => GantryCoordination
#Source coordination system (S)=> BeamPosition rotateX(180), Z position w.r.t GantryCoordination
#Beam source coordinate system rotate 180 and translate along z w.r.t g.
#-> Y is -Y. we have to flip phase space data.
#Isocenter coordination system (Io)
d:Ge/World/HLX = 1. m
d:Ge/World/HLY = 1. m
d:Ge/World/HLZ = 3. m
s:Ge/World/Material = "NiGas"
#S2I
#d:Ge/S2I = 3.0 m

#Gantry coordination system (Ig)
s:Ge/Gantry/Parent = "World"
s:Ge/Gantry/Type = "Group"
d:Ge/Gantry/TransX = 0. m
d:Ge/Gantry/TransY = 0. m
d:Ge/Gantry/TransZ = 0. m
d:Ge/Gantry/RotX = 0. deg
d:Ge/Gantry/RotY = 180. deg
d:Ge/Gantry/RotZ = 0. deg
s:Ge/Gantry/Material = "NiGas"

# Default Beam position
s:Ge/BeamPosition/Parent = "Gantry"
s:Ge/BeamPosition/Type = "Group"
d:Ge/BeamPosition/TransX = 0. m
d:Ge/BeamPosition/TransY = 0. m
d:Ge/BeamPosition/TransZ = 3.0 m
d:Ge/BeamPosition/RotX = 180. deg
d:Ge/BeamPosition/RotY = 0. deg
d:Ge/BeamPosition/RotZ = 0. deg

b:Ts/ShowCPUTime = "true"
i:Ts/ShowHistoryCountAtInterval = 0
b:Ts/ShowHistoryCountOnSingleLine = "False"

########################################
# Physics
########################################
s:Ph/ListName = "Default"
s:Ph/Default/Type = "Geant4_Modular"
sv:Ph/Default/Modules = 6 "g4em-standard_opt4" "g4decay" "g4h-elastic" "g4h-phy_QGSP_BIC_HP" "g4ion-binarycascade" "g4stopping"
d:Ph/Default/EMRaneMin = 100. eV
d:Ph/Default/EMRangeMax = 500 MeV

i:Tf/Verbosity = 1
d:Ph/Default/CutForElectron = 1 cm
