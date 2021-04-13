# Topas Overall Control

import src.utils as ut

control_parameters = [
"""Ts/PauseBeforeSequence = "%(Bool)s"\n""",
"""i:Ts/ShowHistoryConutAtInterval = %(iHistories)s\n""",
"""i:Ts/NumberOfThreads = %(nThreads)s\n""",
"""i:Ts/MaxInteruptedHistories = %(maxHistories)i\n""",
]

control_variables = {
  "Bool":"F", "iHistories":0, "nThreads":"{nNodes}", "maxHistories":100000000
}
control = ut.make_component(control_parameters, control_variables)
