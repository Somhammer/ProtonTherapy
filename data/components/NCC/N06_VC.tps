includeFile = /home/seohyeon/work/ProtonTherapy/data/components/NCC/ConstantsForNozzles.tps
s:Ge/VC/Parent = "Gantry"
d:Ge/VC/TransX = 0 mm
d:Ge/VC/TransY = 0 mm
d:Ge/VC/TransZ = 1201 mm
d:Ge/VC/RotX = 0 deg
d:Ge/VC/RotY = 0 deg
d:Ge/VC/RotZ = 0 deg

d:Ge/VC/Xjaw/HVx = 71.5 mm
d:Ge/VC/Yjaw/HVy = 74.5 mm

##############################################################
# VC
# X Jaws
##############################################################

s:Ge/VC/Xjaw/Plus/Type = "TsBox"
s:Ge/VC/Xjaw/Plus/Parent = "VC"
s:Ge/VC/Xjaw/Plus/Material = "Ni"
d:Ge/VC/Xjaw/Plus/HLX         = 90 mm
d:Ge/VC/Xjaw/Plus/HLY         = 150.5 mm
d:Ge/VC/Xjaw/Plus/HLZ         = 2.85 cm

d:Ge/VC/Xjaw/Xposition = Ge/VC/Xjaw/HVx + Ge/VC/Xjaw/Plus/HLX mm


d:Ge/VC/Xjaw/Plus/TransX      = Ge/VC/Xjaw/Xposition mm
d:Ge/VC/Xjaw/Plus/TransY      = 0 cm
d:Ge/VC/Xjaw/Plus/TransZ      = 3.15 cm
d:Ge/VC/Xjaw/Plus/RotX        = 0. deg
d:Ge/VC/Xjaw/Plus/RotY        = 0. deg
d:Ge/VC/Xjaw/Plus/RotZ        = 0. deg

s:Ge/VC/Xjaw/Minus/Type = "TsBox"
s:Ge/VC/Xjaw/Minus/Parent = "VC"
s:Ge/VC/Xjaw/Minus/Material = "Ni"
d:Ge/VC/Xjaw/Minus/HLX         = 90 mm
d:Ge/VC/Xjaw/Minus/HLY         = 150.5 mm
d:Ge/VC/Xjaw/Minus/HLZ         = 2.85 cm
d:Ge/VC/Xjaw/Minus/TransX      = -1 * Ge/VC/Xjaw/Xposition mm
d:Ge/VC/Xjaw/Minus/TransY      = 0 cm
d:Ge/VC/Xjaw/Minus/TransZ      = 3.15 cm
d:Ge/VC/Xjaw/Minus/RotX        = 0. deg
d:Ge/VC/Xjaw/Minus/RotY        = 0. deg
d:Ge/VC/Xjaw/Minus/RotZ        = 0. deg


##############################################################
# VC
# Y Jaws
##############################################################

s:Ge/VC/Yjaw/Plus/Type = "TsBox"
s:Ge/VC/Yjaw/Plus/Parent = "VC"
s:Ge/VC/Yjaw/Plus/Material = "Ni"
d:Ge/VC/Yjaw/Plus/HLX         = 150.5 mm
d:Ge/VC/Yjaw/Plus/HLY         = 90 mm
d:Ge/VC/Yjaw/Plus/HLZ         = 2.85 cm


d:Ge/VC/Yjaw/Yposition = Ge/VC/Yjaw/HVy + Ge/VC/Yjaw/Plus/HLY mm

d:Ge/VC/Yjaw/Plus/TransX      = 0 mm
d:Ge/VC/Yjaw/Plus/TransY      = Ge/VC/Yjaw/Yposition mm
d:Ge/VC/Yjaw/Plus/TransZ      = -3.55 cm
d:Ge/VC/Yjaw/Plus/RotX        = 0. deg
d:Ge/VC/Yjaw/Plus/RotY        = 0. deg
d:Ge/VC/Yjaw/Plus/RotZ        = 0. deg

s:Ge/VC/Yjaw/Minus/Type = "TsBox"
s:Ge/VC/Yjaw/Minus/Parent = "VC"
s:Ge/VC/Yjaw/Minus/Material = "Ni"
d:Ge/VC/Yjaw/Minus/HLX         = 150.5 mm
d:Ge/VC/Yjaw/Minus/HLY         = 90 mm
d:Ge/VC/Yjaw/Minus/HLZ         = 2.85 cm
d:Ge/VC/Yjaw/Minus/TransX      = 0 mm
d:Ge/VC/Yjaw/Minus/TransY      = -1 * Ge/VC/Yjaw/Yposition mm
d:Ge/VC/Yjaw/Minus/TransZ      = -3.55 cm
d:Ge/VC/Yjaw/Minus/RotX        = 0. deg
d:Ge/VC/Yjaw/Minus/RotY        = 0. deg
d:Ge/VC/Yjaw/Minus/RotZ        = 0. deg
