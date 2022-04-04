#!usr/bin/python3
from PySide6.QtWidgets import QSlider,QLabel,QApplication,\
    QLineEdit,QHBoxLayout,QVBoxLayout,QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor,QPainter,QPaintEvent
import sys

class colorsq(QWidget):
    def __init__(self,parent):
        super().__init__(parent)
        self.rvalue=self.gvalue=self.bvalue=0
        self.setMinimumSize(200,200)
    def paintEvent(self, a0: QPaintEvent):
        qp=QPainter()
        clr=QColor(self.rvalue,self.gvalue,self.bvalue)
        rt=self.rect()
        qp.begin(self)
        qp.eraseRect(self.rect())
        qp.setBrush(clr)
        qp.drawRect(rt)
        qp.end()
    def changev(self,rgbv,mode):
        if mode=='R':
            self.rvalue=rgbv
        elif mode=='G':
            self.gvalue=rgbv
        elif mode=='B':
            self.bvalue=rgbv
    def getrgbv(self,mode):
        if mode=='R':
            return self.rvalue
        elif mode=='G':
            return self.gvalue
        elif mode=='B':
            return self.bvalue

def main():
    app=QApplication(sys.argv)
#initui
    mwindow=QWidget()
    clrsq=colorsq(mwindow)
    rgb=['R','G','B']
    rgbslider=[]
    rgbline=[]
    rgblabel=[]
    rgbbox=[]
    hbox=QHBoxLayout()
    rgbsliderbox=QHBoxLayout()
    #槽函数定义
    rgbfun=[]
    def changev(v,x):
        rgbline[x].setText(str(v))
        rgbslider[x].setValue(int(v))
        clrsq.changev(int(v),rgb[x])
        hextext='#'
        for i in range(3):
            hexv=str(hex(clrsq.getrgbv(rgb[i])))[2:]
            if len(hexv)==1:
                hexv='0'+hexv
            hextext+=hexv
        clrhex.setText(hextext)
        clrsq.repaint()
    rgbfun.append(lambda v:changev(v,0))
    rgbfun.append(lambda v:changev(v,1))
    rgbfun.append(lambda v:changev(v,2))
    def clrhexpro(clrv:str):
        v=''.join(clrv.split())
        if (not len(v) == 7) or (not v[0] == '#'):
            return
        for i in range(3):
            rgbfun[i](int(v[i*2+1:i*2+3],16))
    for i in range(3):
        rgbslider.append(QSlider(Qt.Orientation.Vertical,mwindow))
        rgbline.append(QLineEdit('0',mwindow))
        rgbslider[i].setMinimum(0)
        rgbslider[i].setMaximum(255)
        rgbslider[i].setSingleStep(1)
        #信号与槽连接
        rgbslider[i].valueChanged.connect(rgbfun[i])
        rgbline[i].textChanged.connect(rgbfun[i])
        rgblabel.append(QLabel(rgb[i],mwindow))
        rgbbox.append(QVBoxLayout())
        rgbbox[i].addWidget(rgblabel[i])
        rgbbox[i].addWidget(rgbslider[i])
        rgbbox[i].addWidget(rgbline[i])
        rgbsliderbox.addLayout(rgbbox[i])
    vclrbox=QVBoxLayout()
    vclrbox.addLayout(rgbsliderbox)
    clrhex=QLineEdit('#000000',mwindow)
    clrhex.textChanged.connect(clrhexpro)
    vclrbox.addWidget(clrhex)
    hbox.addLayout(vclrbox)
    hbox.addWidget(clrsq)
    mwindow.setLayout(hbox)
    mwindow.show()
    mwindow.resize(326,200)
    mwindow.setWindowTitle('sRGB mixer')
#ui,finished
    sys.exit(app.exec())

if __name__=='__main__':
    main()