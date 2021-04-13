# Scoring

import src.utils as ut

score_parameters = [
"""s:Sc/%(name)s/Quantity = "%(Quantity)s"\n""",
"""s:Sc/%(name)s/Component = "%(Component)s"\n""",
"""s:Sc/%(name)s/Surface = "%(Surface)s"\n""",
"""b:Sc/%(name)s/OutputToConsole = "%(OutputConsole)s"\n""",
"""s:Sc/%(name)s/OutputType = "%(OutputType)s"\n""",
"""s:Sc/%(name)s/OutputFile = "%(OutputFile)s"\n""",
"""i:Sc/%(name)s/OutputBufferSize = %(OutputBufferSize)s"\n""",
"""s:Sc/%(name)s/OnlyIncludeParticlesGoing  = "%(IncludeGoing)s"\n""",
"""b:Sc/%(name)s/IncludeTOPASTime = "%(TopasTime)s"\n""",
"""b:Sc/%(name)s/IncludeTimeOfFlight = "%(TOF)s"\n""",
"""b:Sc/%(name)s/IncludeRunID   = "%(RunID)s"\n""",
"""b:Sc/%(name)s/IncludeEventID = "%(EventID)s"\n""",
"""b:Sc/%(name)s/IncludeTrackID = "%(TrackID)s"\n""",
"""b:Sc/%(name)s/IncludeParentID = "%(ParentID)s"\n""",
"""b:Sc/%(name)s/IncludeVertexInfo = "%(VertexInfo)s"\n""",
"""b:Sc/%(name)s/IncludeSeed = "%(Seed)s"\n""",
"""sv:Sc/%(name)s/OnlyIncludeParticlesNamed = %(nIncludePtls)d%(IncludePtls)s\n""",
"""s:Sc/%(name)s/IfOutputFileAlreadyExists = "%(ExistentFile)s"\n""",
"""b:Sc/%(name)s/OutputAfterRun = "%(OutputAfterRun)s\n""",
"""u:Sc/%(name)s/DICOMOutputScaleFactor = %(dicomScale)s\n""",
"""b:Sc/%(name)s/DICOMOutput32BitsPerPixel = "%(dicomPixel)s"\n""",
]

ps_at_film_variables = {
  "name":"PhaseSpaceAtVacFilm",
  "Quantity":"PhaseSpace", "Surface":"ZPhaseSpaceVol/ZMinusSurface",
  "OutputConsole":"True", "OutputType":"Binary", "OutputFile":"{output}", "ExistentFile":"Increment",
  "TopasTime":"False", "TOF":"False", "RunID":"False", "EventID":"False", "TrackID":"False",
  "ParentID":"False","VertexInfo":"True","Seed":"False",
  "nIncludePtls":2, "IncludePtls":""" "proton" "neutron" """
}

ps_at_film = ut.make_component(score_parameters, ps_at_film_variables)

dose_at_phantom_variables = {
  "name":"DoseAtPhantom",
  "Component":"Patient",
  "OutputFile":"{output}", "OutputType":"DICOM", "ExistentFile":"Increment",
  "dicomScale":"{Scale}", "dicomPixel":"True"
}

dose_at_phantom = ut.make_component(score_parameters, dose_at_phantom_variables)

pdd_variables = {
  "name":"PDD", "Quantity":"DoseToWater", "Component":"PDD",
  "OutputFile":"{output}", "OutputType":"{outType}",
  "OutputConsole":"False", "ExistentFile":"Overwrite"
}

pdd = ut.make_component(score_parameters, pdd_variables)
