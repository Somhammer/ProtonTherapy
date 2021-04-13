# Physics Sources (Beam)

import src.utils as ut

particle_source_parameters = [
"""s:So/%(name)s/Type = "%(Type)s"\n""",
"""s:So/%(name)s/Component = "%(Component)s"\n""",
"""s:So/%(name)s/BeamParticle = "%(Particle)s"\n""",
"""d:So/%(name)s/BeamEnergy = %(Energy)s\n""",
"""u:So/%(name)s/BeamEnergySpread = %(engSpread)s\n""",
"""s:So/%(name)s/BeamPositionDistribution = "%(posDist)s"\n""",
"""s:So/%(name)s/BeamPositionCutoffShape = "%(posCutoffShape)s"\n""",
"""d:So/%(name)s/BeamPositionCutoffX = %(posCutoffX)s\n""",
"""d:So/%(name)s/BeamPositionCutoffY = %(posCutoffY)s\n""",
"""d:So/%(name)s/BeamPositionSpreadX = %(posSpreadX)s\n""",
"""d:So/%(name)s/BeamPositionSpreadY = %(posSpreadY)s\n""",
"""s:So/%(name)s/BeamAngularDistribution = "%(angDist)s"\n""",
"""d:So/%(name)s/BeamAngularCutoffX = %(angCutoffX)s\n""",
"""d:So/%(name)s/BeamAngularCutoffY = %(angCutoffY)s\n""",
"""d:So/%(name)s/BeamAngularSpreadX = %(angSpreadX)s\n""",
"""d:So/%(name)s/BeamAngularSpreadY = %(angSpreadY)s\n""",
"""i:So/%(name)s/NumberOfHistoriesInRun = %(nHistInRun)s\n""",
"""i:So/%(name)s/NumberOfHistoriesInRandomJob = %(nHistInRandomJob)s\n""",
"""s:So/%(name)s/PhaseSpaceFileName = "%(PSFile)s"\n""",
"""i:So/%(name)s/PhaseSpaceMultipleUse = %(PSMulti)s\n""",
]

beam_variables = {
  "name":"Demo",
  "Component":"BeamPosition",
  "Energy":"{Energy} MeV", "engSpread":"{EnergySpread}",
  "posDist":"Gaussian", "posCutoffShape":"Ellipse",
  "posCutoffX":"0.1 cm", "posCutoffY":"0.1 cm", "posSpreadX":"0.1 cm", "posSpreadY":"0.1 cm",
  "angDist":"Gaussian",
  "angCutoffX":"0.01 deg", "angCutoffY":"0.01 deg", "angSpreadX":"0.01 deg", "angSpreadY":"0.01 deg",
  "nHistInRun":"Tf/BCM_1/Value",
}
beam = ut.make_component(particle_source_parameters, beam_variables)

ps_variables = {
  "name":"Demo",
  "Type":"PhaseSpace", "Component":"World",
  "PSFile":"{PSFile}", "PSMulti":"{PSMulti}"
}
ps = ut.make_component(particle_source_parameters, ps_variables)
