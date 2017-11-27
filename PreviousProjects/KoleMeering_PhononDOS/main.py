#!/usr/bin/env python3

import sys
from pyqtgraph.Qt import QtGui
import pyqtgraph as pg
import numpy as np
from MainWindow import Ui_MainWindow

from Simulation import Simulation

# setup pyqtgraph colors
pg.setConfigOption("background", (0, 0, 0))
pg.setConfigOption("foreground", (255, 255, 255))
pgPenColor = (255, 127, 0)
pgPenWidth = 2


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("MCM: phonon DOS calculation for 3D-lattice")

        # set simulation var
        self.s = Simulation()

        # UI
        self.initWidgets()
        self.connectWidgets()

        # plot
        self.plot1.enableAutoRange("xy", True)
        self.sliderChanged(None)

        # center window and show
        desktop = QtGui.QApplication.desktop()
        screen = desktop.screenNumber(desktop.cursor().pos())
        center = desktop.screenGeometry(screen).center()
        self.move(center.x() - self.size().width() / 2,
                  center.y() - self.size().height() / 2)
        self.show()
        self.raise_()

    def initWidgets(self):
        # plot
        self.plot1 = self.ViewPort.addPlot()
        self.plot1.setLabel("left", text="DOS")  # , units=""
        self.plot1.setLabel("bottom", text="ω")
        self.line = self.plot1.plot(pen=pg.mkPen(pgPenColor, width=pgPenWidth))

        # combobox
        self.comboDispersion.addItems(["Linear", "Harmonic"])

        # sliders
        self.sliders = [self.Slider1, self.Slider2, self.Slider3]
        self.lcds = [self.LcdNumber1, self.LcdNumber2, self.LcdNumber3]
        for i in range(0, 3):
            self.sliders[i].setMinimum(100)
            self.sliders[i].setMaximum(1000)
            self.sliders[i].setTickInterval(100)
            self.sliders[i].setValue(self.s.latticeConstants[i])
            self.lcds[i].display(self.s.latticeConstants[i])

        # vsliders
        self.slidersv = [self.sliderv1, self.sliderv2, self.sliderv3]
        self.lcdsv = [self.lcdv1, self.lcdv2, self.lcdv3]
        for i in range(0, 3):
            self.slidersv[i].setMinimum(100e12)
            self.slidersv[i].setMaximum(10000e12)
            self.slidersv[i].setTickInterval(100e12)
            self.slidersv[i].setValue(self.s.speedOfSound[i])
            self.lcdsv[i].display(self.s.speedOfSound[i])

    def connectWidgets(self):
        self.comboDispersion.currentIndexChanged.connect(self.comboChanged)
        self.Slider1.valueChanged.connect(self.sliderChanged)
        self.Slider2.valueChanged.connect(self.sliderChanged)
        self.Slider3.valueChanged.connect(self.sliderChanged)

        self.sliderv1.valueChanged.connect(self.slidervChanged)
        self.sliderv2.valueChanged.connect(self.slidervChanged)
        self.sliderv3.valueChanged.connect(self.slidervChanged)

        self.atomBox.valueChanged.connect(self.atomBoxChanged)

    def comboChanged(self, value):
        if value == 0:
            for slider in self.slidersv:
                slider.setEnabled(True)
        elif value == 1:
            for slider in self.slidersv:
                slider.setEnabled(False)

        self.s.dispersionRelationType = value
        self.s.updateSimulationValues()
        self.updatePlot()

    def sliderChanged(self, value):
        for i in range(0, 3):
            self.s.latticeConstants[i] = self.sliders[i].value()
            self.lcds[i].display(self.s.latticeConstants[i])

        self.s.updateSimulationValues()
        self.s.generateCoords()
        self.s.generateKStates()
        self.updatePlot()

    def slidervChanged(self, value):
        for i in range(0, 3):
            self.s.speedOfSound[i] = self.slidersv[i].value()
            self.lcdsv[i].display(self.s.speedOfSound[i])

        self.s.updateSimulationValues()
        self.s.generateCoords()
        self.s.generateKStates()
        self.updatePlot()

    def atomBoxChanged(self, value):
        self.s.atomCount = value
        self.s.atomCoords = np.empty((value**3, 3+1))
        self.s.kStateCoords = np.empty((value**3, 3+1))

        self.s.updateSimulationValues()
        self.s.generateCoords()
        self.s.generateKStates()
        self.updatePlot()

    def updatePlot(self):
        self.line.setData(self.s.omegaList, self.s.calcDOS())


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mainWindow = MainWindow()

    sys.exit(app.exec_())
