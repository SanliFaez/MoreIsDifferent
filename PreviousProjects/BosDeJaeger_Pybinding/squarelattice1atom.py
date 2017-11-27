#%%
"""
This script is made by Meike Bos and Marjolein de Jager
It illustrates the energy bands of a square lattice with ONE atom per unit cell
For our calculation we use Pybinding, this is compatible for python 3.4 or newer
http://docs.pybinding.site
"""
#%%
import pybinding as pb
pb.pltutils.use_style()
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from math import pi, sqrt

#%%
"""
First we a fucntion that makes our lattice
"""
#This function makes a square lattice with one atom per unit cell
def squarelat(a, d, tx, ty):                
    #a = lattice constant, d = on-site energy, tx,ty = hopping x-,y-direction
    lat = pb.Lattice(a1=[a, 0], a2=[0, a])
    lat.add_sublattices(
        ('A', [0, 0], d)
    )
    lat.add_hoppings(
        ([0, 1], 'A', 'A', ty),
        ([1, 0], 'A', 'A', tx)
    )
    return lat

#%%
"""
Then we make our starting lattice
Varying the lattice constant isn't interesting for our plots, so we choose a = 0.2 nm
"""
#The starting lattice
a=0.2
d=0
tx=1.5
ty=1.5
lattice = squarelat(a, d, tx, ty)
modellat = pb.Model(lattice, pb.primitive(a1=5,a2=5))
modellat.plot()
modellat.lattice.plot_vectors(position=[0.0,0.0])
plt.show()

#%%
"""
Then we calculate the energy bands and plot them
"""
#First close a figures that were still open
plt.close('all')

#Make a figure
fig, ax = plt.subplots(figsize=(6, 4))
plt.subplots_adjust(left=0.15, bottom=0.35)
ax.set_xlabel('Location', fontsize=7)
ax.set_ylabel('Energy (eV)', fontsize=7)
ax.set_title('Energy band', fontsize=10)

#Calculate the energy band
model = pb.Model(lattice, pb.translational_symmetry())
solver = pb.solver.lapack(model)
bands = solver.calc_bands([0, 0], [0, pi/a], [pi/a, pi/a], [0, 0])
data = bands.energy

#Plot the band
y = data
dx = pi/a * (2 + sqrt(2))/len(y)
x = np.arange(0.0, len(y) * dx, dx)
xtick = [0, pi/a, 2*pi/a, x[-1]]
labels = ['[0,0]','[0,$\pi$/a]','[$\pi$/a,$\pi$/a]','[0,0]']
plt.xticks(xtick, labels)
l, = plt.plot(x, y, lw=1, color='red')
plt.axis([0, len(y)*dx, -10, 10])
plt.xticks()

#%%
"""
We make three sliders that can vary the on-site energy and the hopping in x- and y-direction
to show their influence on the energy bands
"""
#Making the sliders
axcolor = 'lightgoldenrodyellow'
axd = plt.axes([0.15, 0.2, 0.75, 0.03], axisbg=axcolor)
axtx = plt.axes([0.15, 0.15, 0.75, 0.03], axisbg=axcolor)
axty = plt.axes([0.15, 0.1, 0.75, 0.03], axisbg=axcolor)

sd = Slider(axd, 'Energy', -10.0, 10.0, valinit=0)
stx = Slider(axtx, 'Hopping x', -5.0, 5.0, valinit=1.5)
sty = Slider(axty, 'Hopping y', -5.0, 5.0, valinit=1.5)

#Making sure that the plot of the energy bands is updated
def update(val):
    d = sd.val
    tx = stx.val
    ty = sty.val
    lattice = squarelat(a, d, tx, ty)
    model = pb.Model(lattice, pb.translational_symmetry())
    solver = pb.solver.lapack(model)
    bands = solver.calc_bands([0, 0], [0, pi/a], [pi/a, pi/a], [0, 0])
    l.set_ydata(bands.energy)
    fig.canvas.draw_idle()
sd.on_changed(update)
stx.on_changed(update)
sty.on_changed(update)

#A reset button that takes you back to the initial values of the sliders
resetax = plt.axes([0.79, 0.025, 0.11, 0.04])
resetb = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

def reset(event):
    sd.reset()
    stx.reset()
    sty.reset()
resetb.on_clicked(reset)

plt.show()

#%%
"""
We make three more button that give us figures of the lattice, unit cell and first Brillouin zone
"""
latax = plt.axes([0.15, 0.025, 0.1, 0.04])
latb = Button(latax, 'Lattice', color=axcolor, hovercolor='0.975')

def showlat(event):
    plt.figure(2)
    plt.subplot(111, title="Lattice")
    modellat.plot()
    modellat.lattice.plot_vectors(position=[0.0,0.0])
    plt.show()
latb.on_clicked(showlat)

unitax = plt.axes([0.27, 0.025, 0.1, 0.04])
unitb = Button(unitax, 'Unit', color=axcolor, hovercolor='0.975')

def showunit(event):
    plt.figure(3)
    plt.subplot(111, title="Unit cell with neighbours")
    lattice.plot()
    plt.show()
unitb.on_clicked(showunit)

brax = plt.axes([0.39, 0.025, 0.1, 0.04])
brb = Button(brax, 'Brillouin', color=axcolor, hovercolor='0.975')

def showbr(event):
    plt.figure(4)
    plt.subplot(111, title="Brillouin zone")
    lattice.plot_brillouin_zone()
    plt.show()
brb.on_clicked(showbr)
