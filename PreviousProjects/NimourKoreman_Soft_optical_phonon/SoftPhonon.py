# Made by Ruud Nimour (4100484) and Tim Koreman(4128648),
# Adapted from Sanli Faez' "udemo_harmonic_chain.py" and "udemo_disordered_tightbinding.py"

import sys
from pyqtgraph.Qt import QtCore, QtGui
from guihelp import Ui_MainWindow
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time
import math

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

    # initialize
    def __init__(self, nr):
        QtGui.QMainWindow.__init__(self)
        self.timer = QtCore.QTimer(self)
        #GUI loading
        self.setupUi(self)

        self.N=nr           # nr of particles
        self.omega=1.       # natural frequency
        self.alpha=0.05     # coupling strength
        self.a=1            # lattice spacing
        self.xindex = np.arange(self.N)
        self.deltaT = 0.05  # time steps

        self.initUi()       
        self.connectButtons()
        
    #connecting user interactions with corresponding functions
    def connectButtons(self):       
        self.Slider1.valueChanged.connect(self.coupling)
        self.Slider2.valueChanged.connect(self.basefreq)
    
    # setting initial values and ranges
    def initUi(self):
        self.p1 = self.ViewPort.addPlot()
        self.Slider1.setMinimum(0) # coupling, /100
        self.Slider1.setMaximum(40)
        self.Slider1.setValue(self.alpha*100)
        self.LcdNumber1.display(self.alpha)
        self.Slider2.setMinimum(0) # basefreq, /10
        self.Slider2.setMaximum(100)
        self.Slider2.setValue(self.omega*10)
        self.LcdNumber2.display(self.omega/10)
        self.Label1.setText("Coupling strength")
        self.Label2.setText("Base frequency")

        # plot settings
        self.p1.enableAutoRange('xy', False)
        self.p1.setXRange(-1, self.N, padding=0)
        self.p1.setYRange(-1,1, padding=0)
        
        self.timer.timeout.connect(self.update)
        self.timer.start(20) # looptime in ms

        # initial conditions
        self.array=[0] * self.N
        self.arrayd=[0] * self.N
        self.array[math.ceil(self.N/2)] = 1

        # initialize the curve
        self.curve = self.p1.plot(self.xindex, self.array, pen=None, symbol='o')

    # this is the main loop which runs every x ms where x is as in self.timer.start(x)
    def update(self):
        self.nextstep(self.array, self.arrayd)
        data = self.array
        self.curve.setData(data)

    # the sum E_n in the equation of motion
    def E(self, n, array):
        res = 0

        for m in range(n - math.ceil(self.N/2), n + math.ceil(self.N/2)):
            if n != m:
                res += (2*array[m%self.N]) / ((math.fabs(n-m*self.a))**3)
        return res

    # this takes the arrays from the previous step, and produces the new arrays
    def nextstep(self, array, arrayd):
        oldarray = array
        oldarrayd = arrayd

        for i in range(0,self.N):
            array[i] = oldarray[i] + self.deltaT * oldarrayd[i]
            arrayd[i] = oldarrayd[i] + self.deltaT * (-1 * self.omega**2 * oldarray[i] + self.alpha * self.omega**2 * MainWindow.E(self,i, oldarray) )

        # this gets called if the coupling changes
    def coupling(self):
        self.alpha=self.Slider1.value()/100.
        self.LcdNumber1.display(self.alpha)

    # this gets called if the base frequency changes
    def basefreq(self):
        self.omega=self.Slider2.value()/10.
        self.LcdNumber2.display(self.omega)


## To run the routine as an standalone program use the following structure.
## Starts Qt event loop unless running in interactive mode or using pyside.
def main(arg):
    numberparticles = 25    # standard we have 25 particles
    if len(sys.argv) >= 2:  # if we give an argument, take the first number
        numberparticles = int(sys.argv[1])
        
    app = QtGui.QApplication(sys.argv)
    ui = MainWindow(numberparticles)
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main(10)