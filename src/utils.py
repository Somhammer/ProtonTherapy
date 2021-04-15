import pandas as pd
import pydicom as dicom

def make_component(parameters, variables):
    component = ""
    for para in parameters:
        args = para.split("%")[1:]
        vars = {}
        for key, value in variables.items():
            if any("("+key+")" in i for i in args): vars[key] = value
        if len(args) == len(vars): component += para % vars 
    
    return component

def show_CT(path, CTname):
    CT = dicom.dcmread(os.path.join(path,CTname))

    plt.imshow(CT.pixel_array, cmap=plt.cm.bone)
    plt.show()
