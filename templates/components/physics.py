import src.utils as ut

physics_parameters = [
"""s:Ph/ListName = "%(ListName)s"\n""",
"""b:Ph/ListProcesses = "%(ListProc")s"\n""",
"""s:Ph/%(name)s/Type = "%(Type)s"\n""",
"""sv:Ph/%(name)s/Modules = %(nModules)i %(Modules)s\n""",
"""d:Ph/%(name)s/EMRangeMin = %(EMRangeMin)s\n""",
"""d:Ph/%(name)s/EMRangeMax = %(EMRangeMax)s\n""",
]

modules = ["g4em-standard_opt4", "g4decay", "g4h-elastic", "g4h-phy_QGSP_BIC", "g4ion-binarycascade", "g4stopping"]
physics_for_reading_variables = {
  "name":"Default",
  "ListName":"Default",
  "Type":"Geant4_Modular",
  "nModules":len(modules), "Modules":'"'+'" "'.join(m for m in modules)+'"',
  "EMRangeMin":"100 ev", "EMRangeMax":"500 MeV"
}

physics_for_reading = ut.make_component(physics_parameters, physics_for_reading_variables)
