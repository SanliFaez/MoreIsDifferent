# -*- coding: utf-8 -*-
"""
Script demonstrating waves in a harmonic chain

v0.1 Created by Sanli, 11 November 2016
"""
#%%
import sys
from pyqtgraph.Qt import QtCore, QtGui
from GUI.udemo3v import Ui_MainWindow
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time
#%%
class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        """
        procedure for initializing the functionalities
        """
        QtGui.QMainWindow.__init__(self)
        self.timer = QtCore.QTimer(self)  
        #GUI loading
        self.setupUi(self) 
        self.connectButtons()
        self.looptime = 0
        self.chainlen = 20
        self.xindex = np.arange(self.chainlen)
        self.initUi()
        
    def connectButtons(self):
        """
        connecting user interactions with corresponding functions
        """       
        self.Slider1.valueChanged.connect(self.update)

    def initUi(self):
        """
        setting initial values and ranges if necessary. This is very 
        important for idiot-proofing the program and preventing a crash
        """    
        self.p1 = self.ViewPort.addPlot()        
        self.ViewPort.nextRow()
        self.p2 = self.ViewPort.addPlot()  
        self.Slider1.setMinimum(-self.chainlen/2+1)
        self.Slider1.setMaximum(self.chainlen/2)        
        self.Slider1.setValue(0)
        self.LcdNumber1.display(0)
        self.Slider2.setMinimum(1)
        self.Slider2.setMaximum(20)
        self.Slider2.setValue(1)
        self.LcdNumber2.display(1)        
        self.Slider3.setMinimum(0)
        self.Slider3.setMaximum(1)
        self.Slider3.setValue(0)
        self.LcdNumber3.display(0)
        self.Label1.setText("kL/2pi")
        self.Label2.setText("stiffness")
        self.Label3.setText("dispersion branch")
        y = np.sin(self.xindex)
        self.curve1 = self.p1.plot(self.xindex, y, pen='r', symbol='o', symbolPen='r')
        self.curve2 = self.p2.plot(self.xindex, y, pen='b', symbol='o')
        self.p1.enableAutoRange('xy', False)
        self.p2.enableAutoRange('xy', False)
        self.timer.timeout.connect(self.update)
        self.timer.start(50)

    def dispersion(self, n=1, v=1):
        k = 2*np.pi/self.chainlen*n
        gamma = 1/4
        if self.Slider3.value() == 0:
            w = v*np.sqrt(1-np.sqrt(1-np.sin(k/2)*np.sin(k/2)*gamma))
        else:
            w = v*np.sqrt(1+np.sqrt(1-np.sin(k/2)*np.sin(k/2)*gamma))
                
        return w

    def wave(self, t, n=1, v=1):
        k = 2*np.pi/self.chainlen*n
        w = self.dispersion(n, v)
        positions = np.cos(w*t-k*self.xindex)
        return positions
            
    def update(self):
        """
        actions in the main loop
        """    
        self.looptime = self.looptime + 1
        self.LcdNumber1.display(self.Slider1.value())
        self.LcdNumber2.display(self.Slider2.value())        
        self.LcdNumber3.display(self.Slider3.value())
        data = self.wave(self.looptime, self.Slider1.value(), self.Slider2.value()/self.chainlen)
        self.curve1.setData(data)        
        self.curve2.setData(data)        

#%% To run the routine as an standalone program use the following structure.  
## Starts Qt event loop unless running in interactive mode or using pyside. 
def main():
    app = QtGui.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
