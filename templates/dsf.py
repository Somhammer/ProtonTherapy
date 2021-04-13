# Dose Scale Factor Calculator TOPAS input template

import templates.components.timefeatures as tf
import templates.components.geometry as ge
import templates.components.sources as so
import templates.components.scoring as sc
import templates.components.control as ts

template = """\
includeFile = {path}N01_IC1.tps 
includeFile = {path}N02_FS.tps 
includeFile = {path}N03_RM.tps 
includeFile = {path}N05_SS.tps 
includeFile = {path}N07_IC2.tps 
includeFile = {path}N08_SNT_WO_COM.tps 
includeFile = {path}ConstantsForNozzles.tps

Ge/CheckForOverlaps = "t"
b:Ge/QuitIfOverlapDetected = "F"

""" \
+ ts.control + "\n" \
+ tf.time_feature + "\n" \
+ so.beam + "\n" \
+ ge.rmw + "\n" \
+ "{Scatterer1}\n" \
+ ge.scatterer2 + "\n" \
+ ge.snout + "\n" \
+ ge.aperture + "\n" \
+ ge.water_phantom + "\n" \
+ ge.pdd + "\n" \
+ sc.pdd 
