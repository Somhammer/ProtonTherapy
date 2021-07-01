import os
from dataclasses import dataclass, field
from copy import copy 

class Component():
    @dataclass(order=True)
    class Parameter:
        vtype: str = None
        category: str = None
        directory: str = None
        name: str = None
        value: str = None
        draw: bool = False
        
        def compare(self, other):
            if other.__class__ is self.__class__:
                return (self.vtype, self.category, self.directory, self.name) == (
                    other.vtype, other.category, other.directory, other.name
                )
            elif str(type(other)) == "<class 'tuple'>" or str(type(other)) == "<class 'list'>":
                return (self.vtype, self.category, self.directory, self.name) == (other[0], other[1], other[2], other[3])
            return NotImplemented
        
        def fullname(self):
            fullname = ""
            if self.vtype is not None and self.vtype != "": 
                fullname += f'{self.vtype}:'
            if self.category is not None and self.category != "": 
                fullname += f'{self.category}'
            if self.directory is not None and self.category != "":
                fullname += f'/{self.directory}'
            if self.name is not None and self.name != "":
                fullname += f'/{self.name}'
            return fullname

        def unit(self):
            prefix = { # Name:Prefix
              'yota':'Y', 'zeta':'Z', 'exa':'E', 'peta':'P', 'tera':'T', 'giga':'G', 'mega':'M', 
              'kilo':'k', 'hecto':'h', 'deca':'da', 'deci':'d', 'centi':'c', 'milli':'m',
              'micro':'u', 'nano':'n', 'pico':'p', 'femto':'f', 'atto':'a', 'zepto':'z', 'yocto':'y'
            }
            unit = { # Name:Symbol
              'meter':'m', 'gram':'g', 'second':'s', 'ampere':'A', 'kelvin':'K', 'mole':'mol', 'candela':'cd',
              'herz':'Hz', 'newton':'N', 'pascal':'Pa', 'joule':'J', 'watt':'W', 'coulomb':'C', 'volt':'V',
              'farad':'F', 'ohm':'ohm', 'siemens':'S', 'weber':'Wb', 'tesla':'T', 'henry':'H',
              'lumen':'lm', 'lux':'lx', 'becquerel':'Bq', 'gray':'Gy', 'sievert':'Sv',
              'radian':'rad', 'degree':'deg'
            }

            unit_index = -999

            temp = self.value.split(' ')
            while any('' == i for i in temp):
                temp.remove('')

            for idx, txt in enumerate(temp):
                if any(txt[0] == i for i in prefix.values()):
                    found_prefix = txt[0]
                    found_unit = txt[1:]
                    unit_index = idx
                elif txt[0:1] == prefix['deca']:
                    found_prefix = txt[0:1]
                    found_unit = txt[2:]
                    unit_index = idx
                else:
                    found_prefix = ''
                    found_unit = ''
            if not unit_index < 0: temp.pop(unit_index)
            unitless_value = ' '.join(i for i in temp)

            return unitless_value, found_prefix, found_unit
        
    @dataclass(order=True)
    class SubComponent:
        name: str = None
        parameters: list = field(default_factory=list)
        
    def __init__(self, btype):
        self.base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        self.__outname = None
        self.__name = None
        self.__btype = btype
        self.__ctype = None
        self.__imported = list()
        self.__subcomponent = {'Basis':self.SubComponent(name='Basis')}
    
    @property
    def outname(self):
        return self.__outname

    @outname.setter
    def outname(self, outname):
        self.__outname = outname

    @property     
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        self.__name = name
        
    @property
    def ctype(self):
        return self.__ctype
        
    @ctype.setter
    def ctype(self, ctype):
        self.__ctype = ctype

    @property
    def btype(self):
        return self.__btype

    @btype.setter
    def btype(self, btype):
        self.__btype = btype
        
    @property
    def imported(self):
        return self.__imported
    
    def modify_file(self, name, delete=False):
        if any(name == i for i in self.__imported) and delete:
            self.__imported.remove(name)
        else:
            self.__imported.append(name)
            if len(self.__imported) > 0:
                tmp = set(self.__imported)
                self.__imported = list(tmp)
                self.__imported.sort()
            
    @property
    def subcomponent(self):
        return self.__subcomponent
        
    def modify_subcomponent(self, subname, paras, delete=False):
        exist = self.__subcomponent.get(subname)
        if exist and delete:
            del self.__subcomponent[subname]
            return
        if not exist:
            self.__subcomponent[subname] = self.SubComponent(name=subname)
        self.modify_parameter(subname, paras)

    def modify_name(self, old, new):
        self.name = new
        for sub in self.subcomponent.values():
            for para in sub.parameters:
                para.directory = para.directory.replace(old, new)

    def modify_subname(self, old, new):
        self.__subcomponent[new] = self.__subcomponent.pop(old)
        self.__subcomponent[new].name = new
        for para in self.subcomponent[new].parameters:
            if old in para.directory:
                para.directory = para.directory.replace(old, new)
            else:
                tmp = para.directory.split('/')
                if len(tmp) == 2:
                    para.directory = f'{tmp[0]}/{new}'
                elif len(tmp) >= 3:
                    t = '/'.join(tmp[2:])
                    para.directory = f'{tmp[0]}/{new}/{t}'
        
    def __split_paraname(self, name):
        tmp = name.split(':')
        if len(tmp) < 2:
            vtype = ''
        else:
            vtype = tmp[0]
        tmp = tmp[-1].split('/')
        if len(tmp) < 3:
            category = ''
            directory = '/'.join(i for i in tmp[0:2])
            name = tmp[2]
        else:
            category = tmp[0]
            directory = '/'.join(i for i in tmp[1:-1])
            name = tmp[-1]
        return vtype, category, directory, name

    def modify_parameter(self, subname, paras, delete=False):
        # para should be dictionary {"name":"value"}
        para_list = []
        for key, value in paras.items():
            vtype, category, directory, name = self.__split_paraname(key)
            para_list.append(self.Parameter(vtype=vtype, category=category, directory=directory, name=name, value=value))
            
        for new in para_list:
            if delete:
                try:
                    idx = self.__subcomponent[subname].parameters.index(new)
                    self.__subcomponent[subname].parameters.pop(idx)
                    continue
                except:
                    continue
                
            findit = False
            for old in self.__subcomponent[subname].parameters:
                if new.compare(old):
                    findit = True
                    old.value = new.value
                    break
            if not findit:
                self.__subcomponent[subname].parameters.append(new)
                    
    def modify_paraname(self, subname, old, new):
        old = self.__split_paraname(old)
        new = self.__split_paraname(new)
        for para in self.__subcomponent[subname].parameters:
            if para.compare(old):
                para.vtype = new[0]
                para.category = new[1]
                para.directory = new[2]
                para.name = new[3]
                return
            
    def load(self, fname, load=False, draw_all=False):
        if draw_all: draw=True
        else: draw=False
        isdir = False
        if os.path.isdir(fname):
            isdir = True
            self.name = fname.split('/')[-1]
            self.ctype = fname.split('/')[-1]
        elif os.path.isfile(fname):
            self.name = fname.split('/')[-1].split('.')[0]
            self.ctype = self.name
        elif not load:
            finditem = False
            component_path = os.path.join(self.base_path, 'data/components')
            for directory in os.listdir(component_path):
                if fname == directory: 
                    fname = os.path.join(component_path, directory)
                    finditem = True
                    continue
                for f in os.listdir(os.path.join(component_path, directory)):
                    if fname+'.tps' == f or fname+'.tps' == os.path.join(directory, f):
                        fname = os.path.join(component_path, directory, f)
                        finditem = True
                        continue
            if not finditem:
                return

        paras = {}
        if isdir:
            subs = [i for i in self.component_list()[self.name]]
            for sub in subs:
                f = open(os.path.join(fname, sub+'.tps'),'r')
                lines = f.readlines()
                paras[sub] = [line for line in lines]
        else:
            changed = False
            if not load:
                f = open(fname, 'r')
                lines = f.readlines()
            else:
                lines = fname.split('\n')

            paras['Basis'] = []
            for line in lines:
                tmp = line.split('=')[0].split('/')
                if not changed and len(tmp) >= 3:
                    self.ctype = tmp[1]
                    changed = True
                if len(tmp) >= 4:
                    subname = tmp[2]
                    if not any(i == subname for i in paras.keys()):
                        paras[subname] = []
                else:
                    subname = 'Basis'
                paras[subname].append(line)

        for sub, lines in paras.items():
            if not sub in self.__subcomponent:
                self.__subcomponent[sub] = self.SubComponent(name=sub)
            for line in lines:
                line = line.split('#')[0]
                line = line.replace('\t','').replace('\n', '')
                line = line.split(' ')
                while any('' == i for i in line): line.remove('')
                line = ' '.join(i for i in line)
                if line == '' or line.startswith('#'): continue
                line = line.split(' = ')
                if line[0].startswith('includeFile'):
                    self.modify_file(line[-1])
                    continue

                if ':' in line[0]:
                    tmp = line[0].split(':')
                    vtype = tmp[0]
                    name = tmp[1]
                else:
                    vtype = ''
                    name = line[0]

                tmp = name.split('/')
                if len(tmp) == 1:
                    category = ''
                    directory = ''
                    name = tmp[0].replace('\t','').replace(' ','')
                elif len(tmp) == 2:
                    category = ''
                    directory = tmp[0]
                    name = tmp[1].replace('\t','').replace(' ','')
                else:
                    category = tmp[0]
                    directory = '/'.join(i for i in tmp[1:-1])
                    name = tmp[-1].replace('\t','').replace(' ','')
                value = line[-1]
                        
                self.__subcomponent[sub].parameters.append(self.Parameter(vtype=vtype, category=category, directory=directory, name=name, value=value, draw=draw))

    def component_list(self):
        outdict = {}
        common = {
          'Beam':['Basis','Distribution'],
          'MonitorChamber':['Basis', 'CylinderFrame', 'BoxFrame', 'CylinderLayer', 'BoxLayer'],
        }
        scanning = {
          'Magnet':['ScanningMagnet', 'Quadrupole']
        }
        scattering = {
          'Scatterer':['Basis', 'Scatterer1', 'Lollipop', 'Scatterer2', 'Holder', 'Hole'],
          'RangeModulator':['Basis','SmallWheel'], 
          'VC':['Basis','XJaws', 'YJaws'],
          'Snout':['Basis','BrassBlock', 'BrassCone'],
          'Phantom':['Basis','WaterPhantom','Patient','PDD','DoseAtPhantom'],
          'PhaseSpaceVolume':['PhaseSpaceVolume', 'PhaseSpaceOutput'],
          'Contour':['Material','Parallel','Contour']
        }
        outdict.update(common)
        if self.btype is None: return
        if self.btype.lower() == 'scanning':
            outdict.update(scanning)
        elif self.btype.lower() == 'scattering':
            outdict.update(scattering)

        return outdict

    def find_parameter(self, name):
        for subname, subcomp in self.subcomponent.items():
            for para in subcomp.parameters:
                if name in para.fullname():
                    return para.value

        for fname in self.imported:
            lines = open(fname, 'r').readlines()
            for line in lines:
                line = line.split('#')[0]
                line = line.replace('\t','').replace('\n', '')
                line = line.split(' ')
                while any('' == i for i in line): line.remove('')
                line = ' '.join(i for i in line)
                line = line.split(' = ')

                fullname = line[0]
                value = line[-1]
                if name in fullname:
                    return value

        path = os.path.join(self.base_path,'data/TopasDefaults.tps')
        for line in open(path,'r').readlines():
            line = line.split('=')
            fullname = line[0]
            value = line[-1]
            if name in fullname:
                return value

        return None

    def calculate_value(self, para):
        if 'v' in para.vtype: return
        
        def is_numeric(value):
            if value.isnumeric():
                return True
            elif value[0].isalpha():
                return False
            else:
                is_str = False
                if '-' == value[0]:
                    tmp = value[1:]
                else:
                    tmp = value
                if '.' in tmp:
                    tmp = tmp.split('.')
                    for val in tmp:
                        if val == '': continue
                        if not val.isnumeric(): is_str = True
                if is_str: return False
                else: return True
        
        def is_operator(value):
            operators = ['+', '-', '*']
            if any(value == i for i in operators):
                return True
            else:
                return False

        value, prefix, unit = para.unit()

        final_value = {}
        operators = {}

        temp = value.split(' ')

        if type(temp[0]) == int and temp[0] == len(temp[1:]): return

        for idx, val in enumerate(temp):
            if is_operator(val):
                operators[idx] = val
                continue

            if is_numeric(val):
                final_value[idx] = val
                continue
            else:
                tmp = copy(para)
                tmp.value = self.find_parameter(val)
                if tmp.value is None: print(tmp)
                numeric_value = tmp.value.split(' ')[0]
                if is_numeric(numeric_value):
                    final_value[idx] = numeric_value
                    continue
                elif tmp.value is None:
                    final_value[idx] = 0.0
                    continue
                else:
                    final_value[idx], uselsess = self.calculate_value(tmp)

        value_sum = 0.0

        if len(operators) < 1:
            if 'i' in para.vtype or (not '.' in str(final_value[0])):
                final_value[0] = int(final_value[0])
            else:
                final_value[0] = float(final_value[0])

            return final_value[0], f'{prefix}{unit}'

        first = None
        oper_idx = list(operators.keys())
        oper_idx.sort()
        for idx in oper_idx:
            if first is None:
                first = final_value[idx-1]
            else:
                first = outvalue
            second = final_value[idx+1]

            if 'i' in para.vtype or (not '.' in str(first) and not '.' in str(second)):
                first = int(first)
                second = int(second)
            else:
                first = float(first)
                second = float(second)

            if operators[idx] == '+':
                outvalue = first + second
            elif operators[idx] == '-':
                outvalue = first - second
            elif operators[idx] == '*':
                outvalue = first * second

        return outvalue, f'{prefix}{unit}'

    def fulltext(self):
        text = ""
        for item in self.imported:
                text += f"includeFile = {item}\n"
        text += "\n"
        for subcomp in self.subcomponent.values():
            for para in subcomp.parameters:
                if not para.draw: continue
                text += f'{para.fullname()} = {para.value}\n'
            text += '\n'
        return text

class Patient():
    def __init__(self):
        self.directory = ""
        self.CT = []
        self.RTP = None
        self.RTS = None
        self.RD = None
        self.is_real = None
        
    def patient_setup(self, dirname):
        if dirname == "": return
        self.directory = dirname
        for f in os.listdir(self.directory):
            if not f.endswith('.dcm'): continue
            if f.startswith('RN'):
                self.RTP = f
            elif f.startswith('RS'):
                self.RTS = f
            elif f.startswith('RD'):
                self.RD = f
            else:
                self.CT.append(f)
        self.CT.sort()

    def determine_patient_type(self):
        return