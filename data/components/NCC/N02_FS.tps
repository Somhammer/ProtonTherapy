includeFile = /home/seohyeon/work/ProtonTherapy/data/components/ConstantsForNozzles.tps
###############################################################
# First Scatterer:	9 lollipop
#	Lx	Ly	Lz	dX	dY	posZ	Mat
#	125	50	5.480	25	0	14	Lexan
#	125	50	0.125	-25	0	20	Pb
#	50	121.5	0.500	0	39.25	22	Pb	
#	125	50	1.000	25	0	29	Pb
#	125	50	0.250	-25	0	33	Pb
#	50	121.5	0.060	0	39.25	37	Pb
#	125	50	2.740	25	0	44	Lexan
#	125	50	1.370	-25	0	48	Lexan
#	50	121.5	0.030	0	39.25	52	Pb
###############################################################
s:Ge/Scatterer1/Type  	= "Group"
s:Ge/Scatterer1/Parent 	= "Gantry"
d:Ge/Scatterer1/TransX 	=  -9 cm
#d:Ge/Scatterer1/TransX 	=  0 cm
d:Ge/Scatterer1/TransY 	=  -5.0 cm
#d:Ge/Scatterer1/TransY 	=  -2.5 cm
d:Ge/Scatterer1/TransZ 	= 2697.5 mm  # 280 default
d:Ge/Scatterer1/RotX 	= 0. deg
d:Ge/Scatterer1/RotY 	= 0. deg
d:Ge/Scatterer1/RotZ 	= 0. deg
s:Ge/Scatterer1/Message 	= "Constructing IBA TsScatterer1"
s:Ge/Scatterer1/DrawingStyle = "Solid"

# Center for rotation of scatterers:
#d:Ge/Scatterer1/RotationCenterY = 0.38125 cm
d:Ge/Scatterer1/RotationCenterY = 5 cm
# Defining the in and out of beam rotation angle
d:Ge/Scatterer1/RotZ_InBeam    	=  90.0 deg
d:Ge/Scatterer1/RotZ_OutOfBeam 	=   0.0 deg

d:Ge/Scatterer1/Lollipop1       = Ge/Scatterer1/RotZ_OutOfBeam deg
d:Ge/Scatterer1/Lollipop2       = Ge/Scatterer1/RotZ_OutOfBeam deg
d:Ge/Scatterer1/Lollipop3       = Ge/Scatterer1/RotZ_OutOfBeam deg
d:Ge/Scatterer1/Lollipop4       = Ge/Scatterer1/RotZ_OutOfBeam deg
d:Ge/Scatterer1/Lollipop5       = Ge/Scatterer1/RotZ_OutOfBeam deg
d:Ge/Scatterer1/Lollipop6       = Ge/Scatterer1/RotZ_OutOfBeam deg
d:Ge/Scatterer1/Lollipop7       = Ge/Scatterer1/RotZ_OutOfBeam deg
d:Ge/Scatterer1/Lollipop8       = Ge/Scatterer1/RotZ_OutOfBeam deg
d:Ge/Scatterer1/Lollipop9       = Ge/Scatterer1/RotZ_OutOfBeam deg

# Lollipop 1:
s:Ge/Scatterer1/L1/Type   	= "Group"
s:Ge/Scatterer1/L1/Parent 	= "Scatterer1"
d:Ge/Scatterer1/L1/TransX 	= 0.0 cm
d:Ge/Scatterer1/L1/TransY 	= Ge/Scatterer1/RotationCenterY cm
d:Ge/Scatterer1/L1/TransZ 	= 0.0 cm
d:Ge/Scatterer1/L1/RotX 	= 0. deg
d:Ge/Scatterer1/L1/RotY 	= 0. deg
d:Ge/Scatterer1/L1/RotZ 	= Ge/Scatterer1/Lollipop1 deg

# L1 Lead Foil:
s:Ge/Scatterer1/L1/LeadFoil/Parent	= "Scatterer1/L1"
s:Ge/Scatterer1/L1/LeadFoil/Type  	= "TsBox"
s:Ge/Scatterer1/L1/LeadFoil/Material 	= "Lexan"
d:Ge/Scatterer1/L1/LeadFoil/HLX 	= 6.25 cm 
d:Ge/Scatterer1/L1/LeadFoil/HLY 	= 2.5 cm
d:Ge/Scatterer1/L1/LeadFoil/HLZ 	= 0.274 cm
d:Ge/Scatterer1/L1/LeadFoil/TransX	= 0 cm
d:Ge/Scatterer1/L1/LeadFoil/TransY	= Ge/Scatterer1/RotationCenterY + 3.925 cm
d:Ge/Scatterer1/L1/LeadFoil/TransZ	= 1.476 cm
d:Ge/Scatterer1/L1/LeadFoil/RotX 	= 0. deg
d:Ge/Scatterer1/L1/LeadFoil/RotY 	= 0. deg
d:Ge/Scatterer1/L1/LeadFoil/RotZ 	= 0. deg


# Lollipop 2:
s:Ge/Scatterer1/L2/Type   	= "Group"
s:Ge/Scatterer1/L2/Parent 	= "Scatterer1"
d:Ge/Scatterer1/L2/TransX 	= 0.0 cm
d:Ge/Scatterer1/L2/TransY 	= Ge/Scatterer1/RotationCenterY cm
d:Ge/Scatterer1/L2/TransZ 	= 0.0 cm
d:Ge/Scatterer1/L2/RotX 	= 0. deg
d:Ge/Scatterer1/L2/RotY 	= 0. deg
d:Ge/Scatterer1/L2/RotZ 	= Ge/Scatterer1/Lollipop2 deg

# L2 Lead Foil:
s:Ge/Scatterer1/L2/LexanFoil/Parent	= "Scatterer1/L2"
s:Ge/Scatterer1/L2/LexanFoil/Type  	= "TsBox"
s:Ge/Scatterer1/L2/LexanFoil/Material 	= "Lead"
d:Ge/Scatterer1/L2/LexanFoil/HLX 	= 6.25 cm
d:Ge/Scatterer1/L2/LexanFoil/HLY 	= 2.5 cm
d:Ge/Scatterer1/L2/LexanFoil/HLZ 	= 0.00625 cm
d:Ge/Scatterer1/L2/LexanFoil/TransX	= 0 cm
d:Ge/Scatterer1/L2/LexanFoil/TransY	= Ge/Scatterer1/RotationCenterY + 3.925 cm
d:Ge/Scatterer1/L2/LexanFoil/TransZ	= 1.14375 cm
d:Ge/Scatterer1/L2/LexanFoil/RotX 	= 0. deg
d:Ge/Scatterer1/L2/LexanFoil/RotY 	= 0. deg
d:Ge/Scatterer1/L2/LexanFoil/RotZ 	= 0. deg

# Lollipop 3:
s:Ge/Scatterer1/L3/Type   	= "Group"
s:Ge/Scatterer1/L3/Parent 	= "Scatterer1"
d:Ge/Scatterer1/L3/TransX 	=  0.0 cm
d:Ge/Scatterer1/L3/TransY 	=  Ge/Scatterer1/RotationCenterY cm
d:Ge/Scatterer1/L3/TransZ 	=  0.0 cm
d:Ge/Scatterer1/L3/RotX 	= 0. deg
d:Ge/Scatterer1/L3/RotY 	= 0. deg
d:Ge/Scatterer1/L3/RotZ 	= Ge/Scatterer1/Lollipop3 deg


# L3 Lead Foil:
s:Ge/Scatterer1/L3/LeadFoil/Parent	= "Scatterer1/L3"
s:Ge/Scatterer1/L3/LeadFoil/Type  	= "TsBox"
s:Ge/Scatterer1/L3/LeadFoil/Material 	= "Lead"
d:Ge/Scatterer1/L3/LeadFoil/HLX 	= 6.25 cm 
d:Ge/Scatterer1/L3/LeadFoil/HLY 	= 2.5 cm
d:Ge/Scatterer1/L3/LeadFoil/HLZ 	= 0.025 cm
d:Ge/Scatterer1/L3/LeadFoil/TransX	= 0.0 cm
d:Ge/Scatterer1/L3/LeadFoil/TransY	= Ge/Scatterer1/RotationCenterY + 3.925 cm
d:Ge/Scatterer1/L3/LeadFoil/TransZ	= 0.925 cm
d:Ge/Scatterer1/L3/LeadFoil/RotX 	= 0. deg
d:Ge/Scatterer1/L3/LeadFoil/RotY 	= 0. deg
d:Ge/Scatterer1/L3/LeadFoil/RotZ 	= 0. deg

# Lollipop 4:
s:Ge/Scatterer1/L4/Type   	= "Group"
s:Ge/Scatterer1/L4/Parent 	= "Scatterer1"
d:Ge/Scatterer1/L4/TransX 	=  0.0 cm
d:Ge/Scatterer1/L4/TransY 	=  Ge/Scatterer1/RotationCenterY cm
d:Ge/Scatterer1/L4/TransZ 	=  0.0 cm
d:Ge/Scatterer1/L4/RotX 	= 0. deg
d:Ge/Scatterer1/L4/RotY 	= 0. deg
d:Ge/Scatterer1/L4/RotZ 	= Ge/Scatterer1/Lollipop4 deg

# L4 Lead Foil:
s:Ge/Scatterer1/L4/LeadFoil/Parent	= "Scatterer1/L4"
s:Ge/Scatterer1/L4/LeadFoil/Type  	= "TsBox"
s:Ge/Scatterer1/L4/LeadFoil/Material 	= "Lead"
d:Ge/Scatterer1/L4/LeadFoil/HLX 	= 6.25 cm 
d:Ge/Scatterer1/L4/LeadFoil/HLY 	= 2.5 cm
d:Ge/Scatterer1/L4/LeadFoil/HLZ 	= 0.050 cm
d:Ge/Scatterer1/L4/LeadFoil/TransX	= 0 cm
d:Ge/Scatterer1/L4/LeadFoil/TransY	= Ge/Scatterer1/RotationCenterY + 3.925 cm
d:Ge/Scatterer1/L4/LeadFoil/TransZ	= 0.2 cm
d:Ge/Scatterer1/L4/LeadFoil/RotX 	= 0. deg
d:Ge/Scatterer1/L4/LeadFoil/RotY 	= 0. deg
d:Ge/Scatterer1/L4/LeadFoil/RotZ 	= 0. deg

# Lollipop 5:
s:Ge/Scatterer1/L5/Type   	= "Group"
s:Ge/Scatterer1/L5/Parent 	= "Scatterer1"
d:Ge/Scatterer1/L5/TransX 	=  0.0 cm
d:Ge/Scatterer1/L5/TransY 	=  Ge/Scatterer1/RotationCenterY cm
d:Ge/Scatterer1/L5/TransZ 	=  0.0 cm
d:Ge/Scatterer1/L5/RotX 	= 0. deg
d:Ge/Scatterer1/L5/RotY 	= 0. deg
d:Ge/Scatterer1/L5/RotZ 	= Ge/Scatterer1/Lollipop5 deg

# L5 Lead Foil:
s:Ge/Scatterer1/L5/LeadFoil/Parent	= "Scatterer1/L5"
s:Ge/Scatterer1/L5/LeadFoil/Type  	= "TsBox"
s:Ge/Scatterer1/L5/LeadFoil/Material 	= "Lead"
d:Ge/Scatterer1/L5/LeadFoil/HLX 	= 6.25 cm 
d:Ge/Scatterer1/L5/LeadFoil/HLY 	= 2.5 cm
d:Ge/Scatterer1/L5/LeadFoil/HLZ 	= 0.0125 cm
d:Ge/Scatterer1/L5/LeadFoil/TransX	= 0.0 cm
d:Ge/Scatterer1/L5/LeadFoil/TransY	= Ge/Scatterer1/RotationCenterY + 3.925 cm
d:Ge/Scatterer1/L5/LeadFoil/TransZ	= -0.1625 cm
d:Ge/Scatterer1/L5/LeadFoil/RotX 	= 0. deg
d:Ge/Scatterer1/L5/LeadFoil/RotY 	= 0. deg
d:Ge/Scatterer1/L5/LeadFoil/RotZ 	= 0. deg

# Lollipop 6:
s:Ge/Scatterer1/L6/Type   	= "Group"
s:Ge/Scatterer1/L6/Parent 	= "Scatterer1"
d:Ge/Scatterer1/L6/TransX 	=  0.0 cm
d:Ge/Scatterer1/L6/TransY 	=  Ge/Scatterer1/RotationCenterY cm
d:Ge/Scatterer1/L6/TransZ 	=  0.0 cm
d:Ge/Scatterer1/L6/RotX 	= 0. deg
d:Ge/Scatterer1/L6/RotY 	= 0. deg
d:Ge/Scatterer1/L6/RotZ 	= Ge/Scatterer1/Lollipop6 deg

# L6 Lead Foil:
s:Ge/Scatterer1/L6/LeadFoil/Parent	= "Scatterer1/L6"
s:Ge/Scatterer1/L6/LeadFoil/Type  	= "TsBox"
s:Ge/Scatterer1/L6/LeadFoil/Material 	= "Lead"
d:Ge/Scatterer1/L6/LeadFoil/HLX 	= 6.25 cm 
d:Ge/Scatterer1/L6/LeadFoil/HLY 	= 2.5 cm
d:Ge/Scatterer1/L6/LeadFoil/HLZ 	= 0.003 cm
d:Ge/Scatterer1/L6/LeadFoil/TransX	= 0.0 cm
d:Ge/Scatterer1/L6/LeadFoil/TransY	= Ge/Scatterer1/RotationCenterY + 3.925 cm
d:Ge/Scatterer1/L6/LeadFoil/TransZ	= -0.553 cm
d:Ge/Scatterer1/L6/LeadFoil/RotX 	= 0. deg
d:Ge/Scatterer1/L6/LeadFoil/RotY 	= 0. deg
d:Ge/Scatterer1/L6/LeadFoil/RotZ 	= 0. deg

# Lollipop 7:
s:Ge/Scatterer1/L7/Type   	= "Group"
s:Ge/Scatterer1/L7/Parent 	= "Scatterer1"
d:Ge/Scatterer1/L7/TransX 	=  0.0 cm
d:Ge/Scatterer1/L7/TransY 	=  Ge/Scatterer1/RotationCenterY cm
d:Ge/Scatterer1/L7/TransZ 	=  0.0 cm
d:Ge/Scatterer1/L7/RotX 	= 0. deg
d:Ge/Scatterer1/L7/RotY 	= 0. deg
d:Ge/Scatterer1/L7/RotZ 	= Ge/Scatterer1/Lollipop7 deg

# L7 Lead Foil:
s:Ge/Scatterer1/L7/LeadFoil/Parent	= "Scatterer1/L7"
s:Ge/Scatterer1/L7/LeadFoil/Type  	= "TsBox"
s:Ge/Scatterer1/L7/LeadFoil/Material 	= "Lexan"
d:Ge/Scatterer1/L7/LeadFoil/HLX 	= 6.25 cm 
d:Ge/Scatterer1/L7/LeadFoil/HLY 	= 2.5 cm
d:Ge/Scatterer1/L7/LeadFoil/HLZ 	= 0.1370 cm
d:Ge/Scatterer1/L7/LeadFoil/TransX	= 0.0 cm
d:Ge/Scatterer1/L7/LeadFoil/TransY	= Ge/Scatterer1/RotationCenterY + 3.925 cm
d:Ge/Scatterer1/L7/LeadFoil/TransZ	= -1.387 cm
d:Ge/Scatterer1/L7/LeadFoil/RotX 	= 0. deg
d:Ge/Scatterer1/L7/LeadFoil/RotY 	= 0. deg
d:Ge/Scatterer1/L7/LeadFoil/RotZ 	= 0. deg

# Lollipop 8:
s:Ge/Scatterer1/L8/Type   	= "Group"
s:Ge/Scatterer1/L8/Parent 	= "Scatterer1"
d:Ge/Scatterer1/L8/TransX 	=  0.0 cm
d:Ge/Scatterer1/L8/TransY 	=  Ge/Scatterer1/RotationCenterY cm
d:Ge/Scatterer1/L8/TransZ 	=  0.0 cm
d:Ge/Scatterer1/L8/RotX 	= 0. deg
d:Ge/Scatterer1/L8/RotY 	= 0. deg
d:Ge/Scatterer1/L8/RotZ 	= Ge/Scatterer1/Lollipop8 deg

# L8 Lead Foil:
s:Ge/Scatterer1/L8/LeadFoil/Parent	= "Scatterer1/L8"
s:Ge/Scatterer1/L8/LeadFoil/Type  	= "TsBox"
s:Ge/Scatterer1/L8/LeadFoil/Material 	= "Lexan"
d:Ge/Scatterer1/L8/LeadFoil/HLX 	= 6.25 cm 
d:Ge/Scatterer1/L8/LeadFoil/HLY 	= 2.5 cm
d:Ge/Scatterer1/L8/LeadFoil/HLZ 	= 0.0685 cm
d:Ge/Scatterer1/L8/LeadFoil/TransX	= 0.0 cm
d:Ge/Scatterer1/L8/LeadFoil/TransY	= Ge/Scatterer1/RotationCenterY + 3.925 cm
d:Ge/Scatterer1/L8/LeadFoil/TransZ	= -1.7185 cm
d:Ge/Scatterer1/L8/LeadFoil/RotX 	= 0. deg
d:Ge/Scatterer1/L8/LeadFoil/RotY 	= 0. deg
d:Ge/Scatterer1/L8/LeadFoil/RotZ 	= 0. deg

# Lollipop 9:
s:Ge/Scatterer1/L9/Type   	= "Group"
s:Ge/Scatterer1/L9/Parent 	= "Scatterer1"
d:Ge/Scatterer1/L9/TransX 	=  0.0 cm
d:Ge/Scatterer1/L9/TransY 	=  Ge/Scatterer1/RotationCenterY cm
d:Ge/Scatterer1/L9/TransZ 	=  0.0 cm
d:Ge/Scatterer1/L9/RotX 	= 0. deg
d:Ge/Scatterer1/L9/RotY 	= 0. deg
d:Ge/Scatterer1/L9/RotZ 	= Ge/Scatterer1/Lollipop9 deg

# L9 Lead Foil:
s:Ge/Scatterer1/L9/LeadFoil/Parent	= "Scatterer1/L9"
s:Ge/Scatterer1/L9/LeadFoil/Type  	= "TsBox"
s:Ge/Scatterer1/L9/LeadFoil/Material 	= "Lead"
d:Ge/Scatterer1/L9/LeadFoil/HLX 	= 6.25 cm 
d:Ge/Scatterer1/L9/LeadFoil/HLY 	= 2.5 cm
d:Ge/Scatterer1/L9/LeadFoil/HLZ 	= 0.0015 cm
d:Ge/Scatterer1/L9/LeadFoil/TransX	= 0.0 cm
d:Ge/Scatterer1/L9/LeadFoil/TransY	= Ge/Scatterer1/RotationCenterY + 3.925 cm
d:Ge/Scatterer1/L9/LeadFoil/TransZ	= -2.0515 cm
d:Ge/Scatterer1/L9/LeadFoil/RotX 	= 0. deg
d:Ge/Scatterer1/L9/LeadFoil/RotY 	= 0. deg
d:Ge/Scatterer1/L9/LeadFoil/RotZ 	= 0. deg
