# -*- coding: utf-8 -*-
"""
Script demonstrating solutions of a tight-binding hamiltonian with diagonal
disorder.

This script uses pyQT4 and the pyqtgraph module for GUI.
The skin (interface) should be created separately in
QTdesigner and compiled into a python code (see GUI instructions.)

v0.1 Created by Sanli Faez, 11 November 2016 using Python3.4 on Windows 64bit
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
        procedure for initializing the functionalities of the GUI
        """
        QtGui.QMainWindow.__init__(self)
        self.timer = QtCore.QTimer(self)
        #GUI loading
        self.setupUi(self)
        self.chainlen = 256
        self.modes = np.eye(self.chainlen)
        self.initUi()
        self.connectButtons()

    def connectButtons(self):
        """
        connecting user interactions with corresponding functions
        """
        self.Slider1.valueChanged.connect(self.updatehop)
        self.Slider2.valueChanged.connect(self.updatedis)
        self.Slider3.valueChanged.connect(self.showmode)

    def initUi(self):
        """
        setting initial values and ranges if necessary. This is very
        important for idiot-proofing the program and preventing a crash
        """
        self.p1 = self.ViewPort.addPlot()
        self.Slider1.setMinimum(0)
        self.Slider1.setMaximum(10)
        self.Slider1.setValue(0)
        self.LcdNumber1.display(1)
        self.Slider2.setMinimum(0)
        self.Slider2.setMaximum(10)
        self.Slider2.setValue(0)
        self.LcdNumber2.display(0)
        self.Slider3.setMinimum(1)
        self.Slider3.setMaximum(self.chainlen-1)
        self.Slider3.setValue(1)
        self.LcdNumber3.display(1)
        self.Label3.setText("mode number")
        self.Label1.setText("hopping")
        self.Label2.setText("disorder")
        self.curve = self.p1.plot(self.modes[:,1], pen=pg.mkPen('w', width=2))

        self.p1.enableAutoRange('xy', False)

    def calcmodes(self, n, w=-10, t=1, var=0):
        """
        This function creates a random tridiagonal matrix that represents the
        tight binding hamiltonian and calculated its eigenvectors
        """
        mat = w * np.eye(n) + np.diag(t*np.ones(n-1), k=1) + np.diag(t*np.ones(n-1), k=-1)
        if var != 0:
            dis = np.random.normal(0, var, n)
            mat = mat + np.diag(dis)
        mat[0,n-1] = mat[n-1,0] = t #uncomment for periodic boundary conditions
        w, v = np.linalg.eig(mat)
        return v

    def showmode(self, m=1):
        self.LcdNumber3.display(m)
        data = self.modes[:,m]
        self.curve.setData(np.absolute(data))


    def updatehop(self):
        """
        each time the hopping slider value is changed
        this function generated a new matrix with different hopping
        """
        self.LcdNumber1.display(self.Slider1.value())
        self.modes = self.calcmodes(self.chainlen, -10, self.Slider1.value(), self.Slider2.value())
        self.showmode(self.Slider3.value())

    def updatedis(self):
        """
        each time the disorder slider value is changed
        this function generated a new matrix with different degree of disorder
        """
        self.LcdNumber2.display(self.Slider2.value())
        self.modes = self.calcmodes(self.chainlen, -10, self.Slider1.value(), self.Slider2.value())
        self.showmode(self.Slider3.value())

#%% To run the routine as an standalone program use the following structure.
## Starts Qt event loop unless running in interactive mode or using pyside.
def main():
    app = QtGui.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
