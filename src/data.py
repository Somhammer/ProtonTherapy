import os
import re
from enum import Enum
from dataclasses import dataclass, fields
from copy import copy 

#import variables as var
type_dict = {"d":"Dimensioned double", "u":"Unitless double", "i":"Integer", "b":"Boolean", "s":"String",
             "dv":"Dimensioned double vector", "uv":"Unitless double vector", "iv":"Integer vector", "bv":"Boolean vector", "sv":"String vector"}
directory_dict = {"Ma":"Materials", "El":"Elements", "Is":"Isotopes", "Ge":"Geometry Components", "So":"Particle Sources", "Ph":"Physics",
                  "Vr":"Variance Reduction", "Sc":"Scoring", "Gr":"Graphics", "Tf":"Time Features", "Ts":"Topas overall control"}
si_prefix_dict = {'Y':'yota', 'Z':'zeta', 'E':'exa', 'P':'peta', 'T':'tera', 'G':'giga', 'M':'mega', 
                'k':'kilo', 'h':'hecto', 'da':'deca', 'd':'deci', 'c':'centi', 'm':'milli', 'u':'micro',
                'n':'nano', 'p':'pico', 'f':'femto', 'a':'atto', 'z':'zepto', 'y':'yocto'}
si_unit_dict = {'m':'meter', 'g':'gram', 's':'second', 'A':'ampere', 'K':'kelvin', 
                'mol':'mole', 'cd':'candela', 'Hz':'herz', 'N':'newton', 'Pa':'pascal', 
                'J':'joule', 'W':'watt', 'C':'coulomb', 'V':'volt', 'F':'farad', 'ohm':'ohm', 
                'S':'siemens', 'Wb':'weber', 'T':'tesla', 'H':'henry', 'lm':'lumen', 'lx':'lux', 
                'Bq':'becquerel', 'Gy':'gray', 'Sv':'sievert', 'rad':'radian', 'deg':'degree'}

def enum_init(self, abbriviation, description):
    self.abbriviation = abbriviation
    self.description = description

def enum_str(self):
    return self.name

Type = Enum("Type", {k: (k, v) for k, v in type_dict.items()})
Type.__init__ = enum_init
Type.__str__ = enum_str

Directory = Enum("Directory", {k: (k, v) for k, v in directory_dict.items()})
Directory.__init__ = enum_init
Directory.__str__ = enum_str

SiPrefix = Enum("SiPrefix", {k: (k, v) for k, v in si_prefix_dict.items()})
SiPrefix.__init__ = enum_init
SiPrefix.__str__ = enum_str

SiUnit = Enum("SiUnit", {k: (k, v) for k, v in si_unit_dict.items()})
SiUnit.__init__ = enum_init
SiUnit.__str__ = enum_str

@dataclass
class Unit:
    prefix: SiPrefix = None
    unit: SiUnit = None

    def __str__(self):
        if self.prefix is None:
            return f'{self.unit}'
        elif self.unit is None:
            return ''
        else:
            return f'{self.prefix}{self.unit}'
        
@dataclass(order=True)
class Parameter:
    type: Type
    directory: Directory
    unit: Unit = None
    parent: str = None
    name: str = None
    value: str = None

    def compare(self, other):
        if other.__class__ is self.__class__:
            return (self.type, self.directory, self.unit, self.parent, self.name, self.value) == (other.type, other.directory, other.unit, other.parent, other.name, other.value)
        elif any(i == str(type(other)) for i in ["<class 'tuple'>", "<class 'list'>"]):
            return (str(self.type), str(self.directory), str(self.unit), str(self.parent), str(self.name), str(self.value)) == (str(other[0]), str(other[1]), str(other[2]), str(other[3]), str(other[4]), str(other[5]))
        return NotImplemented

class Component():
    def __init__(self, file_name='NewFile', component_name='NewComponent'):
        self.file_name = file_name
        self.imported = list()
        self.parameters = {component_name:[]} # {myname:parameters}
        self.family_relations = {component_name:None} # child:parent

    def get_family_tree(self, myname):
        family_tree = myname
        parent = self.family_relations[myname]

        while parent != None:
            family_tree = f'{parent}/{family_tree}'
            parent = self.family_relations[parent]
        
        return family_tree

    def add_family(self, parent_name, child_name):
        if not child_name in self.parameters.keys():
            self.parameters[child_name] = []
            if not child_name in self.family_relations.keys():
                self.family_relations[child_name] = parent_name

    def add_parameter(self, para_dict):
        tmp = {k: None for k in [f.name for f in fields(Parameter)]}
        tmp['myname'] = ""
        tmp.update(para_dict)
        para_dict = tmp
        
        for name, parameters in self.parameters.items():
            if name != para_dict['myname']: continue
            for parameter in parameters:
                list_for_comparison = [para_dict['type'], para_dict['directory'], para_dict['unit'], para_dict['parent'], para_dict['name'], para_dict['value']]
                exist_flag = parameter.compare(list_for_comparison)
                if exist_flag: return

        if para_dict['unit'] is not None:
            for si_unit in si_unit_dict.keys():
                if si_unit in para_dict['unit']:
                    postfix = si_unit
                    last_index = para_dict['unit'].rfind(si_unit)  # 문자열의 마지막 인덱스 찾기
                    if last_index != -1:  # 문자열에서 찾은 문자열이 있으면
                        prefix = para_dict['unit'][:last_index]
                    else:
                        prefix = ''
            prefix.strip()
            if prefix != '':
                unit = Unit(prefix=SiPrefix[prefix], unit=SiUnit[postfix])
            else:
                unit = Unit(unit=SiUnit[postfix])
        else:
            unit = None

        if para_dict['type'] is None:
            parameter = Parameter(type=None, directory=Directory[para_dict['directory']],
                                  unit=unit, name=para_dict['name'], value=para_dict['value'])
        else:
            parameter = Parameter(type=Type[para_dict['type']], directory=Directory[para_dict['directory']],
                                  unit=unit, name=para_dict['name'], value=para_dict['value'])
        if para_dict['myname'] in self.family_relations.keys():
            parameter.parent = self.family_relations[para_dict['myname']]        
        
        self.parameters[para_dict['myname']].append(parameter)
    
    def modify_parmeter(self, para_dict):
        tmp = {k: None for k in [f.name for f in fields(Parameter)]}
        tmp['myname'] = ""
        tmp.update(para_dict)
        para_dict = tmp

        for name, parameters in self.parameters.items():
            if name != para_dict['myname']: continue
            for parameter in parameters:
                list_for_comparison = [para_dict['type'], para_dict['directory'], para_dict['unit'], para_dict['parent'], para_dict['name'], parameter.value]
                exist_flag = parameter.compare(list_for_comparison)
                if exist_flag:
                    parameter.value = para_dict['value']

    def delete_parameter(self, para_dict):
        tmp = {k: None for k in [f.name for f in fields(Parameter)]}
        tmp['myname'] = ""
        tmp.update(para_dict)
        para_dict = tmp
        
        for name, parameters in self.parameters.items():
            if name != para_dict['myname']: continue
            for idx, parameter in enumerate(parameters):
                list_for_comparison = [para_dict['type'], para_dict['directory'], para_dict['unit'], para_dict['parent'], para_dict['name'], para_dict['value']]
                exist_flag = parameter.compare(list_for_comparison)
                if exist_flag:
                    parameters.pop(idx)

    def apply_value_from_extern(self, values):
            for parameters in self.parameters.values():
                for parameter in parameters:
                    pattern = r"\{([^\{\}]+)\}"
                    name_keys = re.findall(pattern, parameter.name)
                    value_keys = re.findall(pattern, parameter.value)
                    for key in name_keys:
                        parameter.name = parameter.name.replace("{"+key+"}", str(values[key]))
                    for key in value_keys:
                        parameter.value = parameter.value.replace("{"+key+"}", str(values[key]))

    def convert_parameter_to_str(self, myname, parameter):
        family_tree = self.get_family_tree(myname)
        if parameter.type is None:
            text = f"{parameter.directory}/{family_tree}/{parameter.name} = {parameter.value}"
        else:
            text = f"{parameter.type}:{parameter.directory}/{family_tree}/{parameter.name} = {parameter.value}"
        if parameter.unit is not None:
            text = text + f" {parameter.unit}"

        return text

    # TODO
    def get_geometry(self):
        pass

    def get_fulltext(self):
        text = ""
        for item in self.imported:
                text += f"includeFile = {item}\n"
        text += "\n"

        for myname, parameters in self.parameters.items():
            for parameter in parameters:
                text += self.convert_parameter_to_str(myname, parameter) + '\n'
        return text
    
    def get_parameters_from_textfile(self, filename):
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
        except:
            return
        self.file_name, ext = os.path.splitext(os.path.basename(filename))
        self.parameters = {}
        self.family_relations = {}

        for line in lines:
            line = line.replace("\n", "")
            if len(line.replace(" ", "")) < 1 or line[0] == "#" : continue
            para_dict = {k: None for k in [f.name for f in fields(Parameter)]}
            para_dict['myname'] = None
            
            tmp = line.split("=")
            fullname, value = tmp[0], tmp[1]
            fullname = fullname.strip()
            tmp = fullname.split(":")
            mytype = None
            if len(tmp) == 1:
                fullname = tmp[-1]
            else:
                mytype = tmp[0]
                fullname = tmp[-1]

            para_dict['type'] = mytype

            names = fullname.split("/")
            if len(names) < 2: continue
            if len(names) == 2:
                para_dict['directory'] = names[0]
                para_dict['name'] = names[-1]
            elif len(names) == 3:
                para_dict['directory'] = names[0]
                para_dict['myname'] = names[1]
                para_dict['name'] = names[2]
            else:
                para_dict['directory'] = names[0]
                para_dict['parent'] = names[-3]
                para_dict['myname'] = names[-2]
                para_dict['name'] = names[-1]

            value = value.split("#")[0].strip()
            parts = re.split(r'[= ]+', value)
            if 'd' in mytype:
                para_dict['unit'] = parts[-1]
                para_dict['value'] = ' '.join(parts[:-1])
            else:
                para_dict['value'] = ' '.join(parts[:])

            self.add_family(para_dict['parent'], para_dict['myname'])            
            self.add_parameter(para_dict)