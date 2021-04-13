# Beam simulation for recording phase space

import templates.components.control as ts
import templates.components.timefeatures as tf
import templates.components.geometry as ge
import templates.components.sources as so
import templates.components.scoring as sc

template = """\
includeFile = {path}N01_IC1.tps 
includeFile = {path}N02_FS.tps 
includeFile = {path}N03_RM.tps 
includeFile = {path}N05_SS.tps 
includeFile = {path}N07_IC2.tps 
includeFile = {path}N08_SNT.tps 
includeFile = {path}ConstantForNozzles.tps

Ge/CheckForOverlaps = "t"
Ge/QuitIfOverlapDetected = "F"

""" \
+ ts.control + "\n" \
+ tf.time_feature + "\n" \
+ ge.rmw + "\n" \
+ "{Scatterer1}" \
+ ge.scatterer2 + "\n\n" \
+ ge.snout + "\n" \
+ """Ge/Aperture/InputFile = "{ApertureFile}"\n""" \
+ """Ge/Compensator/InputFile = "{CompensatorFile}"\n\n""" \
+ so.beam + "\n" \
+ sc.ps_at_film
