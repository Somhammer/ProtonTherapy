#All coordination information comes from TsDefaultParameters.
#IEC 61217 compliance

#Fixed Reference system (If)     => World volume
#Gantry coordination system (Ig) => GantryCoordination
#Source coordination system (S)  => BeamPosition rotateX(180), Z position w.r.t GantryCoordination
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
#Material
#NitrogenGas for Chamber
#HeliumGas   for Pipe 
########################################

sv:Ma/NiGas/Components = 1 "Nitrogen"
uv:Ma/NiGas/Fractions = 1 1.0
d:Ma/NiGas/Density = 0.001251 g/cm3
#0.001251 g/cm3 (gas, 0 C, 101.325 kPa)

sv:Ma/HeGas/Components = 1 "Helium"
uv:Ma/HeGas/Fractions = 1 1.0
d:Ma/HeGas/Density = 0.000166322 g/cm3 

sv:Ma/Gold/Components = 1 "Gold"
uv:Ma/Gold/Fractions = 1 1.0
d:Ma/Gold/Density = 19.3 g/cm3
d:Ma/Gold/MeanExcitationEnergy = 790.0 eV
s:Ma/Gold/DefaultColor = "orange"

sv:Ma/Lexan/Components = 3 "Hydrogen" "Carbon" "Oxygen"
uv:Ma/Lexan/Fractions = 3 0.0555 0.7558 0.1887
d:Ma/Lexan/Density = 1.2 g/cm3

sv:Ma/CompensatorLucite/Components = 3 "Hydrogen" "Carbon" "Oxygen"
uv:Ma/CompensatorLucite/Fractions = 3 0.080538 0.599848 0.319614
d:Ma/CompensatorLucite/Density = 1.18 g/cm3
#d:Ma/CompensatorLucite/MeanExcitationEnergy = 74.0 eV
s:Ma/CompensatorLucite/DefaultColor = "grey"

sv:Ma/AlMylar/Components = 4 "Hydrogen" "Carbon" "Oxygen" "Aluminum"
uv:Ma/AlMylar/Fractions = 4 0.0302 0.45 0.24 0.2798
d:Ma/AlMylar/Density = 1.0 g/cm3
s:Ma/AlMylar/DefaultColor = "grey"

sv:Ma/Polyethylene/Components = 2 "Hydrogen" "Carbon"
uv:Ma/Polyethylene/Fractions = 2 0.666666 0.333333
d:Ma/Polyethylene/Density = 0.89 g/cm3
s:Ma/Polyethylene/DefaultColor = "grey"

sv:Ma/C/Components = 1 "Carbon"
uv:Ma/C/Fractions = 1 1
d:Ma/C/Density = 1.7 g/cm3
s:Ma/C/DefaultColor = "blue"

sv:Ma/Lead/Components = 1 "Lead"
uv:Ma/Lead/Fractions = 1 1
d:Ma/Lead/Density = 11.35 g/cm3
s:Ma/Lead/DefaultColor = "red"

sv:Ma/AlZnMgCu/Components = 4 "Aluminum" "Zinc" "Magnesium" "Copper"
uv:Ma/AlZnMgCu/Fractions = 4 0.25 0.25 0.25 0.25
d:Ma/AlZnMgCu/Density = 2.8 g/cm3
s:Ma/AlZnMgCu/DefaultColor = "red"

sv:Ma/CuZn39Pb3/Components = 3 "Copper" "Zinc" "Lead"
uv:Ma/CuZn39Pb3/Fractions = 3 0.5832 0.3802 0.0366
d:Ma/CuZn39Pb3/Density = 8.49 g/cm3

sv:Ma/Ni/Components = 1 "Nickel"
uv:Ma/Ni/Fractions = 1 1
d:Ma/Ni/Density = 7.81 g/cm3

sv:Ma/Brass/Components = 8 "Copper" "Lead" "Iron" "Aluminum" "Tin" "Silicon" "Manganese" "Zinc"
uv:Ma/Brass/Fractions  = 8 0.5775 0.0345 0.0025 0.0034 0.00002 0.00001 0.00001 0.38206
d:Ma/Brass/Density = 8.320331 g/cm3

########################################
# Physics
########################################
s:ph/ListName = "Default"
s:Ph/Default/Type = "Geant4_Modular"
sv:Ph/Default/Modules = 6 "g4em-standard_opt4" "g4decay" "g4h-elastic" "g4h-phy_QGSP_BIC_HP" "g4ion-binarycascade" "g4stopping"
d:Ph/Default/EMRaneMin = 100. eV
d:Ph/Default/EMRangeMax = 500 MeV

i:Tf/Verbosity = 1
d:Ph/Default/CutForElectron = 1 cm



