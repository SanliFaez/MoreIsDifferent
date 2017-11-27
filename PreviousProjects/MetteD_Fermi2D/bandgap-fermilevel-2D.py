"""
Created on Tue Jan  3 10:20:37 2017

@author: mettemortensen

This program demonstrates the band gap and the Fermi level using 
a 2D square lattice in the nearly free electron model
"""

import numpy as np
from numpy import pi
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl


kpoints=100

a = 1.0 #lattice constant
G = 2*pi/a
n = np.arange(-1,2)
nsize = np.size(n)
nsize2 = nsize**2
V0 = 3.0 #strength of the perioic potential

kxs = np.linspace(-pi/a, pi/a, kpoints)
kys = np.linspace(-pi/a, pi/a, kpoints)

coeffs = np.zeros(nsize2) #Fourier coefficients of the potential 
coeffs[1::2]=0.5 * V0
coeffs[0] = 0.5 * V0

#Create the Hamiltonian
H = np.zeros((nsize2,nsize2))

for i in xrange(1,nsize2):
    offdiag = coeffs[i] * np.ones(nsize2 - i)
    H = H + (np.diag(offdiag,k=i) + np.diag(offdiag,k=-i))
    
    
def Energy(q,p):
    for i in range(0,nsize):
        for j in range(0,nsize):
            H[nsize*i+j,nsize*i+j] = 0.5*((q + n[i]*G)**2 + (p + n[j]*G)**2) + coeffs[0]
    return np.real(np.sort((np.linalg.eigvals(H)))) #Find eigenvalues of the Hamiltonian


#Arrange the values in energy bands
bands = np.array([Energy(-pi/a,-pi/a)])

for kx in kxs:
    for ky in kys:
        bands = np.append(bands, np.array([Energy(kx,ky)]), axis=0)
        
bands = np.delete(bands,0,0)


#Create a GL View widget to display data
app = QtGui.QApplication([])
plot = gl.GLViewWidget()
plot.show()
plot.setWindowTitle('Band gap + Fermi level')
plot.setCameraPosition(distance=50)

#Add a grid
g = gl.GLGridItem()
g.setDepthValue(10)
plot.addItem(g)

#Plot the bands
#Change the values in xrange to add more bands to the plot
for n in xrange(0,2):
    z = np.reshape(bands[:,n],(100,100))
    bandn = gl.GLSurfacePlotItem(x=kxs, y=kys, z=z, shader='normalColor')
    bandn.scale(3,3,1)
    plot.addItem(bandn)

#Add the Fermi level to the plot
Ef = 5.0 * np.ones((100,100))
fermi = gl.GLSurfacePlotItem(x=kxs, y=kys, z=Ef, shader='shaded', 
                             color=(0.0,0.25,0.5,0.0))
fermi.scale(3,3,1)
plot.addItem(fermi)


#Start Qt event loop unless running in interactive mode
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()