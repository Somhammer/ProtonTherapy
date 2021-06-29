includeFile = /home/seohyeon/work/ProtonTherapy/data/components/NCC/ConstantsForNozzles.tps

########################################
#2. Monitor chamber 1.
# Filled with Nitrogen Gas, 16 layers
# Thickness, position, Material
#1  0.025	23	AlMylar
#2  0.025	28	AlMylar
#3  0.023	28.025	Polyethylene
#4  0.050	34.025	C
#5  0.050	34.075	Polyester
#6  0.050	34.125	C
#7  0.050	38.125	Al
#8  0.050	42.125	C
#9  0.050	42.175	Polyester
#10 0.050	42.225	C
#11 0.014	46.225	Al
#12 0.050	50.225	C
#13 0.050	50.275	Polyester
#14 0.050	50.325	C
#15 0.023	58.325	Polyethylene
#16 0.025	58.348	AlMylar
########################################
s:Ge/MonitorChamber1/Parent   = "Gantry"
s:Ge/MonitorChamber1/Type     = "TsBox"
s:Ge/MonitorChamber1/Material = "NiGas"
d:Ge/MonitorChamber1/HLX      = 88.0  mm
d:Ge/MonitorChamber1/HLY      = 120.0  mm
d:Ge/MonitorChamber1/HLZ      = 30.5  mm
d:Ge/MonitorChamber1/RotX     = 0.0 deg
d:Ge/MonitorChamber1/RotY     = 0.0 deg
d:Ge/MonitorChamber1/RotZ     = 0.0 deg
d:Ge/MonitorChamber1/TransX   = 0.0 mm
d:Ge/MonitorChamber1/TransY   = 0.0 mm
d:Ge/MonitorChamber1/MinusHL  = Ge/MonitorChamber1/HLZ mm * -1.0
d:Ge/MonitorChamber1/TransZ   = 2769.5 mm
b:Ge/MonitorChamber1/Include  = "TRUE"
s:Ge/MonitorChamber1/Message  = "Constructing IBA Monitor Chamber 1"

s:Ge/MonitorChamber1/Frame/Parent   = "MonitorChamber1"
s:Ge/MonitorChamber1/Frame/Type     = "TsCylinder"
s:Ge/MonitorChamber1/Frame/Material = "Aluminum"
d:Ge/MonitorChamber1/Frame/RMin     = 30.0 mm
d:Ge/MonitorChamber1/Frame/RMax     = 35.0 mm
d:Ge/MonitorChamber1/Frame/HL       = 11.5 mm
d:Ge/MonitorChamber1/Frame/SPhi     = 0.0   deg
d:Ge/MonitorChamber1/Frame/DPhi     = 360.0 deg
d:Ge/MonitorChamber1/Frame/RotX     = 0.0 deg
d:Ge/MonitorChamber1/Frame/RotY     = 0.0 deg
d:Ge/MonitorChamber1/Frame/RotZ     = 0.0 deg
d:Ge/MonitorChamber1/Frame/TransX   = 0.0 mm
d:Ge/MonitorChamber1/Frame/TransY   = 0.0 mm
d:Ge/MonitorChamber1/Frame/TransZ   = 19 mm
b:Ge/MonitorChamber1/Frame/Include  = "TRUE"

s:Ge/MonitorChamber1/Layer1/Parent   = "MonitorChamber1"
s:Ge/MonitorChamber1/Layer1/Type     = "TsCylinder"
s:Ge/MonitorChamber1/Layer1/Material = "AlMylar"
d:Ge/MonitorChamber1/Layer1/RMin     = 0.0   mm
d:Ge/MonitorChamber1/Layer1/RMax     = 42.0 mm
d:Ge/MonitorChamber1/Layer1/HL       = 0.0125  mm
d:Ge/MonitorChamber1/Layer1/SPhi     = 0.0   deg
d:Ge/MonitorChamber1/Layer1/DPhi     = 360.0 deg
d:Ge/MonitorChamber1/Layer1/RotX     = 0.0 deg
d:Ge/MonitorChamber1/Layer1/RotY     = 0.0 deg
d:Ge/MonitorChamber1/Layer1/RotZ     = 0.0 deg
d:Ge/MonitorChamber1/Layer1/TransX   = 0.0 mm
d:Ge/MonitorChamber1/Layer1/TransY   = 0.0 mm
d:Ge/MonitorChamber1/Layer1/TransZ   = 7.4875 mm
b:Ge/MonitorChamber1/Layer1/Include  = "TRUE"

s:Ge/MonitorChamber1/Layer2/Parent   = "MonitorChamber1"
s:Ge/MonitorChamber1/Layer2/Type     = "TsCylinder"
s:Ge/MonitorChamber1/Layer2/Material = "AlMylar"
d:Ge/MonitorChamber1/Layer2/RMin     = 0.0   mm
d:Ge/MonitorChamber1/Layer2/RMax     = 42.0 mm
d:Ge/MonitorChamber1/Layer2/HL       = 0.0125  mm
d:Ge/MonitorChamber1/Layer2/SPhi     = 0.0   deg
d:Ge/MonitorChamber1/Layer2/DPhi     = 360.0 deg
d:Ge/MonitorChamber1/Layer2/RotX     = 0.0 deg
d:Ge/MonitorChamber1/Layer2/RotY     = 0.0 deg
d:Ge/MonitorChamber1/Layer2/RotZ     = 0.0 deg
d:Ge/MonitorChamber1/Layer2/TransX   = 0.0 mm
d:Ge/MonitorChamber1/Layer2/TransY   = 0.0 mm
d:Ge/MonitorChamber1/Layer2/TransZ   = 2.4875 mm
b:Ge/MonitorChamber1/Layer2/Include  = "TRUE"

s:Ge/MonitorChamber1/Layer3/Parent   = "MonitorChamber1"
s:Ge/MonitorChamber1/Layer3/Type     = "TsCylinder"
s:Ge/MonitorChamber1/Layer3/Material = "Polyethylene"
d:Ge/MonitorChamber1/Layer3/RMin     = 0.0   mm
d:Ge/MonitorChamber1/Layer3/RMax     = 42.0 mm
d:Ge/MonitorChamber1/Layer3/HL       = 0.0115  mm
d:Ge/MonitorChamber1/Layer3/SPhi     = 0.0   deg
d:Ge/MonitorChamber1/Layer3/DPhi     = 360.0 deg
d:Ge/MonitorChamber1/Layer3/RotX     = 0.0 deg
d:Ge/MonitorChamber1/Layer3/RotY     = 0.0 deg
d:Ge/MonitorChamber1/Layer3/RotZ     = 0.0 deg
d:Ge/MonitorChamber1/Layer3/TransX   = 0.0 mm
d:Ge/MonitorChamber1/Layer3/TransY   = 0.0 mm
d:Ge/MonitorChamber1/Layer3/TransZ   = 2.4635 mm
b:Ge/MonitorChamber1/Layer3/Include  = "TRUE"

s:Ge/MonitorChamber1/Layer4/Parent   = "MonitorChamber1"
s:Ge/MonitorChamber1/Layer4/Type     = "TsCylinder"
s:Ge/MonitorChamber1/Layer4/Material = "Carbon"
d:Ge/MonitorChamber1/Layer4/RMin     = 0.0   mm
d:Ge/MonitorChamber1/Layer4/RMax     = 42.0 mm
d:Ge/MonitorChamber1/Layer4/HL       = 0.025  mm
d:Ge/MonitorChamber1/Layer4/SPhi     = 0.0   deg
d:Ge/MonitorChamber1/Layer4/DPhi     = 360.0 deg
d:Ge/MonitorChamber1/Layer4/RotX     = 0.0 deg
d:Ge/MonitorChamber1/Layer4/RotY     = 0.0 deg
d:Ge/MonitorChamber1/Layer4/RotZ     = 0.0 deg
d:Ge/MonitorChamber1/Layer4/TransX   = 0.0 mm
d:Ge/MonitorChamber1/Layer4/TransY   = 0.0 mm
d:Ge/MonitorChamber1/Layer4/TransZ   = -3.55 mm
b:Ge/MonitorChamber1/Layer4/Include  = "TRUE"

s:Ge/MonitorChamber1/Layer5/Parent   = "MonitorChamber1"
s:Ge/MonitorChamber1/Layer5/Type     = "TsCylinder"
s:Ge/MonitorChamber1/Layer5/Material = "Mylar"
d:Ge/MonitorChamber1/Layer5/RMin     = 0.0   mm
d:Ge/MonitorChamber1/Layer5/RMax     = 42.0 mm
d:Ge/MonitorChamber1/Layer5/HL       = 0.025  mm
d:Ge/MonitorChamber1/Layer5/SPhi     = 0.0   deg
d:Ge/MonitorChamber1/Layer5/DPhi     = 360.0 deg
d:Ge/MonitorChamber1/Layer5/RotX     = 0.0 deg
d:Ge/MonitorChamber1/Layer5/RotY     = 0.0 deg
d:Ge/MonitorChamber1/Layer5/RotZ     = 0.0 deg
d:Ge/MonitorChamber1/Layer5/TransX   = 0.0 mm
d:Ge/MonitorChamber1/Layer5/TransY   = 0.0 mm
d:Ge/MonitorChamber1/Layer5/TransZ   = -3.6 mm
b:Ge/MonitorChamber1/Layer5/Include  = "TRUE"

s:Ge/MonitorChamber1/Layer6/Parent   = "MonitorChamber1"
s:Ge/MonitorChamber1/Layer6/Type     = "TsCylinder"
s:Ge/MonitorChamber1/Layer6/Material = "Carbon"
d:Ge/MonitorChamber1/Layer6/RMin     = 0.0   mm
d:Ge/MonitorChamber1/Layer6/RMax     = 42.0 mm
d:Ge/MonitorChamber1/Layer6/HL       = 0.025  mm
d:Ge/MonitorChamber1/Layer6/SPhi     = 0.0   deg
d:Ge/MonitorChamber1/Layer6/DPhi     = 360.0 deg
d:Ge/MonitorChamber1/Layer6/RotX     = 0.0 deg
d:Ge/MonitorChamber1/Layer6/RotY     = 0.0 deg
d:Ge/MonitorChamber1/Layer6/RotZ     = 0.0 deg
d:Ge/MonitorChamber1/Layer6/TransX   = 0.0 mm
d:Ge/MonitorChamber1/Layer6/TransY   = 0.0 mm
d:Ge/MonitorChamber1/Layer6/TransZ   = -3.65 mm
b:Ge/MonitorChamber1/Layer6/Include  = "TRUE"

s:Ge/MonitorChamber1/Layer7/Parent   = "MonitorChamber1"
s:Ge/MonitorChamber1/Layer7/Type     = "TsCylinder"
s:Ge/MonitorChamber1/Layer7/Material = "Aluminum"
d:Ge/MonitorChamber1/Layer7/RMin     = 0.0   mm
d:Ge/MonitorChamber1/Layer7/RMax     = 42.0 mm
d:Ge/MonitorChamber1/Layer7/HL       = 0.007  mm
d:Ge/MonitorChamber1/Layer7/SPhi     = 0.0   deg
d:Ge/MonitorChamber1/Layer7/DPhi     = 360.0 deg
d:Ge/MonitorChamber1/Layer7/RotX     = 0.0 deg
d:Ge/MonitorChamber1/Layer7/RotY     = 0.0 deg
d:Ge/MonitorChamber1/Layer7/RotZ     = 0.0 deg
d:Ge/MonitorChamber1/Layer7/TransX   = 0.0 mm
d:Ge/MonitorChamber1/Layer7/TransY   = 0.0 mm
d:Ge/MonitorChamber1/Layer7/TransZ   = -7.632 mm
b:Ge/MonitorChamber1/Layer7/Include  = "TRUE"

s:Ge/MonitorChamber1/Layer8/Parent   = "MonitorChamber1"
s:Ge/MonitorChamber1/Layer8/Type     = "TsCylinder"
s:Ge/MonitorChamber1/Layer8/Material = "Carbon"
d:Ge/MonitorChamber1/Layer8/RMin     = 0.0   mm
d:Ge/MonitorChamber1/Layer8/RMax     = 42.0 mm
d:Ge/MonitorChamber1/Layer8/HL       = 0.025  mm
d:Ge/MonitorChamber1/Layer8/SPhi     = 0.0   deg
d:Ge/MonitorChamber1/Layer8/DPhi     = 360.0 deg
d:Ge/MonitorChamber1/Layer8/RotX     = 0.0 deg
d:Ge/MonitorChamber1/Layer8/RotY     = 0.0 deg
d:Ge/MonitorChamber1/Layer8/RotZ     = 0.0 deg
d:Ge/MonitorChamber1/Layer8/TransX   = 0.0 mm
d:Ge/MonitorChamber1/Layer8/TransY   = 0.0 mm
d:Ge/MonitorChamber1/Layer8/TransZ   = -11.65 mm
b:Ge/MonitorChamber1/Layer8/Include  = "TRUE"

s:Ge/MonitorChamber1/Layer9/Parent   = "MonitorChamber1"
s:Ge/MonitorChamber1/Layer9/Type     = "TsCylinder"
s:Ge/MonitorChamber1/Layer9/Material = "Mylar"
d:Ge/MonitorChamber1/Layer9/RMin     = 0.0   mm
d:Ge/MonitorChamber1/Layer9/RMax     = 42.0 mm
d:Ge/MonitorChamber1/Layer9/HL       = 0.025  mm
d:Ge/MonitorChamber1/Layer9/SPhi     = 0.0   deg
d:Ge/MonitorChamber1/Layer9/DPhi     = 360.0 deg
d:Ge/MonitorChamber1/Layer9/RotX     = 0.0 deg
d:Ge/MonitorChamber1/Layer9/RotY     = 0.0 deg
d:Ge/MonitorChamber1/Layer9/RotZ     = 0.0 deg
d:Ge/MonitorChamber1/Layer9/TransX   = 0.0 mm
d:Ge/MonitorChamber1/Layer9/TransY   = 0.0 mm
d:Ge/MonitorChamber1/Layer9/TransZ   = -11.7 mm
b:Ge/MonitorChamber1/Layer9/Include  = "TRUE"

s:Ge/MonitorChamber1/Layer10/Parent   = "MonitorChamber1"
s:Ge/MonitorChamber1/Layer10/Type     = "TsCylinder"
s:Ge/MonitorChamber1/Layer10/Material = "Carbon"
d:Ge/MonitorChamber1/Layer10/RMin     = 0.0   mm
d:Ge/MonitorChamber1/Layer10/RMax     = 42.0 mm
d:Ge/MonitorChamber1/Layer10/HL       = 0.025  mm
d:Ge/MonitorChamber1/Layer10/SPhi     = 0.0   deg
d:Ge/MonitorChamber1/Layer10/DPhi     = 360.0 deg
d:Ge/MonitorChamber1/Layer10/RotX     = 0.0 deg
d:Ge/MonitorChamber1/Layer10/RotY     = 0.0 deg
d:Ge/MonitorChamber1/Layer10/RotZ     = 0.0 deg
d:Ge/MonitorChamber1/Layer10/TransX   = 0.0 mm
d:Ge/MonitorChamber1/Layer10/TransY   = 0.0 mm
d:Ge/MonitorChamber1/Layer10/TransZ   = -11.75 mm
b:Ge/MonitorChamber1/Layer10/Include  = "TRUE"

s:Ge/MonitorChamber1/Layer11/Parent   = "MonitorChamber1"
s:Ge/MonitorChamber1/Layer11/Type     = "TsCylinder"
s:Ge/MonitorChamber1/Layer11/Material = "Aluminum"
d:Ge/MonitorChamber1/Layer11/RMin     = 0.0   mm
d:Ge/MonitorChamber1/Layer11/RMax     = 42.0 mm
d:Ge/MonitorChamber1/Layer11/HL       = 0.007  mm
d:Ge/MonitorChamber1/Layer11/SPhi     = 0.0   deg
d:Ge/MonitorChamber1/Layer11/DPhi     = 360.0 deg
d:Ge/MonitorChamber1/Layer11/RotX     = 0.0 deg
d:Ge/MonitorChamber1/Layer11/RotY     = 0.0 deg
d:Ge/MonitorChamber1/Layer11/RotZ     = 0.0 deg
d:Ge/MonitorChamber1/Layer11/TransX   = 0.0 mm
d:Ge/MonitorChamber1/Layer11/TransY   = 0.0 mm
d:Ge/MonitorChamber1/Layer11/TransZ   = -15.732 mm
b:Ge/MonitorChamber1/Layer11/Include  = "TRUE"

s:Ge/MonitorChamber1/Layer12/Parent   = "MonitorChamber1"
s:Ge/MonitorChamber1/Layer12/Type     = "TsCylinder"
s:Ge/MonitorChamber1/Layer12/Material = "Carbon"
d:Ge/MonitorChamber1/Layer12/RMin     = 0.0   mm
d:Ge/MonitorChamber1/Layer12/RMax     = 42.0 mm
d:Ge/MonitorChamber1/Layer12/HL       = 0.025  mm
d:Ge/MonitorChamber1/Layer12/SPhi     = 0.0   deg
d:Ge/MonitorChamber1/Layer12/DPhi     = 360.0 deg
d:Ge/MonitorChamber1/Layer12/RotX     = 0.0 deg
d:Ge/MonitorChamber1/Layer12/RotY     = 0.0 deg
d:Ge/MonitorChamber1/Layer12/RotZ     = 0.0 deg
d:Ge/MonitorChamber1/Layer12/TransX   = 0.0 mm
d:Ge/MonitorChamber1/Layer12/TransY   = 0.0 mm
d:Ge/MonitorChamber1/Layer12/TransZ   = -19.75 mm
b:Ge/MonitorChamber1/Layer12/Include  = "TRUE"

s:Ge/MonitorChamber1/Layer13/Parent   = "MonitorChamber1"
s:Ge/MonitorChamber1/Layer13/Type     = "TsCylinder"
s:Ge/MonitorChamber1/Layer13/Material = "Mylar"
d:Ge/MonitorChamber1/Layer13/RMin     = 0.0   mm
d:Ge/MonitorChamber1/Layer13/RMax     = 42.0 mm
d:Ge/MonitorChamber1/Layer13/HL       = 0.025  mm
d:Ge/MonitorChamber1/Layer13/SPhi     = 0.0   deg
d:Ge/MonitorChamber1/Layer13/DPhi     = 360.0 deg
d:Ge/MonitorChamber1/Layer13/RotX     = 0.0 deg
d:Ge/MonitorChamber1/Layer13/RotY     = 0.0 deg
d:Ge/MonitorChamber1/Layer13/RotZ     = 0.0 deg
d:Ge/MonitorChamber1/Layer13/TransX   = 0.0 mm
d:Ge/MonitorChamber1/Layer13/TransY   = 0.0 mm
d:Ge/MonitorChamber1/Layer13/TransZ   = -19.8 mm
b:Ge/MonitorChamber1/Layer13/Include  = "TRUE"

s:Ge/MonitorChamber1/Layer14/Parent   = "MonitorChamber1"
s:Ge/MonitorChamber1/Layer14/Type     = "TsCylinder"
s:Ge/MonitorChamber1/Layer14/Material = "Carbon"
d:Ge/MonitorChamber1/Layer14/RMin     = 0.0   mm
d:Ge/MonitorChamber1/Layer14/RMax     = 42.0 mm
d:Ge/MonitorChamber1/Layer14/HL       = 0.025  mm
d:Ge/MonitorChamber1/Layer14/SPhi     = 0.0   deg
d:Ge/MonitorChamber1/Layer14/DPhi     = 360.0 deg
d:Ge/MonitorChamber1/Layer14/RotX     = 0.0 deg
d:Ge/MonitorChamber1/Layer14/RotY     = 0.0 deg
d:Ge/MonitorChamber1/Layer14/RotZ     = 0.0 deg
d:Ge/MonitorChamber1/Layer14/TransX   = 0.0 mm
d:Ge/MonitorChamber1/Layer14/TransY   = 0.0 mm
d:Ge/MonitorChamber1/Layer14/TransZ   = -19.85 mm
b:Ge/MonitorChamber1/Layer14/Include  = "TRUE"

s:Ge/MonitorChamber1/Layer15/Parent   = "MonitorChamber1"
s:Ge/MonitorChamber1/Layer15/Type     = "TsCylinder"
s:Ge/MonitorChamber1/Layer15/Material = "Polyethylene"
d:Ge/MonitorChamber1/Layer15/RMin     = 0.0   mm
d:Ge/MonitorChamber1/Layer15/RMax     = 42.0 mm
d:Ge/MonitorChamber1/Layer15/HL       = 0.0115  mm
d:Ge/MonitorChamber1/Layer15/SPhi     = 0.0   deg
d:Ge/MonitorChamber1/Layer15/DPhi     = 360.0 deg
d:Ge/MonitorChamber1/Layer15/RotX     = 0.0 deg
d:Ge/MonitorChamber1/Layer15/RotY     = 0.0 deg
d:Ge/MonitorChamber1/Layer15/RotZ     = 0.0 deg
d:Ge/MonitorChamber1/Layer15/TransX   = 0.0 mm
d:Ge/MonitorChamber1/Layer15/TransY   = 0.0 mm
d:Ge/MonitorChamber1/Layer15/TransZ   = -27.8365 mm
b:Ge/MonitorChamber1/Layer15/Include  = "TRUE"

s:Ge/MonitorChamber1/Layer16/Parent   = "MonitorChamber1"
s:Ge/MonitorChamber1/Layer16/Type     = "TsCylinder"
s:Ge/MonitorChamber1/Layer16/Material = "AlMylar"
d:Ge/MonitorChamber1/Layer16/RMin     = 0.0   mm
d:Ge/MonitorChamber1/Layer16/RMax     = 42.0 mm
d:Ge/MonitorChamber1/Layer16/HL       = 0.0125  mm
d:Ge/MonitorChamber1/Layer16/SPhi     = 0.0   deg
d:Ge/MonitorChamber1/Layer16/DPhi     = 360.0 deg
d:Ge/MonitorChamber1/Layer16/RotX     = 0.0 deg
d:Ge/MonitorChamber1/Layer16/RotY     = 0.0 deg
d:Ge/MonitorChamber1/Layer16/RotZ     = 0.0 deg
d:Ge/MonitorChamber1/Layer16/TransX   = 0.0 mm
d:Ge/MonitorChamber1/Layer16/TransY   = 0.0 mm
d:Ge/MonitorChamber1/Layer16/TransZ   = -27.8605 mm
b:Ge/MonitorChamber1/Layer16/Include  = "TRUE"
