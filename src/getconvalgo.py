import os, sys
import xlwings as xw

class GetParaFromConvAlgo():
    def __init__(self, path, conv):
        self.path = path
        self.conv = conv
        self.fscatterer = None # first scatterer
        self.sscatterer = None # second scatterer
        self.modulator = None # range modulator
        self.stop = None # stop position
        self.energy = None # beam energy
        self.bcm_name = None
        self.bwt = None # beam weigth time
        self.bcm = None # beam current modulation



    def get_data(self):
        wb = xw.Book(os.path.join(self.path, self.conv))
        main = wb.sheets['Summary']
        self.bcm_name = main['C36']

        GetParaFromConvAlgo.fscatterer = []
        for col in range(2,main.ncols):
            if main.row_values(31)[col] == '': break
            if str(type(main.row_values(31)[col])) == "<class 'str'>": continue
            GetParaFromConvAlgo.fscatterer.append(main.row_values(31)[col])
        GetParaFromConvAlgo.sscatterer = main.cell_value(36, 2)
        GetParaFromConvAlgo.modulator = main.cell_value(33, 2)
        GetParaFromConvAlgo.stop = main.cell_value(34, 2)
        GetParaFromConvAlgo.energy = main.cell_value(53, 2)
 
        bcm_sheet = wb['BCM']
       
        GetParaFromConvAlgo.bwt = []
        for row in range(1, bcm_sheet.nrows):
            GetParaFromConvAlgo.bwt.append(bcm_sheet.col_values(0)[row])

        idx = 999
        for col in range(0, bcm_sheet.ncols):
            if bcm_sheet.row_values(0)[col] == bcm:
                idx = col
                break
        
        GetParaFromConvAlgo.bcm = []
        for row in range(1, bcm_sheet.nrows):
            GetParaFromConvAlgo.bcm.append(int(bcm_sheet.col_values(idx)[row]))
    
    def _get_data_by_openpyxl(self):
        import openpyxl as xl
        wb = xl.load_workbook(os.path.join(self.path, self.conv), data_only=True)
        main = wb['Main']
        bcm = main['C36'].value
        GetParaFromConvAlgo.bcm_name = bcm

        GetParaFromConvAlgo.fscatterer = []
        for cell in main[32]:
            if cell.column < 3: continue
            if cell.value == None: break
            if str(type(cell.value)) == "<class 'str'>": continue
            GetParaFromConvAlgo.fscatterer.append(cell.value)
        GetParaFromConvAlgo.sscatterer = main['C37'].value
        GetParaFromConvAlgo.modulator = main['C34'].value
        GetParaFromConvAlgo.stop = main['C35'].value
        GetParaFromConvAlgo.energy = main['C54'].value

        bcm_sheet = wb['BCM']
       
        GetParaFromConvAlgo.bwt = []
        for cell in bcm_sheet['A']:
            if cell.row == 1: continue
            if cell.value == None: break
            GetParaFromConvAlgo.bwt.append(cell.value)

        for cell in bcm_sheet[1]:
            if cell.value == bcm:
                col = xl.utils.cell.get_column_letter(cell.column)
                break
        
        GetParaFromConvAlgo.bcm = []
        for cell in bcm_sheet[col]:
            if cell.row == 1: continue
            if cell.value == None: break
            GetParaFromConvAlgo.bcm.append(cell.value)
