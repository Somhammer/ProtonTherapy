import os, sys
import pandas as pd
import pydicom as dicom

import src.variables as var

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

def readBCM(bcm_name):
    import openpyxl as xl
    wb = xl.load_workbook(os.path.join(var.BASE_PATH, 'data', 'BCM.xlsx'), data_only=True)
    bcm_sheet = wb['BCM']
    bwt = []
    bcm = []
       
    for cell in bcm_sheet['A']:
        if cell.row == 1: continue
        if cell.value == None: break
        bwt.append(cell.value)

    col = ''
    for cell in bcm_sheet[1]:
        if cell.value == bcm_name:
            col = xl.utils.cell.get_column_letter(cell.column)
            break
    if col == '': 
        return bcm, bwt
        
    for cell in bcm_sheet[col]:
        if cell.row == 1: continue
        if cell.value == None: break
        bcm.append(cell.value)
    return bcm, bwt