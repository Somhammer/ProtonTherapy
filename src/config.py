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
        self.topas_path = ''
        self.output_path = ''
        self.input = {} # order:file
        sys.path.append(self.base_path)

    def set_path(self, outpath):
        ptext = open(os.path.join(self.base_path,'path.dat'),'r').readlines()[0].replace('\n','')
        self.topas_path = ptext.split('=')[-1]
        self.output_path = outpath

    def set_input(self, idict):
        self.input = idict

    def run(self):
        import subprocess
        def call_subprocess(iname):
            cmd = [self.topas_path, iname]
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            return out.decode('utf-8'), err.decode('utf-8')
        
        for order in self.input.keys():
            iname = self.input[order]
            out, err = call_subprocess(iname)
            outname = iname.split('/')[-1].replace('.tps','')
            ofile = open(os.path.join(self.output_path, outname+'.log'), 'w')
            efile = open(os.path.join(self.output_path, outname+'.err'), 'w')
            ofile.write(out)
            efile.write(err)
            ofile.close()
            efile.close()

        """
        # Update please...
        import multiprocessing as mp
        for cmds in commands:
            for item in cmds:
                proc = mp.Process(target=call_subprocess, args=(item,))
                proc.start()
            for item in cmds:
                proc.join()
        """