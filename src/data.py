import os
from dataclasses import dataclass, field


class Component():
    @dataclass(order=True)
    class Parameter:
        vtype: str = None
        category: str = None
        directory: str = None
        name: str = None
        value: str = None
        darw: bool = False
        
        def compare(self, other):
            if other.__class__ is self.__class__:
                return (self.vtype, self.category, self.directory, self.name) == (
                    other.vtype, other.category, other.directory, other.name
                )
            elif str(type(other)) == "<class 'tuple'>" or str(type(other)) == "<class 'list'>":
                return (self.vtype, self.category, self.directory, self.name) = (other[0], other[1], other[2], other[3])
            return NotImplemented
        
        def fullname(self):
            fullname = ""
            if vtype is not None and vtype != "": 
                fullname += f'{vtype}:'
            if category is not None and category != "": 
                fullname += f'{category}'
            if directory is not None and category != "":
                fullname += f'/{directory}'
            if name is not None and name != "":
                fullname += f'/{name}'
            return fullname
        
    @dataclass(order=True)
    class SubComponent:
        name: str = None
        parameters: list = field(default_factory=list)
        draw: bool = False
        
    def __init__(self):
        self.__name = None
        self.__ctype = None
        self.__imported = []
        self.__subcomponent = {'Basis':self.SubComponent(name='Basis')}
    
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
    def imported(self):
        return self.__imported
    
    @imported.setter
    def imported(self, name):
        if any(name == i for i in self.__imported): return
        self.__imported.append(name)
        if len(self.__imported) > 0:
            tmp = set(self.__imported)
            self.__imported = list(tmp).sort()
            
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

    def modify_subname(self, old, new):
        self.__subcomponent[new] = self.__subcomponent.pop(old)
        self.__subcomponent[new].name = new
        for para in self.__subcomponent[new].parameters:
            para.directory.replace(old, new)
        
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
        old = self.__split_paraname()
        new = self.__split_paraname()
        for para in self.__subcomponent[subname].parameters:
            if para.compare(old):
                para.vtype = new[0]
                para.category = new[1]
                para.directory = new[2]
                para.name = new[3]
                return
            
    def load(self, fname):
        g_component_list = {
          'MonitorElement':['Basis', 'CylinderFrame', 'BoxFrame', 'CylinderLayer', 'BoxLayer'],
          'Scatterer':['Basis', 'Scatterer1', 'Lollipop', 'Scatterer2', 'Holder', 'Hole'],
          'RangeModulator':['LargeWheel','SmallWheel'], 
          'SMAG':['Basis','Dipole'],
          'VC':['Basis','XJaws', 'YJaws'],
          'Snout':['Basis','BrassBlock', 'BrassCone'],
          'Apperture':['Basis'],
          'Compensator':['Basis'],
          'PhaseSpaceVolume':['Basis'],
          'Contour':['Basis']
        }

        # Load flie
        # Generate sub-components.
        isdir = False
        if os.path.isdir(fname):
            isdir = True
            self.name = fname.split('/')[-1]
        elif os.path.isfile(fname):
            self.name = fname.split('/')[-1].split('.')[0]
        else:
            return
        subs = []
        if isdir:
            
        else:
        path = base_path
        if fname is dir
        else f name is file
        
                maxlen = 1
        for line in lines:
            if line.startswith('#'): continue

            line = line.replace('\t','').replace('\n', '').replace(' ', '')
            if line == '': continue
            line = line.split('=')
            if line[0].startswith("includeFile"):
                self._import_component(line[-1])
                continue
            if maxlen < len(line[0]): maxlen = len(line[0])
            if any(line[0] == i.name for i in self.elements[name]): continue
                
            para = QListWidgetItem(listPara)
            parameter = self.Item()
            parameter.add_parameter(line[0], line[1])
            self.elements[name].append(parameter)
            listPara.setItemWidget(para, parameter)
            listPara.addItem(para)
            para.setSizeHint(parameter.sizeHint())
        index = self.tabComp.addTab(listPara, name)
        return index
        
class Patient():
    def __init__(self):
        self.directory = None
        self.files = []
        
    def patient_setup(self, dirname):
        if dirname = "": return
        self.directory = dirname
        for f in os.listdir(self.directory):
            if not f.endswith('.dcm'): continue
            self.files.append(i)
        self.files.sort()