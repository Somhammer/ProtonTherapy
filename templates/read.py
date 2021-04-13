# Read phase-space file

import templates.components.control as ts
import templates.components.materials as ma
import templates.components.sources as so
import templates.components.geometry as ge
import templates.components.scoring as sc
import templates.components.physics as ph

template = """\
includeFile = {path}HUtoMatrialSchneider_{manu}.tps

""" \
+ ts.control + "\n" \
+ ma.nigas + "\n" \
+ ge.world + "\n" \
+ so.ps + "\n" \
+ ge.box + "\n" \
+ ge.patient + "\n" \
+ sc.dose_at_phantom + "\n" \
+ ph.physics_for_reading + "\n"
