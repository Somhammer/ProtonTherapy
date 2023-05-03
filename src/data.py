import os
import re
from enum import Enum
from dataclasses import dataclass, fields
from collections import OrderedDict
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
class Variable:
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

@dataclass
class Container:
    nozzle_type: int = None
    fields: OrderedDict = None
    components: OrderedDict = None 
    scorers: OrderedDict = None
    ct_directory: str = None

class Component():
    def __init__(self, filename='NewFile', component_name='NewComponent'):
        self.filename = filename
        self.imported = list()
        self.variables = {component_name:[]} # {myname:variables}
        self.family_relations = {component_name:None} # child:parent

    def get_family_tree(self, myname):
        family_tree = myname
        parent = self.family_relations[myname]

        while parent != None:
            family_tree = f'{parent}/{family_tree}'
            parent = self.family_relations[parent]
        
        return family_tree

    def add_family(self, parent_name, child_name):
        if not child_name in self.variables.keys():
            self.variables[child_name] = []
            if not child_name in self.family_relations.keys():
                self.family_relations[child_name] = parent_name

    def delete_family(self, child_name):
        if child_name in self.variables.keys():
            del self.variables[child_name]
            del self.family_relations[child_name]

    def change_myname(self, myname, newname):
        self.family_relations[newname] = self.family_relations.pop(myname)
        self.variables[newname] = self.variables.pop(myname)

    def add_import_file(self, path):
        if path not in self.imported:
            self.imported.append(path)

    def delete_import_file(self, path):
        if path in self.imported:
            self.imported.remove(path)

    def add_variable(self, vari_dict):
        tmp = {k: None for k in [f.name for f in fields(Variable)]}
        tmp['myname'] = ""
        tmp.update(vari_dict)
        vari_dict = tmp
        
        for name, variables in self.variables.items():
            if name != vari_dict['myname']: continue
            for variable in variables:
                list_for_comparison = [vari_dict['type'], vari_dict['directory'], vari_dict['unit'], vari_dict['parent'], vari_dict['name'], vari_dict['value']]
                exist_flag = variable.compare(list_for_comparison)
                if exist_flag: return

        if vari_dict['unit'] is not None:
            for si_unit in si_unit_dict.keys():
                if si_unit in vari_dict['unit']:
                    postfix = si_unit
                    last_index = vari_dict['unit'].rfind(si_unit)
                    if last_index != -1:
                        prefix = vari_dict['unit'][:last_index]
                    else:
                        prefix = ''
            prefix.strip()
            if prefix != '':
                unit = Unit(prefix=SiPrefix[prefix], unit=SiUnit[postfix])
            else:
                unit = Unit(unit=SiUnit[postfix])
        else:
            unit = None

        if vari_dict['type'] is None:
            variable = Variable(type=None, directory=Directory[vari_dict['directory']],
                                  unit=unit, name=vari_dict['name'], value=vari_dict['value'])
        else:
            variable = Variable(type=Type[vari_dict['type']], directory=Directory[vari_dict['directory']],
                                  unit=unit, name=vari_dict['name'], value=vari_dict['value'])
        if vari_dict['myname'] in self.family_relations.keys():
            variable.parent = self.family_relations[vari_dict['myname']]        
        
        self.variables[vari_dict['myname']].append(variable)
    
    def modify_variable(self, vari_dict):
        tmp = {k: None for k in [f.name for f in fields(Variable)]}
        tmp['myname'] = ""
        tmp.update(vari_dict)
        vari_dict = tmp

        for name, variables in self.variables.items():
            if name != vari_dict['myname']: continue
            for variable in variables:
                list_for_comparison = [vari_dict['type'], vari_dict['directory'], variable.unit, vari_dict['parent'], vari_dict['name'], variable.value]
                exist_flag = variable.compare(list_for_comparison)
                if exist_flag:
                    variable.value = vari_dict['value']

    def delete_variable(self, vari_dict):
        tmp = {k: None for k in [f.name for f in fields(Variable)]}
        tmp['myname'] = ""
        tmp.update(vari_dict)
        vari_dict = tmp
        
        for name, variables in self.variables.items():
            if name != vari_dict['myname']: continue
            for idx, variable in enumerate(variables):
                list_for_comparison = [vari_dict['type'], vari_dict['directory'], vari_dict['unit'], vari_dict['parent'], vari_dict['name'], vari_dict['value']]
                exist_flag = variable.compare(list_for_comparison)
                if exist_flag:
                    variables.pop(idx)

    def apply_value_from_extern(self, values):
            for variables in self.variables.values():
                for variable in variables:
                    pattern = r"\{([^\{\}]+)\}"
                    name_keys = re.findall(pattern, variable.name)
                    value_keys = re.findall(pattern, variable.value)
                    for key in name_keys:
                        variable.name = variable.name.replace("{"+key+"}", str(values[key]))
                    for key in value_keys:
                        variable.value = variable.value.replace("{"+key+"}", str(values[key]))

    def convert_variable_to_str(self, myname, variable):
        family_tree = self.get_family_tree(myname)
        if variable.type is None:
            text = f"{variable.directory}/{family_tree}/{variable.name} = {variable.value}"
        else:
            text = f"{variable.type}:{variable.directory}/{family_tree}/{variable.name} = {variable.value}"
        if variable.unit is not None:
            text = text + f" {variable.unit}"

        return text
    
    def generate_vari_dict_from_str(self, string):
        string = string.replace("\n", "")
        if len(string.replace(" ", "")) < 1 or string[0] == "#" : return
        if "include" in string: return

        vari_dict = {k: None for k in [f.name for f in fields(Variable)]}
        vari_dict['myname'] = None
        
        tmp = string.split("=")
        fullname, value = tmp[0], tmp[1]
        fullname = fullname.strip()
        tmp = fullname.split(":")
        mytype = None
        if len(tmp) == 1:
            fullname = tmp[-1]
        else:
            mytype = tmp[0]
            fullname = tmp[-1]

        vari_dict['type'] = mytype

        names = fullname.split("/")
        if len(names) < 2: return
        if len(names) == 2:
            vari_dict['directory'] = names[0]
            vari_dict['name'] = names[-1]
        elif len(names) == 3:
            vari_dict['directory'] = names[0]
            vari_dict['myname'] = names[1]
            vari_dict['name'] = names[2]
        else:
            vari_dict['directory'] = names[0]
            vari_dict['parent'] = names[-3]
            vari_dict['myname'] = names[-2]
            vari_dict['name'] = names[-1]

        value = value.split("#")[0].strip()
        parts = re.split(r'[= ]+', value)
        if mytype is not None:
            if 'd' in mytype:
                vari_dict['unit'] = parts[-1]
                vari_dict['value'] = ' '.join(parts[:-1])
            else:
                vari_dict['value'] = ' '.join(parts[:])
        else:
            vari_dict['value'] = ' '.join(parts[:])

        return vari_dict

    def add_variable_from_str(self, string):
        vari_dict = self.generate_vari_dict_from_str(string)
        self.add_family(vari_dict['parent'], vari_dict['myname'])            
        self.add_variable(vari_dict)

    def modify_variable_from_str(self, string):
        vari_dict = self.generate_vari_dict_from_str(string)
        self.modify_variable(vari_dict)

    def delete_variable_from_str(self, string):
        vari_dict = self.generate_vari_dict_from_str(string)
        self.delete_variable(vari_dict)

    # TODO
    ### Need to contain geometry structure of subcomponents
    def get_geometry(self):
        ancestor = None
        for child, parent in self.family_relations.items():
            if parent is None:
                ancestor = child
                break

        if ancestor is None: return

        geometry = {'Type':'TsBox','HLX':"0.0 mm",'HLY':"0.0 mm",'HLZ':"0.0 mm",
               'RMin':"0.0 mm",'RMax':"0.0 mm",
               'HL':"0.0 mm", 'SPhi':"0.0 deg", 'DPhi':"0.0 deg",
               'RotX':"0.0 deg",'RotY':"0.0 deg",'RotZ':"0.0 deg",
               'TransX':"0.0 mm",'TransY':"0.0 mm",'TransZ':"0.0 mm"}
        for variable in self.variables[ancestor]:
            for key in geometry.keys():
                if key in variable.name:
                    if variable.unit is not None:
                        geometry[key] = f"{variable.value} {variable.unit}"
                    else:
                        geometry[key] = f"{variable.value}"
                    break
                   
        return geometry

    def get_fulltext(self):
        text = ""
        for item in self.imported:
                text += f"includeFile = {item}\n"
        text += "\n"

        ancestors = {} # rank: names
        writing_order = {} # rank: names
        i = 0
        found_names = []
        while set(found_names) != set(self.variables.keys()):
            if i == 20: break
            if not i in writing_order.keys():
                writing_order[i] = []
                ancestors[i] = []
            for child, parent in self.family_relations.items():
                if child in found_names: 
                    continue
                if i == 0 and parent is None:
                    ancestors[i].append(child)
                    writing_order[i].append(child)
                    found_names.append(child)
                else:
                    if i > 0 and parent in ancestors[i-1]:
                        ancestors[i].append(child)
                        writing_order[i].append(child)
                        found_names.append(child)
            i += 1

        for rank, names in writing_order.items():
            names.sort()
            for myname in names:
                for variable in self.variables[myname]:
                    text += self.convert_variable_to_str(myname, variable) + '\n'
        return text
    
    def get_variables_from_textfile(self, filename, initialize=False):
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
        except:
            return
        self.filename, ext = os.path.splitext(os.path.basename(filename))
        if initialize:
            self.imported = list()
            self.variables = {}
            self.family_relations = {}

        for line in lines:
            line = line.replace("\n", "")
            if len(line.replace(" ", "")) < 1 or line[0] == "#" : continue

            if "include" in line:
                tmp = line.split("=")
                tmp = tmp[-1]
                tmp = tmp.strip()
                self.imported.append(tmp)
                continue

            self.add_variable_from_str(line)