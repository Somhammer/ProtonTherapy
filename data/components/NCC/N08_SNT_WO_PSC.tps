includeFile = /home/seohyeon/work/ProtonTherapy/data/components/NCC/ConstantsForNozzles.tps
# Snout: 
##################################################
s:Ge/Snout/Type		="Group"
s:Ge/Snout/Parent	="World"
d:Ge/Snout/TransX	= 0. m
d:Ge/Snout/TransY	= 0. m
d:Ge/Snout/TransZ	= -47.25 cm
d:Ge/Snout/RotX		= 0. deg
d:Ge/Snout/RotY		= 0. deg
d:Ge/Snout/RotZ		= 0. deg
s:Ge/Snout/Message 	= "Constructing Snout"

d:Ge/Snout/SNT100R1	= 55	mm
d:Ge/Snout/SNT180R1	= 90	mm
d:Ge/Snout/SNT250R1	= 135	mm
d:Ge/Snout/SNT100R2	= 90	mm
d:Ge/Snout/SNT180R2	= 125	mm
d:Ge/Snout/SNT250R2	= 160	mm

d:Ge/Snout/SNTTypeR1	= Ge/Snout/SNT250R1 mm
d:Ge/Snout/SNTTypeR2	= Ge/Snout/SNT250R2 mm

# Snout:
s:Ge/Snout/Block/Parent 	= "Snout"
s:Ge/Snout/Block/Type   	= "TsBox"
s:Ge/Snout/Block/Material 	= "NiGas"
d:Ge/Snout/Block/HLX 		= 20.0 cm 
d:Ge/Snout/Block/HLY 		= 20.0 cm
d:Ge/Snout/Block/HLZ 		= 3.25 cm
d:Ge/Snout/Block/TransX		= 0. cm
d:Ge/Snout/Block/TransY		= 0. cm
d:Ge/Snout/Block/TransZ		= 0. cm
d:Ge/Snout/Block/RotX		= 0. deg
d:Ge/Snout/Block/RotY		= 0. deg
d:Ge/Snout/Block/RotZ		= 0. deg
s:Ge/Snout/Block/DrawingStyle = "Solid"
d:Ge/Snout/Block/LowerEdge	= Ge/Snout/Block/HLZ cm

# Snout: Hole in Brass Block
s:Ge/Snout/Hole/Parent 		= "Snout/Block"
s:Ge/Snout/Hole/Type   		= "TsCylinder"
s:Ge/Snout/Hole/Material	= "Air"
d:Ge/Snout/Hole/RMin 		=  0.0 cm
d:Ge/Snout/Hole/RMax 		=  Ge/Snout/SNTTypeR1 mm
#d:Ge/Snout/Hole/HL		=  6.75 cm
d:Ge/Snout/Hole/HL		=  3.25 cm
d:Ge/Snout/Hole/TransX 		=  0.0 cm
d:Ge/Snout/Hole/TransY 		=  0.0 cm
d:Ge/Snout/Hole/TransZ 		=  0.0 cm
d:Ge/Snout/Hole/RotX 		=  0.0 deg
d:Ge/Snout/Hole/RotY 		=  0.0 deg
d:Ge/Snout/Hole/RotZ 		=  0.0 deg
d:Ge/Snout/Hole/SPhi 		=  0.0 deg
d:Ge/Snout/Hole/DPhi 		=  360.0 deg
s:Ge/Snout/Hole/DrawingStyle = "Solid"

# Snout: Brass Cone 
s:Ge/Snout/BrassCone/Parent 	= "Snout"
s:Ge/Snout/BrassCone/Type   	= "TsCylinder"
s:Ge/Snout/BrassCone/Material	= "NiGas"
#d:Ge/Snout/BrassCone/RMin 	=  5.5 cm
d:Ge/Snout/BrassCone/RMin 	=  Ge/Snout/SNTTypeR1 mm
d:Ge/Snout/BrassCone/RMax 	=  Ge/Snout/SNTTypeR2 mm
d:Ge/Snout/BrassCone/HL		=  12.0 cm
d:Ge/Snout/BrassCone/TransX 	=  0.0 cm
d:Ge/Snout/BrassCone/TransY 	=  0.0 cm
d:Ge/Snout/BrassCone/TransZ 	=  Ge/Snout/Block/LowerEdge + Ge/Snout/BrassCone/HL cm
d:Ge/Snout/BrassCone/RotX 	=  0.0 deg
d:Ge/Snout/BrassCone/RotY 	=  0.0 deg
d:Ge/Snout/BrassCone/RotZ 	=  0.0 deg
d:Ge/Snout/BrassCone/SPhi 	=  0.0 deg
d:Ge/Snout/BrassCone/DPhi 	=  360.0 deg
s:Ge/Snout/BrassCone/DrawingStyle = "Solid"
d:Ge/Snout/BrassCone/LowerEdge	=  Ge/Snout/BrassCone/TransZ + Ge/Snout/BrassCone/HL cm
