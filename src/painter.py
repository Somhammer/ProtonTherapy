from PySide6.QtWidgets import *
from PySide6.QtGui import *

import src.variables as var

class Painter(QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding
        )
        self.painter = QPainter()
        self.paintEvent(self)
                
        self.zmax = 0.00
        self.zeros = None

    def trigger_refresh(self):
        self.update()

    def paintEvent(self, event):
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.Base)
        self.painter.begin(self)
        self.draw_axis()
        self.draw()
        self.painter.end()

    def draw_axis(self):
        self.painter.setPen(QPen(Qt.blue,2))
        self.painter.drawLine(0,int(self.height()/2),self.width(),int(self.height()/2))
        self.painter.setPen(QPen(Qt.black,2))
        matrices = QFontMetrics(self.font())
        width = matrices.horizontalAdvance('beam')
        self.painter.drawText(0,(int(self.height()/2))+10, 'beam')
        self.painter.drawLine(width+5,0,width+5,self.height())
        self.painter.setPen(QPen(Qt.black,1))
        self.zeros = [width+6, int(self.height()/2)]

    def draw(self):
        #if len(g_component) < 1:
        #    return
        for component in var.G_COMPONENT:
            if component.ctype == "Beam": continue
            self.container(component)

    def container(self, component):
        # Only Draw container...
        # Should update subcomponent figure
        pos = {'HLX':"0.0 mm",'HLY':"0.0 mm",'HLZ':"0.0 mm",
               'RMin':"0.0 mm",'RMax':"0.0 mm",
               'HL':"0.0 mm", 'SPhi':"0.0 deg", 'DPhi':"0.0 deg",
               'RotX':"0.0 deg",'RotY':"0.0 deg",'RotZ':"0.0 deg",
               'TransX':"0.0 mm",'TransY':"0.0 mm",'TransZ':"0.0 mm"}
        ftype = ''
        for para in component.subcomponent['Basis'].parameters:
            if 'Type' == para.name:
                ftype = para.value.replace('"','').replace("'",'').replace(' ','')
            if any(para.name.lower() == i.lower() for i in pos.keys()):
                value, unit = component.calculate_value(para)
                if unit == 'mm': 
                    value = value / 10
                elif unit == 'm': 
                    value *= 100
                pos[para.name] = value

        for key, val in pos.items():
            if str(type(val)) == "<class 'str'>":
                temp = val.split(' ')
                pos[key] = float(temp[0])

        if pos['TransZ'] > self.zmax:
            self.zmax = pos['TransZ']

        if ftype == '': ftype = 'Other'

        if any(ftype == i for i in ['TsBox', 'TsDipoleMagnet', 'Other']) and any(i == 0.0 for i in [pos['HLY'], pos['HLZ']]):
            if pos['HLY'] == 0.0:
                HLY = 0.0
                for subname, subcomp in component.subcomponent.items():
                    if subname == 'Basis': continue
                    for para in subcomp.parameters:
                        if not para.name.lower() == 'hly': continue
                        value, unit = component.calculate_value(para)
                        if unit == 'mm': value = value / 10
                        elif unit == 'm': value *= 100
                        if value > HLY: HLY = value
                pos['HLY'] = HLY
            if pos['HLZ'] == 0.0:
                HLZ = 0.0
                for subname, subcomp in component.subcomponent.items():
                    if subname == 'Basis': continue
                    for para in subcomp.parameters:
                        if not para.name.lower() == 'hlz': continue
                        value, unit = component.calculate_value(para)
                        if unit == 'mm': value = value / 10
                        elif unit == 'm': value *= 100
                        HLZ += value
                pos['HLZ'] = HLZ

        elif any(ftype == i for i in ['TsCylinder', 'TsRangeModulator']) and any(i == 0.0 for i in [pos['RMax'], pos['HL']]):
            if pos['RMax'] == 0.0:
                RMax = 0.0
                for subname, subcomp in component.subcomponent.items():
                    if subname == 'Basis': continue
                    for para in subcomp.parameters:
                        if not para.name.lower() == 'rmax': continue
                        value, unit = component.calculate_value(para)
                        if unit == 'mm': value = value / 10
                        elif unit == 'm': value *= 100
                        if value > RMax: RMax = value
                pos['RMax'] = RMax
            if pos['HL'] == 0.0:
                HL = 0.0
                for subname, subcomp in component.subcomponent.items():
                    if subname == 'Basis': continue
                    for para in subcomp.parameters:
                        if not para.name.lower() == 'hl': continue
                        value, unit = component.calculate_value(para)
                        if unit == 'mm': value = value / 10
                        elif unit == 'm': value *= 100
                        HL += value
                pos['HLZ'] = HL

        self.figure(ftype, pos)

    def figure(self, ftype, pos):
        hexcodes = { # Name:(Container, Interior)
            'TsBox':('#07098a','#1be32c'), 
            'TsCylinder':('#9d1be3','#1be32c'),
            'TsRangeModulator':('#373d36','#f0e373'),
            'TsDipoleMagnet':('#23fabd','#23d2fa'),
            'TsAperture':('#30d14e','#a69b94'),
            'TsCompensator':('#e88133','#a69b94'),
            'Group':('#ffff00','#59ff00'),
            'Other':('#000000','#000000')}
        color = QColor(0,0,0)
        idx = 0 # Removing interior part, if you have enough time update interior
        color.setNamedColor(hexcodes[ftype][idx])
        self.painter.setBrush(color)
        yaxis = pos['TransY']
        zaxis = pos['TransZ']
        if ftype == "TsBox":
            height = pos['HLY']
            width = pos['HLZ']
        elif ftype == "TsCylinder":
            height = pos['RMax']
            width = pos['HL']
        elif ftype == "TsRangeModulator":
            # FIXME
            height = pos['RMax']*2
            width = pos['HL']
        elif ftype == "TsDipoleMagnet":
            height = pos['HLY']
            width = pos['HLZ']
        else:
            height = pos['HLY']
            width = pos['HLZ']
            if height == 0.0: height = 10.0
            if width == 0.0: width = 10.0

        if pos['TransZ'] == self.zmax:
            start = (self.zeros[0],self.zeros[1]-5*height/2)
            end = (self.zeros[0]+5*width,self.zeros[1]+5*height/2)
        else:
            relz = self.zmax - pos['TransZ']
            start = (self.zeros[0]+3*relz,self.zeros[1]-5*height/2)
            end = (self.zeros[0]+3*relz+5*width, self.zeros[1]+5*height/2)
        
        self.painter.drawRect(int(start[0]),int(start[1]),int(end[0]-start[0]),int(end[1]-start[1]))