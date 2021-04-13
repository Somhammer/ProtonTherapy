includeFile = /home/seohyeon/work/ProtonTherapy/data/components/ConstantsForNozzles.tps
#Range modulator
#from Proteus235
################################################
s:Ge/RMW/Type = "TsCylinder"
s:Ge/RMW/Material = "Parent"
s:Ge/RMW/Parent = "Gantry"
d:Ge/RMW/RMin = 0.0 cm
d:Ge/RMW/RMax = 40.2 cm
#d:Ge/RMW/HL = 156.4 mm
d:Ge/RMW/HL = 120 mm
d:Ge/RMW/TransX = 13.0 cm
d:Ge/RMW/TransY = 0 cm
d:Ge/RMW/TransZ = 2551 mm




d:Ge/RMW/Track1 = 0 deg
d:Ge/RMW/Track2 = 26.7898759 deg
d:Ge/RMW/Track3 = 41.1377081 deg
d:Ge/RMW/Track4 = 120 deg
d:Ge/RMW/Track5 = 146.7898759 deg
d:Ge/RMW/Track6 = 161.1377081 deg
d:Ge/RMW/Track7 = 240 deg
d:Ge/RMW/Track8 = 266.7898759 deg
d:Ge/RMW/Track9 = 281.1377081 deg

d:Ge/RMW/Small/Track0 = 0 deg
d:Ge/RMW/Small/Track1 = 57.421029637 deg
d:Ge/RMW/Small/Track2 = 77.282161915 deg

d:Ge/RMW/Track = 240 deg

d:Ge/RMW/RotX = 0 deg
d:Ge/RMW/RotY = 0 deg
d:Ge/RMW/RotZ = Ge/RMW/Track deg
d:Ge/RMW/SPhi = 0 deg
d:Ge/RMW/DPhi = 360 deg


###############################################
#Small wheel 1 (8b)
#track 1 2 3
###############################################
s:Ge/RMW_1/Type = "TsRangeModulator"
s:Ge/RMW_1/Material = "Parent"
s:Ge/RMW_1/Parent = "RMW"
d:Ge/RMW_1/TransX = -21.5 cm
d:Ge/RMW_1/TransY = 0.0 cm
d:Ge/RMW_1/TransZ = 0.0 mm
d:Ge/RMW_1/RotX = 0.0 deg
d:Ge/RMW_1/RotY = 0.0 deg
d:Ge/RMW_1/RotZ = 0.0 deg
b:Ge/RMW_1/Invisible = "TRUE"
b:Ge/RMW_1/PrintInformation = "false"

d:Ge/RMW_1/HeightOfUpper = 147 mm
d:Ge/RMW_1/HeightOfMiddle = 1.0 mm
d:Ge/RMW_1/HeightOfLower = 8.4 mm

d:Ge/RMW_1/Shell/Rin = 16.0 cm
d:Ge/RMW_1/Shell/Rout = 16.3 cm
s:Ge/RMW_1/Shell/Material = "Aluminum"
s:Ge/RMW_1/Shell/Color = "grey"
s:Ge/RMW_1/Shell/DrawingStyle = "Solid"
i:Ge/RMW_1/Shell/VisSegsPerCircle = 360

d:Ge/RMW_1/Hub/Rin = 0.0 cm
d:Ge/RMW_1/Hub/Rout = 7.0 cm
s:Ge/RMW_1/Hub/Material = "Aluminum"
s:Ge/RMW_1/Hub/Color = "grey"
s:Ge/RMW_1/Hub/DrawingStyle = "Solid"
i:Ge/RMW_1/Hub/VisSegsPerCircle = 360

dv:Ge/RMW_1/Upper/RadialDivisions=2 10 13 cm
s:Ge/RMW_1/Upper/Track1/Pattern = "LexanBlockT1"
s:Ge/RMW_1/Upper/Track2/Pattern = "LexanBlockT2"
s:Ge/RMW_1/Upper/Track3/Pattern = "LexanBlockT3"
dv:Ge/RMW_1/Middle/RadialDivisions=1 15 cm
#s:Ge/RMW_1/Middle/Track1/Pattern = "HoleTrackDisk"
s:Ge/RMW_1/Middle/Track1/Pattern = "InterfaceDisk"
s:Ge/RMW_1/Middle/Track2/Pattern = "InterfaceDisk"
dv:Ge/RMW_1/Lower/RadialDivisions=2 10 13 cm
s:Ge/RMW_1/Lower/Track1/Pattern = "LeadBlockT1"
s:Ge/RMW_1/Lower/Track2/Pattern = "LeadBlockT2"
s:Ge/RMW_1/Lower/Track3/Pattern = "LeadBlockT3"


d:Ge/LexanBlockT1/Offset = 0 deg
dv:Ge/LexanBlockT1/Angles = 14
5.000000 114.130000 146.540000 175.660000 197.170000 216.150000 231.940000 246.000000 258.640000 270.600000 282.240000 294.560000 306.170000 324.000000 deg
dv:Ge/LexanBlockT1/Heights = 14
77.717000 82.501000 87.268000 92.017000 96.747000 101.455000 106.142000 110.811000 115.326000 119.494000 123.663000 127.832000 132.003000 65.000000 mm
sv:Ge/LexanBlockT1/Materials=14
"Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Brass" 

dv:Ge/InterfaceDisk/Angles = 1 0.0 deg
dv:Ge/InterfaceDisk/Heights  =1 1.0 mm
sv:Ge/InterfaceDisk/Materials=1 "AlZnMgCu"

dv:Ge/HoleTrackDisk/Angles = 2 90 110 deg
dv:Ge/HoleTrackDisk/Heights  =2 0 1 mm
sv:Ge/HoleTrackDisk/Materials=2 "NULL" "Aluminum"

d:Ge/LeadBlockT1/Offset = 0 deg
dv:Ge/LeadBlockT1/Angles = 9
3.000000 114.130000 146.540000 175.660000 197.170000 216.150000 231.940000 246.000000 257.64 deg
dv:Ge/LeadBlockT1/Heights = 9
0.893000 0.766000 0.642000 0.522000 0.405000 0.291000 0.182000 0.075000 0 mm
sv:Ge/LeadBlockT1/Materials=9
"Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead"

d:Ge/LexanBlockT2/Offset =0 deg
dv:Ge/LexanBlockT2/Angles = 15
33.090000 152.940000 188.220000 217.830000 240.900000 260.150000 276.740000 291.030000 303.820000 315.030000 325.730000 334.440000 344.260000 349.990000 357.060000 deg
dv:Ge/LexanBlockT2/Heights = 15
44.355000 51.476000 58.601000 65.729000 72.858000 79.988000 87.116000 94.242000 101.364000 108.481000 115.590000 122.690000 129.778000 136.853000 65.000000 mm
sv:Ge/LexanBlockT2/Materials=15
"Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Brass" 

d:Ge/LeadBlockT2/Offset = 0 deg
dv:Ge/LeadBlockT2/Angles = 15
31.090000 152.940000 188.220000 217.830000 240.900000 260.150000 276.740000 291.030000 303.820000 315.030000 325.730000 334.440000 344.260000 349.990000 357.06 deg
dv:Ge/LeadBlockT2/Heights = 15
8.395000 8.046000 7.696000 7.345000 6.993000 6.640000 6.288000 5.935000 5.582000 5.230000 4.879000 4.529000 4.181000 3.834000 0 mm
sv:Ge/LeadBlockT2/Materials=15
"Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead"

d:Ge/LexanBlockT3/Offset = 0 deg
dv:Ge/LexanBlockT3/Angles = 22
4.12 37.120000 136.760000 168.870000 194.800000 214.480000 231.460000 246.300000 259.150000 270.430000 280.700000 290.220000 298.980000 307.060000 314.510000 321.450000 327.990000 334.070000 339.920000 345.280000 351.660000 356.830000 deg
dv:Ge/LexanBlockT3/Heights = 22
44.437000 49.485000 54.528000 59.561000 64.587000 69.604000 74.609000 79.602000 84.580000 89.544000 94.488000 99.413000 104.317000 109.196000 114.047000 118.870000 123.671000 128.286000 132.539000 136.793000 141.050000 65 mm
sv:Ge/LexanBlockT3/Materials=22
"Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Brass"

d:Ge/LeadBlockT3/Offset = 0 deg
dv:Ge/LeadBlockT3/Angles = 18
37.120000 136.760000 168.870000 194.800000 214.480000 231.460000 246.300000 259.150000 270.430000 280.700000 290.220000 298.980000 307.060000 314.510000 321.450000 327.990000 334.070000 339.92 deg
dv:Ge/LeadBlockT3/Heights = 18
2.379000 2.218000 2.059000 1.901000 1.745000 1.589000 1.436000 1.285000 1.137000 0.991000 0.848000 0.709000 0.574000 0.443000 0.317000 0.196000 0.079000 0 mm
sv:Ge/LeadBlockT3/Materials=18
"Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead"


###############################################
#Small wheel 2 (6)
#track 4 5 6
###############################################
s:Ge/RMW_2/Type = "TsRangeModulator"
s:Ge/RMW_2/Material = "Parent"
s:Ge/RMW_2/Parent = "RMW"
d:Ge/RMW_2/TransX = 10.75 cm
d:Ge/RMW_2/TransY = 18.6195462 cm
d:Ge/RMW_2/TransZ = 0.0 mm
d:Ge/RMW_2/RotX = 0.0 deg
d:Ge/RMW_2/RotY = 0.0 deg
d:Ge/RMW_2/RotZ = 0.0 deg
b:Ge/RMW_2/Invisible = "TRUE"
b:Ge/RMW_2/PrintInformation = "false"

d:Ge/RMW_2/HeightOfUpper = 147 mm
d:Ge/RMW_2/HeightOfMiddle = 1.0 mm
d:Ge/RMW_2/HeightOfLower = 8.4 mm

d:Ge/RMW_2/Shell/Rin = 16.0 cm
d:Ge/RMW_2/Shell/Rout = 16.3 cm
s:Ge/RMW_2/Shell/Material = "Aluminum"
s:Ge/RMW_2/Shell/Color = "grey"
s:Ge/RMW_2/Shell/DrawingStyle = "Solid"
i:Ge/RMW_2/Shell/VisSegsPerCircle = 360

d:Ge/RMW_2/Hub/Rin = 0.0 cm
d:Ge/RMW_2/Hub/Rout = 7.0 cm
s:Ge/RMW_2/Hub/Material = "Aluminum"
s:Ge/RMW_2/Hub/Color = "grey"
s:Ge/RMW_2/Hub/DrawingStyle = "Solid"
i:Ge/RMW_2/Hub/VisSegsPerCircle = 360

dv:Ge/RMW_2/Upper/RadialDivisions=2 10 13 cm
s:Ge/RMW_2/Upper/Track1/Pattern = "LexanBlockT4"
s:Ge/RMW_2/Upper/Track2/Pattern = "LexanBlockT5"
s:Ge/RMW_2/Upper/Track3/Pattern = "LexanBlockT6"
dv:Ge/RMW_2/Middle/RadialDivisions=1 15 cm
#s:Ge/RMW_2/Middle/Track2/Pattern = "HoleTrackDisk"
s:Ge/RMW_2/Middle/Track1/Pattern = "InterfaceDisk"
s:Ge/RMW_2/Middle/Track2/Pattern = "InterfaceDisk"
dv:Ge/RMW_2/Lower/RadialDivisions=2 10 13 cm
s:Ge/RMW_2/Lower/Track1/Pattern = "LeadBlockT4"
s:Ge/RMW_2/Lower/Track2/Pattern = "LeadBlockT5"
s:Ge/RMW_2/Lower/Track3/Pattern = "LeadBlockT6"


d:Ge/LexanBlockT4/Offset = 8 deg
dv:Ge/LexanBlockT4/Angles = 31
5.00 75.51 101.42 120.91 135.92 149.12 160.53 170.61 179.71 188.42 196.69 204.63 212.15 219.50 226.64 233.34 239.54 245.30 250.99 256.77 262.92 268.90 275.47 282.31 288.99 295.57 302.44 308.99 315.15 320.93 326.33 deg
dv:Ge/LexanBlockT4/Heights = 31
0.71 6.13 11.53 17.19 22.31 27.91 33.03 38.57 43.68 49.14 54.23 59.62 64.67 69.98 75.12 80.18 85.22 90.14 94.94 99.38 104.67 109.29 113.94 118.68 123.30 127.90 132.50 137.10 141.70 146.30 50.00 mm
sv:Ge/LexanBlockT4/Materials=31
"Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "CuZn39Pb3"

d:Ge/LeadBlockT4/Offset = 8 deg
dv:Ge/LeadBlockT4/Angles = 21
3.00 75.51 101.42 120.91 135.92 149.12 160.53 170.61 179.71 188.42 196.69 204.63 212.15 219.50 226.64 233.34 239.54 245.30 250.99 256.77 262.92 deg
dv:Ge/LeadBlockT4/Heights = 21
2.44 2.27 2.11 1.89 1.79 1.59 1.48 1.29 1.19 1.01 0.91 0.75 0.65 0.51 0.40 0.30 0.21 0.15 0.10 0.14 0 mm
sv:Ge/LeadBlockT4/Materials=21
"Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead"

d:Ge/LexanBlockT5/Offset = 4 deg
dv:Ge/LexanBlockT5/Angles = 23
7.09 101.42 132.91 156.78 176.07 191.94 205.98 218.46 229.57 239.87 249.28 258.26 266.74 274.96 282.47 289.87 296.99 303.23 309.22 315.06 320.47 325.66 331.09 deg
dv:Ge/LexanBlockT5/Heights = 23
1.06 7.91 15.20 21.64 28.87 35.31 42.09 49.18 55.62 62.62 69.03 75.94 82.54 89.13 95.67 102.35 108.83 115.24 121.65 127.41 133.17 138.93 50.00 mm
sv:Ge/LexanBlockT5/Materials=23
"Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "CuZn39Pb3"

d:Ge/LeadBlockT5/Offset = 4 deg
dv:Ge/LeadBlockT5/Angles = 19
5.09 101.42 132.91 156.78 176.07 191.94 205.98 218.46 229.57 239.87 249.28 258.26 266.74 274.96 282.47 289.87 296.99 303.23 309.22 deg
dv:Ge/LeadBlockT5/Heights = 19
3.17 2.97 2.69 2.56 2.29 2.16 1.97 1.72 1.60 1.36 1.24 1.02 0.87 0.71 0.56 0.38 0.25 0.12 0 mm
sv:Ge/LeadBlockT5/Materials=19
"Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead"

d:Ge/LexanBlockT6/Offset = -4 deg
dv:Ge/LexanBlockT6/Angles = 21
4.12 113.00 150.23 177.46 198.72 216.27 231.15 243.80 255.18 265.33 274.29 282.50 289.81 296.52 302.56 308.18 313.35 318.18 322.71 327.02 331.12 deg
dv:Ge/LexanBlockT6/Heights = 21
1.08 8.56 16.03 23.53 30.96 38.35 46.19 53.13 60.44 68.12 75.04 82.60 89.78 97.19 104.05 111.35 118.37 125.38 132.33 139.43 50.00 mm
sv:Ge/LexanBlockT6/Materials=21
"Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "CuZn39Pb3"

d:Ge/LeadBlockT6/Offset = -4 deg
dv:Ge/LeadBlockT6/Angles = 20
2.12 113 150.23 177.46 198.72 216.27 231.15 243.8 255.18 265.33 274.29 285.5 289.81 296.52 302.56 308.18 313.35 318.18 322.71 327.02 deg
dv:Ge/LeadBlockT6/Heights = 20
4.25 3.99 3.74 3.47 3.22 2.97 2.64 2.49 2.26 1.95 1.80 1.52 1.32 1.07 0.93 0.70 0.52 0.35 0.19 0 mm
sv:Ge/LeadBlockT6/Materials=20
"Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead"


###############################################
#Small wheel 3 (5c)
#track 7 8 9
###############################################
s:Ge/RMW_3/Type = "TsRangeModulator"
s:Ge/RMW_3/Material = "Parent"
s:Ge/RMW_3/Parent = "RMW"
d:Ge/RMW_3/TransX = 10.75 cm
d:Ge/RMW_3/TransY = -18.6195462 cm
d:Ge/RMW_3/TransZ = 0.0 mm
d:Ge/RMW_3/RotX = 0.0 deg
d:Ge/RMW_3/RotY = 0.0 deg
d:Ge/RMW_3/RotZ = 0.0 deg
b:Ge/RMW_3/Invisible = "TRUE"
b:Ge/RMW_3/PrintInformation = "false"

d:Ge/RMW_3/HeightOfUpper = 147 mm
d:Ge/RMW_3/HeightOfMiddle = 1.0 mm
d:Ge/RMW_3/HeightOfLower = 8.4 mm

d:Ge/RMW_3/Shell/Rin = 16.0 cm
d:Ge/RMW_3/Shell/Rout = 16.3 cm
s:Ge/RMW_3/Shell/Material = "Aluminum"
s:Ge/RMW_3/Shell/Color = "grey"
s:Ge/RMW_3/Shell/DrawingStyle = "Solid"
i:Ge/RMW_3/Shell/VisSegsPerCircle = 360

d:Ge/RMW_3/Hub/Rin = 0.0 cm
d:Ge/RMW_3/Hub/Rout = 7.0 cm
s:Ge/RMW_3/Hub/Material = "Aluminum"
s:Ge/RMW_3/Hub/Color = "grey"
s:Ge/RMW_3/Hub/DrawingStyle = "Solid"
i:Ge/RMW_3/Hub/VisSegsPerCircle = 360

dv:Ge/RMW_3/Upper/RadialDivisions=2 10 13 cm
s:Ge/RMW_3/Upper/Track1/Pattern = "LexanBlockT7"
s:Ge/RMW_3/Upper/Track2/Pattern = "LexanBlockT8"
s:Ge/RMW_3/Upper/Track3/Pattern = "LexanBlockT9"
dv:Ge/RMW_3/Middle/RadialDivisions=1 15 cm
s:Ge/RMW_3/Middle/Track1/Pattern = "InterfaceDisk"
s:Ge/RMW_3/Middle/Track2/Pattern = "InterfaceDisk"
dv:Ge/RMW_3/Lower/RadialDivisions=2 10 13 cm
s:Ge/RMW_3/Lower/Track1/Pattern = "LeadBlockT7"
s:Ge/RMW_3/Lower/Track2/Pattern = "LeadBlockT8"
s:Ge/RMW_3/Lower/Track3/Pattern = "LeadBlockT9"


d:Ge/LexanBlockT7/Offset = 0 deg
dv:Ge/LexanBlockT7/Angles = 14
5 65.04 86.86 104.56 119.66 133.34 147.09 161.26 176.37 193.79 224.68 256.72 289.72 324.00 deg
dv:Ge/LexanBlockT7/Heights = 14
23.18 27.46 31.74 36.02 40.30 44.58 48.86 53.14 57.43 61.74 66.21 70.20 74.32 65.00 mm
sv:Ge/LexanBlockT7/Materials=14
"C" "C" "C" "C" "C" "C" "C" "C" "C" "C" "C" "C" "C" "Brass"

d:Ge/LeadBlockT7/Offset = 0 deg
dv:Ge/LeadBlockT7/Angles = 11
3.00 65.04 86.86 104.56 119.66 133.34 147.09 161.26 176.37 193.76 224.65 deg
dv:Ge/LeadBlockT7/Heights = 11
1.63 1.51 1.39 1.26 1.14 1.02 0.90 0.78 0.67 0.55 0 mm
sv:Ge/LeadBlockT7/Materials=11
"Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead"

d:Ge/LexanBlockT8/Offset = 4 deg
dv:Ge/LexanBlockT8/Angles = 25
106.64 137.76 166.39 186.19 202.84 216.46 228.24 238.21 247.06 254.82 261.63 267.79 273.18 277.98 282.59 287.10 291.60 296.08 300.49 304.96 309.40 313.85 318.39 323.09 354.09 deg
dv:Ge/LexanBlockT8/Heights = 25
5.17 10.41 15.62 20.85 26.01 31.18 36.36 41.51 46.65 51.75 56.87 61.97 67.08 71.84 76.28 80.73 85.17 89.61 94.05 98.50 102.94 107.39 111.84 65.00 0 mm
sv:Ge/LexanBlockT8/Materials=25
"C" "C" "C" "C" "C" "C" "C" "C" "C" "C" "C" "C" "C" "C" "C" "C" "C" "C" "C" "C" "C" "C" "C" "C" "Brass"

d:Ge/LeadBlockT8/Offset = 4 deg
dv:Ge/LeadBlockT8/Angles = 15
106.64 137.76 166.39 186.19 202.84 216.46 228.24 238.21 247.06 254.82 261.63 267.79 273.18 277.98 352.09 deg
dv:Ge/LeadBlockT8/Heights = 15
2.53 2.31 2.09 1.87 1.67 1.46 1.25 1.05 0.85 0.66 0.47 0.29 0.09 0 2.74 mm
sv:Ge/LeadBlockT8/Materials=15
"Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" 

d:Ge/LexanBlockT9/Offset = 0 deg
dv:Ge/LexanBlockT9/Angles = 22
37.120000 136.760000 168.870000 194.800000 214.480000 231.460000 246.300000 259.150000 270.430000 280.700000 290.220000 298.980000 307.060000 314.510000 321.450000 327.990000 334.070000 339.920000 345.280000 351.660000 356.830000 364.12 deg
#4.12
dv:Ge/LexanBlockT9/Heights = 22
44.437000 49.485000 54.528000 59.561000 64.587000 69.604000 74.609000 79.602000 84.580000 89.544000 94.488000 99.413000 104.317000 109.196000 114.047000 118.870000 123.671000 128.286000 132.539000 136.793000 141.050000 65 mm
#65
sv:Ge/LexanBlockT9/Materials=22
"Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan" "Lexan"

d:Ge/LeadBlockT9/Offset = 0 deg
dv:Ge/LeadBlockT9/Angles = 17
37.120000 136.760000 168.870000 194.800000 214.480000 231.460000 246.300000 259.150000 270.430000 280.700000 290.220000 298.980000 307.060000 314.510000 321.450000 327.990000 334.070000 deg
dv:Ge/LeadBlockT9/Heights = 17
2.379000 2.218000 2.059000 1.901000 1.745000 1.589000 1.436000 1.285000 1.137000 0.991000 0.848000 0.709000 0.574000 0.443000 0.317000 0.196000 0.079000 mm
sv:Ge/LeadBlockT9/Materials=17
"Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead" "Lead"

