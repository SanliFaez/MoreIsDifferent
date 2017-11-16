# -*- coding: utf-8 -*-
"""
Example of interactive dynamic viewer based on PyQt and pyqtgraph for a generic multi-variable function

v0.1 Created by Sanli Faez, 16 November 2017
"""
## Libraries necessary for running the interactive app
import sys
from pyqtgraph.Qt import QtCore, QtGui
from GUI.udemo2v import Ui_MainWindow
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time

##
from MIDmethods import SanliFaez
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
        self.chainlen = 50
        self.xindex = np.arange(self.chainlen)
        y = np.sin(self.xindex)
        self.p1 = self.ViewPort.addPlot()
        self.curve = self.p1.plot(self.xindex, y, pen=None, symbol='o')
        self.p1.enableAutoRange('xy', False)
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
        self.Slider1.setMinimum(1)
        self.Slider1.setMaximum(30)
        self.Slider1.setValue(1)
        self.LcdNumber1.display(1)
        self.Slider2.setMinimum(1)
        self.Slider2.setMaximum(20)
        self.Slider2.setValue(1)
        self.LcdNumber2.display(1)
        self.Label1.setText("Wavelength")
        self.Label2.setText("Phase")
        self.timer.timeout.connect(self.update)
        self.timer.start(50)

    def update(self):
        """
        Generic actions in the main loop
        """    
        self.looptime = self.looptime + 1
        self.LcdNumber1.display(self.Slider1.value())
        self.LcdNumber2.display(self.Slider2.value())

        ## Actual calculation to be displated
        data = SanliFaez.sine_wave(self.xindex, wavelength=self.Slider1.value(), phase=self.Slider2.value())
        self.curve.setData(data)

# To run the routine as an standalone program use the following structure.
# Starts Qt event loop unless running in interactive mode or using pyside.
def main():
    app = QtGui.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
