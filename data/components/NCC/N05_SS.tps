includeFile = /home/seohyeon/work/ProtonTherapy/data/components/ConstantsForNozzles.tps
# Second Scatterer: 
##################################################
s:Ge/Scatterer2/Type   		= "Group"
s:Ge/Scatterer2/Parent 		= "Gantry"
d:Ge/Scatterer2/TransX 		=  0.0 cm
d:Ge/Scatterer2/TransY 		=  0.0 cm
d:Ge/Scatterer2/TransZ 		= 1630 mm
d:Ge/Scatterer2/RotX 		= 0. deg
d:Ge/Scatterer2/RotY 		= 0. deg
d:Ge/Scatterer2/RotZ 		= 0. deg
s:Ge/Scatterer2/Message 	= "Constructing IBA TsScatterer2"

# Scatterer 2 Brass Box (Mother Volume)
s:Ge/Scatterer2/BrassBox/Parent		= "Scatterer2"
s:Ge/Scatterer2/BrassBox/Type  		= "TsCylinder"
s:Ge/Scatterer2/BrassBox/Material	= "Brass"
d:Ge/Scatterer2/BrassBox/RMin 		= 0.0 cm 
d:Ge/Scatterer2/BrassBox/RMax 		= 21.8 cm
d:Ge/Scatterer2/BrassBox/HL 		=  3.0 cm
d:Ge/Scatterer2/BrassBox/TransX		= -13.0 cm
d:Ge/Scatterer2/BrassBox/TransY		=  0.0 cm
d:Ge/Scatterer2/BrassBox/TransZ		=  0.0 cm
d:Ge/Scatterer2/BrassBox/RotX 		=  0. deg
d:Ge/Scatterer2/BrassBox/RotY 		=  0. deg
d:Ge/Scatterer2/BrassBox/RotZ 		=  0. deg
d:Ge/Scatterer2/BrassBox/SPhi 		=  0. deg
d:Ge/Scatterer2/BrassBox/DPhi 		=  360. deg

# Scatter Holder Group:
s:Ge/Scatterer2/Holder/Type   		= "Group"
s:Ge/Scatterer2/Holder/Parent 		= "Scatterer2/BrassBox"
d:Ge/Scatterer2/Holder/TransX 		=  0.0 cm
d:Ge/Scatterer2/Holder/TransY 		=  0.0 cm
d:Ge/Scatterer2/Holder/TransZ 		=  0.0 cm
d:Ge/Scatterer2/Holder/RotX 		= 0. deg
d:Ge/Scatterer2/Holder/RotY 		= 0. deg
d:Ge/Scatterer2/Holder/RotZ 		= 0. deg

# Setting up the rotations for selecting a scatterer, this can be made Gantry specific:
d:Ge/Scatterer2/RotZForS1 		=   0. deg
d:Ge/Scatterer2/RotZForS8 		=  90. deg
d:Ge/Scatterer2/RotZForS2 		= 180. deg
d:Ge/Scatterer2/RotZForS3 		= 270. deg

# Scatter Hole 1
s:Ge/Scatterer2/Hole1/Type   		= "Group"
s:Ge/Scatterer2/Hole1/Parent 		= "Scatterer2/Holder"
d:Ge/Scatterer2/Hole1/TransX 		= 13.0 cm
d:Ge/Scatterer2/Hole1/TransY 		= 0.0 cm
d:Ge/Scatterer2/Hole1/TransZ 		= 0.0 cm
d:Ge/Scatterer2/Hole1/RotX 		= 0. deg
d:Ge/Scatterer2/Hole1/RotY 		= 0. deg
d:Ge/Scatterer2/Hole1/RotZ 		= 0. deg

# Scatter Hole 2
s:Ge/Scatterer2/Hole2/Type   		= "Group"
s:Ge/Scatterer2/Hole2/Parent 		= "Scatterer2/Holder"
d:Ge/Scatterer2/Hole2/TransX 		= 0.0 cm
d:Ge/Scatterer2/Hole2/TransY 		= 13.0 cm
d:Ge/Scatterer2/Hole2/TransZ 		= 0.0 cm
d:Ge/Scatterer2/Hole2/RotX 		= 0. deg
d:Ge/Scatterer2/Hole2/RotY 		= 0. deg
d:Ge/Scatterer2/Hole2/RotZ 		= 0. deg

# Scatter Hole 3
s:Ge/Scatterer2/Hole3/Type   		= "Group"
s:Ge/Scatterer2/Hole3/Parent 		= "Scatterer2/Holder"
d:Ge/Scatterer2/Hole3/TransX 		= -13.0 cm
d:Ge/Scatterer2/Hole3/TransY 		= 0.0 cm
d:Ge/Scatterer2/Hole3/TransZ 		= 0.0 cm
d:Ge/Scatterer2/Hole3/RotX 		= 0. deg
d:Ge/Scatterer2/Hole3/RotY 		= 0. deg
d:Ge/Scatterer2/Hole3/RotZ 		= 0. deg

# Scatter Hole 4
s:Ge/Scatterer2/Hole4/Type   		= "Group"
s:Ge/Scatterer2/Hole4/Parent 		= "Scatterer2/Holder"
d:Ge/Scatterer2/Hole4/TransX 		= 0.0 cm
d:Ge/Scatterer2/Hole4/TransY 		= -13.0 cm
d:Ge/Scatterer2/Hole4/TransZ 		= 0.0 cm
d:Ge/Scatterer2/Hole4/RotX 		= 0. deg
d:Ge/Scatterer2/Hole4/RotY 		= 0. deg
d:Ge/Scatterer2/Hole4/RotZ 		= 0. deg

##########################################################
# S1 -> Hole
##########################################################

# Scatterer 1 (no scattering)
# Air Tube:  (no scattering, for pencil beam etc)
s:Ge/Scatterer2/S1/Parent 		= "Scatterer2/Hole1"
s:Ge/Scatterer2/S1/Type 		= "TsCylinder"
s:Ge/Scatterer2/S1/Material 		= "World"
d:Ge/Scatterer2/S1/RMin 		=  0.0 cm
d:Ge/Scatterer2/S1/RMax 		=  8.0 cm
d:Ge/Scatterer2/S1/HL   		=  3.0 cm
d:Ge/Scatterer2/S1/TransX 		=  0.0 cm
d:Ge/Scatterer2/S1/TransY 		=  0.0 cm
d:Ge/Scatterer2/S1/TransZ 		=  0.0 cm
d:Ge/Scatterer2/S1/RotX 		=  0.0 deg
d:Ge/Scatterer2/S1/RotY 		=  0.0 deg
d:Ge/Scatterer2/S1/RotZ 		=  0.0 deg
d:Ge/Scatterer2/S1/SPhi 		=  0.0 deg
d:Ge/Scatterer2/S1/DPhi 		=  360.0 deg

##########################################################
# S8
##########################################################

# Scatterer 2 (example second scatterer)
# Air Hole for Scatterer 2:
s:Ge/Scatterer2/S8/Parent 		= "Scatterer2/Hole2"
s:Ge/Scatterer2/S8/Type 		= "TsCylinder"
s:Ge/Scatterer2/S8/Material 		= "World"
d:Ge/Scatterer2/S8/RMin 		=  0.0 cm
d:Ge/Scatterer2/S8/RMax 		=  8.0 cm
d:Ge/Scatterer2/S8/HL   		=  3.0 cm
d:Ge/Scatterer2/S8/TransX 		=  0.0 cm
d:Ge/Scatterer2/S8/TransY 		=  0.0 cm
d:Ge/Scatterer2/S8/TransZ 		=  0.0 cm
d:Ge/Scatterer2/S8/RotX 		=  0.0 deg
d:Ge/Scatterer2/S8/RotY 		=  0.0 deg
d:Ge/Scatterer2/S8/RotZ 		=  0.0 deg
d:Ge/Scatterer2/S8/SPhi 		=  0.0 deg
d:Ge/Scatterer2/S8/DPhi 		=  360.0 deg
 
# Lexan Polycone Scatterer2:
s:Ge/Scatterer2/S8/LexanPolycone/Parent 	= "Scatterer2/S8"
s:Ge/Scatterer2/S8/LexanPolycone/Type 		= "G4HPolycone"
s:Ge/Scatterer2/S8/LexanPolycone/Material 	= "Lexan"
dv:Ge/Scatterer2/S8/LexanPolycone/RInner 	= 59 0	0	1	2	3	4	5	6	7	8	9	10	11	12	13	14	15	16	17	18	19	20	21	22	23	24	25	26	27	28	29	30	31	32	33	34	35	36	37	38	39	40	41	42	43	44	45	46	47	48	49	50	51	52	53	54	55	56	57 mm
dv:Ge/Scatterer2/S8/LexanPolycone/ROuter 	= 59 80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80 mm
dv:Ge/Scatterer2/S8/LexanPolycone/Z      	= 59 0	37.5000000000000	37.5100000000000	37.5500000000000	37.6300000000000	37.7200000000000	37.8500000000000	37.9900000000000	38.1700000000000	38.3600000000000	38.5800000000000	38.8200000000000	39.0800000000000	39.3600000000000	39.6500000000000	39.9700000000000	40.2900000000000	40.6400000000000	40.9900000000000	41.3600000000000	41.7400000000000	42.1300000000000	42.5200000000000	42.9300000000000	43.3400000000000	43.7500000000000	44.1700000000000	44.5900000000000	45.0100000000000	45.4400000000000	45.8700000000000	46.2900000000000	46.7200000000000	47.1500000000000	47.5700000000000	47.9800000000000	48.3900000000000	48.7900000000000	49.1900000000000	49.5800000000000	49.9500000000000	50.3200000000000	50.6800000000000	51.0300000000000	51.3700000000000	51.7000000000000	52.0100000000000	52.3200000000000	52.6100000000000	52.9000000000000	53.1700000000000	53.4400000000000	53.6300000000000	53.7300000000000	53.8100000000000	53.8900000000000	53.9500000000000	54.0100000000000	54.0400000000000 mm
d:Ge/Scatterer2/S8/LexanPolycone/TransX 	=  0.0 cm
d:Ge/Scatterer2/S8/LexanPolycone/TransY 	=  0.0 cm
d:Ge/Scatterer2/S8/LexanPolycone/TransZ 	=  -2.595 cm
d:Ge/Scatterer2/S8/LexanPolycone/RotX 		=  0.0 deg
d:Ge/Scatterer2/S8/LexanPolycone/RotY 		=  0.0 deg
d:Ge/Scatterer2/S8/LexanPolycone/RotZ 		=  0.0 deg
d:Ge/Scatterer2/S8/LexanPolycone/PhiStart 	=  0.0 deg
d:Ge/Scatterer2/S8/LexanPolycone/PhiTotal 	=  360.0 deg

# Lead Polycone Scatterer2:
s:Ge/Scatterer2/S8/LeadPolycone/Parent 	= "Scatterer2/S8"
s:Ge/Scatterer2/S8/LeadPolycone/Type 		= "G4HPolycone"
s:Ge/Scatterer2/S8/LeadPolycone/Material 	= "Lead"
dv:Ge/Scatterer2/S8/LeadPolycone/RInner 	= 57 0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0 mm
dv:Ge/Scatterer2/S8/LeadPolycone/ROuter 	= 57 57	56	55	54	53	52	51	50	49	48	47	46	45	44	43	42	41	40	39	38	37	36	35	34	33	32	31	30	29	28	27	26	25	24	23	22	21	20	19	18	17	16	15	14	13	12	11	10	9	8	7	6	5	4	3	2	1 mm
dv:Ge/Scatterer2/S8/LeadPolycone/Z      	= 57 0	-0.510000000000000	-0.520000000000000	-0.530000000000000	-0.550000000000000	-0.570000000000000	-0.590000000000000	-0.620000000000000	-0.680000000000000	-0.740000000000000	-0.800000000000000	-0.860000000000000	-0.920000000000000	-0.990000000000000	-1.06000000000000	-1.13000000000000	-1.20000000000000	-1.28000000000000	-1.36000000000000	-1.44000000000000	-1.52000000000000	-1.60000000000000	-1.69000000000000	-1.77000000000000	-1.86000000000000	-1.95000000000000	-2.03000000000000	-2.12000000000000	-2.21000000000000	-2.30000000000000	-2.39000000000000	-2.48000000000000	-2.57000000000000	-2.66000000000000	-2.74000000000000	-2.83000000000000	-2.91000000000000	-3	-3.08000000000000	-3.16000000000000	-3.23000000000000	-3.31000000000000	-3.38000000000000	-3.45000000000000	-3.51000000000000	-3.57000000000000	-3.63000000000000	-3.68000000000000	-3.73000000000000	-3.78000000000000	-3.82000000000000	-3.86000000000000	-3.89000000000000	-3.91000000000000	-3.93000000000000	-3.95000000000000	-3.96000000000000 mm
d:Ge/Scatterer2/S8/LeadPolycone/TransX 	=  0.0 cm
d:Ge/Scatterer2/S8/LeadPolycone/TransY 	=  0.0 cm
d:Ge/Scatterer2/S8/LeadPolycone/TransZ 	=  -2.595 cm
d:Ge/Scatterer2/S8/LeadPolycone/RotX 		=  0.0 deg
d:Ge/Scatterer2/S8/LeadPolycone/RotY 		=  0.0 deg
d:Ge/Scatterer2/S8/LeadPolycone/RotZ 		=  0.0 deg
d:Ge/Scatterer2/S8/LeadPolycone/PhiStart 	=  0.0 deg
d:Ge/Scatterer2/S8/LeadPolycone/PhiTotal 	= 360.0 deg

##########################################################
# S2
##########################################################

s:Ge/Scatterer2/S2/Parent 		= "Scatterer2/Hole3"
s:Ge/Scatterer2/S2/Type 		= "TsCylinder"
s:Ge/Scatterer2/S2/Material 		= "World"
d:Ge/Scatterer2/S2/RMin 		=  0.0 cm
d:Ge/Scatterer2/S2/RMax 		=  8.0 cm
d:Ge/Scatterer2/S2/HL   		=  3.0 cm
d:Ge/Scatterer2/S2/TransX 		=  0.0 cm
d:Ge/Scatterer2/S2/TransY 		=  0.0 cm
d:Ge/Scatterer2/S2/TransZ 		=  0.0 cm
d:Ge/Scatterer2/S2/RotX 		=  0.0 deg
d:Ge/Scatterer2/S2/RotY 		=  0.0 deg
d:Ge/Scatterer2/S2/RotZ 		=  0.0 deg
d:Ge/Scatterer2/S2/SPhi 		=  0.0 deg
d:Ge/Scatterer2/S2/DPhi 		=  360.0 deg
 
# Lexan Polycone Scatterer2:
s:Ge/Scatterer2/S2/LexanPolycone/Parent 	= "Scatterer2/S2"
s:Ge/Scatterer2/S2/LexanPolycone/Type 		= "G4HPolycone"
s:Ge/Scatterer2/S2/LexanPolycone/Material 	= "Lexan"
dv:Ge/Scatterer2/S2/LexanPolycone/RInner 	= 6 75.00 	76.00 	77.00 	78.00 	79.00 	80.00 mm
dv:Ge/Scatterer2/S2/LexanPolycone/ROuter 	= 6 80.00 	80.00 	80.00 	80.00 	80.00 	80.00 mm
dv:Ge/Scatterer2/S2/LexanPolycone/Z      	= 6 28.26 	28.27 	28.30 	28.36 	28.44 	28.57 mm
d:Ge/Scatterer2/S2/LexanPolycone/TransX 	=  0.0 cm
d:Ge/Scatterer2/S2/LexanPolycone/TransY 	=  0.0 cm
d:Ge/Scatterer2/S2/LexanPolycone/TransZ 	=  0.0 cm
d:Ge/Scatterer2/S2/LexanPolycone/RotX 		=  0.0 deg
d:Ge/Scatterer2/S2/LexanPolycone/RotY 		=  0.0 deg
d:Ge/Scatterer2/S2/LexanPolycone/RotZ 		=  0.0 deg
d:Ge/Scatterer2/S2/LexanPolycone/PhiStart 	=  0.0 deg
d:Ge/Scatterer2/S2/LexanPolycone/PhiTotal 	=  360.0 deg

# Lexan Polycone2 Scatterer2:
s:Ge/Scatterer2/S2/LexanPolycone2/Parent 	= "Scatterer2/S2"
s:Ge/Scatterer2/S2/LexanPolycone2/Type 		= "G4HPolycone"
s:Ge/Scatterer2/S2/LexanPolycone2/Material 	= "Lexan"
dv:Ge/Scatterer2/S2/LexanPolycone2/RInner 	= 75 0.00 	1.00 	2.00 	3.00 	4.00 	5.00 	6.00 	7.00 	8.00 	9.00 	10.00 	11.00 	12.00 	13.00 	14.00 	15.00 	16.00 	17.00 	18.00 	19.00 	20.00 	21.00 	22.00 	23.00 	24.00 	25.00 	26.00 	27.00 	28.00 	29.00 	30.00 	31.00 	32.00 	33.00 	34.00 	35.00 	36.00 	37.00 	38.00 	39.00 	40.00 	41.00 	42.00 	43.00 	43.06 	43.13 	43.25 	43.41 	43.66 	43.94 	44.00 	44.28 	44.62 	45.00 	45.04 	45.54 	46.00 	46.09 	47.18 	47.00 	47.24 	47.94 	48.00 	48.59 	49.00 	49.42 	50.00 	50.25 	51.00 	51.17 	52.00 	52.25 	53.00 	53.50 	54.00 mm
dv:Ge/Scatterer2/S2/LexanPolycone2/ROuter 	= 75 80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	74.00 	73.00 	72.00 	71.00 	70.00 	69.80 	69.00 	68.00 	67.08 	67.00 	66.00 	65.08 	65.00 	64.00 	63.33 	63.00 	62.00 	61.91 	61.00 	60.56 	60.00 	59.22 	59.00 	58.14 	58.00 	57.17 	57.00 	56.25 	56.00 	55.00 mm
dv:Ge/Scatterer2/S2/LexanPolycone2/Z      	= 75 0.00 	0.03 	0.13 	0.30 	0.54 	0.84 	1.20 	1.62 	2.09 	2.62 	3.20 	3.83 	4.50 	5.21 	5.97 	6.75 	7.57 	8.42 	9.29 	10.19 	11.10 	12.03 	12.97 	13.92 	14.86 	15.81 	16.76 	17.69 	18.61 	19.51 	20.37 	21.20 	22.00 	22.76 	23.49 	24.19 	24.84 	25.45 	26.02 	26.55 	27.04 	27.47 	27.88 	28.24 	28.26 	28.28 	28.32 	28.37 	28.45 	28.54 	28.56 	28.64 	28.74 	28.85 	28.86 	28.98 	29.09 	29.10 	29.22 	29.30 	29.34 	29.46 	29.47 	29.57 	29.61 	29.66 	29.73 	29.75 	29.81 	29.82 	29.87 	29.88 	29.91 	29.92 	29.93 mm
d:Ge/Scatterer2/S2/LexanPolycone2/TransX 	=  0.0 cm
d:Ge/Scatterer2/S2/LexanPolycone2/TransY 	=  0.0 cm
d:Ge/Scatterer2/S2/LexanPolycone2/TransZ 	=  0.0 cm
d:Ge/Scatterer2/S2/LexanPolycone2/RotX 		=  0.0 deg
d:Ge/Scatterer2/S2/LexanPolycone2/RotY 		=  0.0 deg
d:Ge/Scatterer2/S2/LexanPolycone2/RotZ 		=  0.0 deg
d:Ge/Scatterer2/S2/LexanPolycone2/PhiStart 	=  0.0 deg
d:Ge/Scatterer2/S2/LexanPolycone2/PhiTotal 	=  360.0 deg

# Lead Polycone Scatterer2:
s:Ge/Scatterer2/S2/LeadPolycone/Parent 	= "Scatterer2/S2"
s:Ge/Scatterer2/S2/LeadPolycone/Type 		= "G4HPolycone"
s:Ge/Scatterer2/S2/LeadPolycone/Material 	= "Lead"
dv:Ge/Scatterer2/S2/LeadPolycone/RInner 	= 55 0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 mm
dv:Ge/Scatterer2/S2/LeadPolycone/ROuter 	= 55 80.00 	80.00 	52.00 	51.00 	50.00 	49.00 	48.00 	47.00 	46.00 	45.00 	44.00 	43.00 	42.00 	41.00 	40.00 	39.00 	38.00 	37.00 	36.00 	35.00 	34.00 	33.00 	32.00 	31.00 	30.00 	29.00 	28.00 	27.00 	26.00 	25.00 	24.00 	23.00 	22.00 	21.00 	20.00 	19.00 	18.00 	17.00 	16.00 	15.00 	14.00 	13.00 	12.00 	11.00 	10.00 	9.00 	8.00 	7.00 	6.00 	5.00 	4.00 	3.00 	2.00 	1.00 	0.00 mm
dv:Ge/Scatterer2/S2/LeadPolycone/Z      	= 55 0.00 	-0.20 	-0.21 	-0.22 	-0.24 	-0.26 	-0.29 	-0.32 	-0.37 	-0.41 	-0.47 	-0.54 	-0.61 	-0.69 	-0.78 	-0.88 	-0.99 	-1.10 	-1.23 	-1.36 	-1.50 	-1.65 	-1.80 	-1.96 	-2.13 	-2.30 	-2.48 	-2.67 	-2.86 	-3.05 	-3.24 	-3.43 	-3.62 	-3.81 	-4.00 	-4.18 	-4.37 	-4.54 	-4.71 	-4.88 	-5.04 	-5.19 	-5.33 	-5.47 	-5.59 	-5.71 	-5.82 	-5.91 	-6.00 	-6.07 	-6.13 	-6.18 	-6.21 	-6.23 	-6.24 mm
d:Ge/Scatterer2/S2/LeadPolycone/TransX 	=  0.0 cm
d:Ge/Scatterer2/S2/LeadPolycone/TransY 	=  0.0 cm
d:Ge/Scatterer2/S2/LeadPolycone/TransZ 	=  0.0 cm
d:Ge/Scatterer2/S2/LeadPolycone/RotX 		=  0.0 deg
d:Ge/Scatterer2/S2/LeadPolycone/RotY 		=  0.0 deg
d:Ge/Scatterer2/S2/LeadPolycone/RotZ 		=  0.0 deg
d:Ge/Scatterer2/S2/LeadPolycone/PhiStart 	=  0.0 deg
d:Ge/Scatterer2/S2/LeadPolycone/PhiTotal 	= 360.0 deg

# Lead Polycone Scatterer2:
s:Ge/Scatterer2/S2/LeadPolycone2/Parent 	= "Scatterer2/S2"
s:Ge/Scatterer2/S2/LeadPolycone2/Type 		= "G4HPolycone"
s:Ge/Scatterer2/S2/LeadPolycone2/Material 	= "Lead"
dv:Ge/Scatterer2/S2/LeadPolycone2/RInner 	= 20 56.00 	57.00 	58.00 	59.00 	60.00 	61.00 	62.00 	63.00 	64.00 	65.00 	66.00 	67.00 	68.00 	69.00 	69.50 	70.00 	71.00 	72.00 	73.00 	74.00 mm
dv:Ge/Scatterer2/S2/LeadPolycone2/ROuter 	= 20 80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	80.00 	79.40 	78.20 	77.60 	77.00 	77.00 mm
dv:Ge/Scatterer2/S2/LeadPolycone2/Z      	= 20 -0.20 	-0.21 	-0.22 	-0.23 	-0.25 	-0.27 	-0.29 	-0.31 	-0.34 	-0.36 	-0.39 	-0.41 	-0.44 	-0.46 	-0.47 	-0.48 	-0.50 	-0.51 	-0.52 	-0.53 mm
d:Ge/Scatterer2/S2/LeadPolycone2/TransX 	=  0.0 cm
d:Ge/Scatterer2/S2/LeadPolycone2/TransY 	=  0.0 cm
d:Ge/Scatterer2/S2/LeadPolycone2/TransZ 	=  0.0 cm
d:Ge/Scatterer2/S2/LeadPolycone2/RotX 		=  0.0 deg
d:Ge/Scatterer2/S2/LeadPolycone2/RotY 		=  0.0 deg
d:Ge/Scatterer2/S2/LeadPolycone2/RotZ 		=  0.0 deg
d:Ge/Scatterer2/S2/LeadPolycone2/PhiStart 	=  0.0 deg
d:Ge/Scatterer2/S2/LeadPolycone2/PhiTotal 	= 360.0 deg

##########################################################
# S3
##########################################################

s:Ge/Scatterer2/S3/Parent 		= "Scatterer2/Hole4"
s:Ge/Scatterer2/S3/Type 		= "TsCylinder"
s:Ge/Scatterer2/S3/Material 		= "World"
d:Ge/Scatterer2/S3/RMin 		=  0.0 cm
d:Ge/Scatterer2/S3/RMax 		=  8.0 cm
d:Ge/Scatterer2/S3/HL   		=  3.0 cm
d:Ge/Scatterer2/S3/TransX 		=  0.0 cm
d:Ge/Scatterer2/S3/TransY 		=  0.0 cm
d:Ge/Scatterer2/S3/TransZ 		=  0.0 cm
d:Ge/Scatterer2/S3/RotX 		=  0.0 deg
d:Ge/Scatterer2/S3/RotY 		=  0.0 deg
d:Ge/Scatterer2/S3/RotZ 		=  0.0 deg
d:Ge/Scatterer2/S3/SPhi 		=  0.0 deg
d:Ge/Scatterer2/S3/DPhi 		=  360.0 deg
 
# Lexan Polycone Scatterer2:
s:Ge/Scatterer2/S3/LexanPolycone/Parent 	= "Scatterer2/S3"
s:Ge/Scatterer2/S3/LexanPolycone/Type 		= "G4HPolycone"
s:Ge/Scatterer2/S3/LexanPolycone/Material 	= "Lexan"
dv:Ge/Scatterer2/S3/LexanPolycone/RInner 	= 36 0	0	1	2	3	4	5	6	7	8	9	10	11	12	13	14	15	16	17	18	19	20	21	22	23	24	25	26	27	28	29	30	31	75	75	76 mm
dv:Ge/Scatterer2/S3/LexanPolycone/ROuter 	= 36 80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80	80 mm
dv:Ge/Scatterer2/S3/LexanPolycone/Z      	= 36 0	1.26	1.34	1.47	1.62	1.79	1.97	2.14	2.32	2.51	2.71	2.93	3.12	3.37	3.6	3.8	4.01	4.3	4.58	4.8	5.01	5.26	5.45	5.66	5.88	6.07	6.22	6.34	6.45	6.57	6.67	6.75	7.02	7.02	19.5	20 mm
d:Ge/Scatterer2/S3/LexanPolycone/TransX 	=  0.0 cm
d:Ge/Scatterer2/S3/LexanPolycone/TransY 	=  0.0 cm
d:Ge/Scatterer2/S3/LexanPolycone/TransZ 	=  0.9 cm
d:Ge/Scatterer2/S3/LexanPolycone/RotX 		=  0.0 deg
d:Ge/Scatterer2/S3/LexanPolycone/RotY 		=  0.0 deg
d:Ge/Scatterer2/S3/LexanPolycone/RotZ 		=  0.0 deg
d:Ge/Scatterer2/S3/LexanPolycone/PhiStart 	=  0.0 deg
d:Ge/Scatterer2/S3/LexanPolycone/PhiTotal 	=  360.0 deg

# Lead Polycone Scatterer2:
s:Ge/Scatterer2/S3/LeadPolycone/Parent 	= "Scatterer2/S3"
s:Ge/Scatterer2/S3/LeadPolycone/Type 		= "G4HPolycone"
s:Ge/Scatterer2/S3/LeadPolycone/Material 	= "Lead"
dv:Ge/Scatterer2/S3/LeadPolycone/RInner 	= 32 0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0 mm
dv:Ge/Scatterer2/S3/LeadPolycone/ROuter 	= 32 31	30	29	28	27	26	25	24	23	22	21	20	19	18	17	16	15	14	13	12	11	10	9	8	7	6	5	4	3	2	1	0 mm
dv:Ge/Scatterer2/S3/LeadPolycone/Z      	= 32 0	-0.05	-0.07	-0.09	-0.11	-0.13	-0.16	-0.19	-0.22	-0.27	-0.31	-0.35	-0.4	-0.44	-0.49	-0.54	-0.6	-0.64	-0.68	-0.73	-0.78	-0.81	-0.86	-0.9	-0.94	-0.97	-1.01	-1.04	-1.08	-1.11	-1.13	-1.15 mm
d:Ge/Scatterer2/S3/LeadPolycone/TransX 	=  0.0 cm
d:Ge/Scatterer2/S3/LeadPolycone/TransY 	=  0.0 cm
d:Ge/Scatterer2/S3/LeadPolycone/TransZ 	=  0.9 cm
d:Ge/Scatterer2/S3/LeadPolycone/RotX 		=  0.0 deg
d:Ge/Scatterer2/S3/LeadPolycone/RotY 		=  0.0 deg
d:Ge/Scatterer2/S3/LeadPolycone/RotZ 		=  0.0 deg
d:Ge/Scatterer2/S3/LeadPolycone/PhiStart 	=  0.0 deg
d:Ge/Scatterer2/S3/LeadPolycone/PhiTotal 	= 360.0 deg

