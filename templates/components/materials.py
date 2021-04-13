import src.utils as ut

material_parameters = [
"""sv:Ma/%(name)s/Components = %(nElements)i %(Elements)s\n""",
"""uv:Ma/%(name)s/Fractions = %(nElements)i %(Fractions)s\n""",
"""d:Ma/%(name)s/Density = %(Density)s\n""",
"""s:Ma/%(name)s/State = "%(State)"\n""",
"""d:Ma/%(name)s/Temperature = %(Temperature)s\n""",
"""d:Ma/%(name)s/Pressure = %(Pressure)s\n""",
"""s:Ma/%(name)s/DefaultColor = "%(Color)s"\n""", 
"""i:Ma/%(name)s/AtomicNumber = %(AtomicNumber)i\n""",
"""d:Ma/%(name)s/AtomicMass = %(AtomicMass)s\n""",
"""d:Ma/%(name)s/MeanExcitationEnergy = %(ExEnergy)s\n""",
]

nigas_variables = {
  "name":"NiGas",
  "nElements":1, "Elements":""" "Nitrogen" """, "Fractions":"1.0", "Density":"0.001251 g/cm3"
}

nigas = ut.make_component(material_parameters, nigas_variables)

contour_variables = {
  "name":"Contour{Number}",
  "nElements":2, "Elements":""" "Hydrogen" "Oxygen" """, "Fractions":"0.1119 0.8881", "Density":"{Density} g/cm3",
}
contour = ut.make_component(material_parameters, contour_variables)
