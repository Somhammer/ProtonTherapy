import os, sys
import inspect
import ast

class Proton():
    def __init__(self):
        self.base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        sys.path.append(self.base_path)
        self.module = None

    def load(self, module):
        module = module.replace('.py','')
        module = module.split('/')[-1]
        try:
            del sys.modules[module]
        except BaseException as err:
            pass
        try:
            import importlib
            self.module = importlib.import_module('src.'+module)
        except BaseException as err:
            serr = str(err)
            print("Error to load the module src/" + module + ": " + serr)
    
    def name(self, fname):
        f = open(fname,'r')
        line = '\n'.join(i for i in f.readlines())
        p = ast.parse(line)
        return [node.name for node in ast.walk(p) if isinstance(node, ast.ClassDef)][0]

    def process(self, name = None):
        if name is not None:
            instance = eval('self.module.'+name)
        else:
            clsmembers = inspect.getmembers(self.module, inspect.isclass)
            for cls in clsmembers:
                instance = eval('self.module.'+cls[0])
                loc = inspect.getfile(instance)
                if self.base_path in loc:
                    break
        return instance

class Topas():
    def __init__(self):
        self.base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        sys.path.append(self.base_path)

    def run(self, script):
        if str(type(script)) == "<class '_io.TextIOWrapper'>":
            script = script.readlines()

        import subprocess
        def call_subprocess(cmd):
            cmd = cmd.split(' ')
            print(cmd)
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            print(out.decode('utf-8'))
            print(err.decode('utf-8'))
        
        if str(type(script)) == "<class 'list'>" and len(script) > 1:
            split_idx = [0]
            for i in range(len(script)):
                tmp = script[i].replace('\n','')
                tmp = tmp.replace(' ', '')
                tmp = tmp.replace('\t', '')
                if tmp == '': split_idx.append(i)
            split_idx.append(len(script))

            commands = []
            for i in range(len(split_idx)):
                if i + 1 == len(split_idx): break
                commands.append(script[split_idx[i]:split_idx[i+1]])

            import multiprocessing as mp
            for cmds in commands:
                for item in cmds:
                    print(item)
                    proc = mp.Process(target=call_subprocess, args=(item,))
                    proc.start()
                for item in cmds:
                    proc.join()
        elif str(type(script)) == "<class 'list'>" and len(script) == 1:
            call_subprocess(script[0])
        else:
            call_subprocess(script)
