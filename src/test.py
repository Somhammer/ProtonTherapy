act_list = [
  ('File', 
    (('New', 'New Simulation', 'Ctrl+N'),
     ('Open', 'Open Simulation Configuration File'),
     ('Save', 'Save Simulation Configuration File'),
     ('Export',
       (('Melona', 'MELONA'),
        ('Orange', 'ORANGE'),
        ('Kiwi', 'KIWI'))
     ))
  ),
  ('Component',
    (('New', 'New Component', 'Ctrl+C'),
     ('Load', 'Load Component', 'Ctrl+L'),
     ('Modify', 'Modify Component', 'Ctrl+M'),
     ('Save', 'Save Component', 'Ctrl+A'))
  ),
  ('Patient',
    (('Setup', 'Set Patient Dicom Directory'),
     ('View', 'View Patient CT Image'))
  ),
  ('Simulation', 'Topas simulation'),
]

def read_tuple(tuple, mother = None):
    for item in tuple:
        if str(type(item[-1])) == "<class 'tuple'>":
            for i in item[-1]:
                if mother is not None:
                    print(str(mother)+'--'+item[0]+'--'+i[0])
                else:
                    print(item[0] + '--' +i[0])
            read_tuple(item[-1], mother=item[0])
        else:
            continue

class MyApp(QtWidgets.QMainWindow):

read_tuple(act_list)
