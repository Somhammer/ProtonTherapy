# Time feature parameters

import src.utils as ut

time_feature_parameters = [
"""s:Tf/%(name)s/Function = "%(Function)s"\n""",
"""dv:Tf/%(name)s/Times = %(nSize)i %(Times)s\n""",
"""iv:Tf/%(name)s/Values = %(nSize)i %(Values)s\n""",
"""d:Tf/%(name)s/Rate = %(Rate)s\n""",
"""d:Tf/%(name)s/StartValue = %(StartValue)s\n""",
"""d:Tf/%(name)s/RepetitionInterval = %(Interval)s\n""",
"""i:Tf/Verbosity = %(Verbosity)i\n""",
"""d:Tf/TimelineEnd = %(EndTime)s\n""",
"""i:Tf/NumberOfSequentialTimes = %(nSeqTimes)s\n""",
]

control_variables = {
  "EndTime":"{stop} ms", "nSeqTimes":"{nSequentialTimes}"
}

beam_weight_variables = {
  "name":"BeamWeight",
  "nSize":256, "Times":"{BWT} ms", "Values":"{BCM}"
}

beam_current_variables = {
  "name":"BeamCurrent",
  "Function":"Step", "nSize":1, "Times":"100 ms", "Values":"{nHistory}"
}

RMW_rotation_variables = {
  "name":"RMW_Rotation",
  "Function":"Linear deg", "Rate":"3.6 deg/ms", "StartValue":"Ge/RMW/Track/zero_angle deg", "Interval":"100.0 ms"
}

time_feature = ut.make_component(time_feature_parameters, control_variables) + "\n" + \
               ut.make_component(time_feature_parameters, beam_weight_variables) + "\n" + \
               ut.make_component(time_feature_parameters, beam_current_variables) + "\n" + \
               ut.make_component(time_feature_parameters, RMW_rotation_variables) + "\n" + \
               "i:Tf/BCM_1/Value = Tf/BeamCurrent/Value * Tf/BeamWeight/Value\n"
