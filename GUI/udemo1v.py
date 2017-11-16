# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interactiveplot.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(518, 432)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.Label = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu Mono"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.Label.setFont(font)
        self.Label.setObjectName(_fromUtf8("Label"))
        self.gridLayout.addWidget(self.Label, 1, 0, 1, 1)
        self.Slider = QtGui.QSlider(self.centralwidget)
        self.Slider.setOrientation(QtCore.Qt.Horizontal)
        self.Slider.setObjectName(_fromUtf8("Slider"))
        self.gridLayout.addWidget(self.Slider, 1, 1, 1, 1)
        self.LcdNumber = QtGui.QLCDNumber(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.LcdNumber.setFont(font)
        self.LcdNumber.setFrameShape(QtGui.QFrame.Box)
        self.LcdNumber.setFrameShadow(QtGui.QFrame.Plain)
        self.LcdNumber.setLineWidth(1)
        self.LcdNumber.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.LcdNumber.setObjectName(_fromUtf8("LcdNumber"))
        self.gridLayout.addWidget(self.LcdNumber, 1, 2, 1, 1)
        self.ViewPort = GraphicsLayoutWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ViewPort.sizePolicy().hasHeightForWidth())
        self.ViewPort.setSizePolicy(sizePolicy)
        self.ViewPort.setMinimumSize(QtCore.QSize(500, 350))
        self.ViewPort.setObjectName(_fromUtf8("ViewPort"))
        self.gridLayout.addWidget(self.ViewPort, 0, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.StatusBar = QtGui.QStatusBar(MainWindow)
        self.StatusBar.setEnabled(False)
        self.StatusBar.setObjectName(_fromUtf8("StatusBar"))
        MainWindow.setStatusBar(self.StatusBar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Utrecht Condensed Matter Demonstrator", None))
        self.Label.setText(_translate("MainWindow", "Variable name", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))

from pyqtgraph import GraphicsLayoutWidget
