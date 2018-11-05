#%%
"""
This script is made by Meike Bos and Marjolein de Jager
It illustrates the energy bands of a square lattice with TWO (different) atoms per unit cell
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
#This function makes a square lattice with two (different) atoms per unit cell
def squarelat2(a, dA, dB, t, dx, dy):                
    #a = lattice constant, dA = on-site energy atom A, dB = on-site energy atom B, t = hopping, 
    #dx,dy = location of atom B (values between 0 and 1)
    lat = pb.Lattice(a1=[a, 0], a2=[0, a])
    lat.add_sublattices(
        ('A', [0, 0], dA),
        ('B', [a*dx, a*dy], dB)
    )
    lat.add_hoppings(
        ([ 0,  0], 'A', 'B', sqrt((1-dx)*(1-dx) + (1-dy)*(1-dy))*t),    #When B closer to A, the hopping should be larger
        ([ 0, -1], 'A', 'B', sqrt((1-dx)*(1-dx) + dy*dy)*t),
        ([-1,  0], 'A', 'B', sqrt(dx*dx + (1-dy)*(1-dy))*t),
        ([-1, -1], 'A', 'B', sqrt(dx*dx + dy*dy)*t) 
    )
    return lat

#%%
"""
Then we make our starting lattice
Varying the lattice constant isn't interesting for our plots, so we choose a = 0.2 nm
"""
#The starting lattice
a=0.2
dA=0
dB=0
t=1.5
dx=0.5
dy=0.5
lattice = squarelat2(a, dA, dB, t, dx, dy)
modellat = pb.Model(lattice, pb.primitive(a1=5,a2=5))

#%%
"""
Then we calculate the energy bands and plot them
"""
#First close a figures that were still open
plt.close('all')

#Make a figure
fig, ax = plt.subplots(figsize=(6, 4))
plt.subplots_adjust(left=0.15, bottom=0.45)
ax.set_xlabel('Location', fontsize=8)
ax.set_ylabel('Energy (eV)', fontsize=8)
ax.set_title('Energy band', fontsize=10)

#Calculate the bands
model = pb.Model(lattice, pb.translational_symmetry())
solver = pb.solver.lapack(model)
bands = solver.calc_bands([0, 0], [0, pi/a], [pi/a, pi/a], [0, 0])

#Plot the bands
data = bands.energy
y1 = data[:,0]
y2 = data[:,1]
dx = pi/a * (2 + sqrt(2))/len(y1)
x = np.arange(0.0, len(y1) * dx, dx)
xtick = [0, pi/a, 2*pi/a, x[-1]]
labels = ['[0,0]','[0,$\pi$/a]','[$\pi$/a,$\pi$/a]','[0,0]']
plt.xticks(xtick, labels)
plt.hold(True)
l1, = plt.plot(x, y1, lw=1, color='red')
l2, = plt.plot(x, y2, lw=1, color='blue')
plt.hold(False)
plt.axis([0, len(y1)*dx, -10, 10])
plt.show()

#%%
"""
We make five sliders that can vary the on-site energy of atom A and B, the hopping and the location of atom B
to show their influence on the energy bands
"""
#Making the sliders
axcolor = 'lightgoldenrodyellow'
axdA = plt.axes([0.15, 0.3, 0.75, 0.03], axisbg=axcolor)
axdB = plt.axes([0.15, 0.25, 0.75, 0.03], axisbg=axcolor)
axt = plt.axes([0.15, 0.2, 0.75, 0.03], axisbg=axcolor)
axdx = plt.axes([0.15, 0.15, 0.75, 0.03], axisbg=axcolor)
axdy = plt.axes([0.15, 0.1, 0.75, 0.03], axisbg=axcolor)

sdA = Slider(axdA, 'Energy A', -10.0, 10.0, valinit=0)
sdB = Slider(axdB, 'Energy B', -10.0, 10.0, valinit=0)
st = Slider(axt, 'Hopping', -5.0, 5.0, valinit=1.5)
sdx = Slider(axdx, 'Location x', 0.0, 1.0, valinit=0.5)
sdy = Slider(axdy, 'Location y', 0.0, 1.0, valinit=0.5)

#Making sure that the plot of the energy bands is updated
def update(val):
    dA = sdA.val
    dB = sdB.val
    t = st.val
    dx = sdx.val
    dy = sdy.val
    lattice = squarelat2(a, dA, dB, t, dx, dy)
    model = pb.Model(lattice, pb.translational_symmetry())
    solver = pb.solver.lapack(model)
    bands = solver.calc_bands([0, 0], [0, pi/a], [pi/a, pi/a], [0, 0])
    l1.set_ydata((bands.energy)[:,0])
    l2.set_ydata((bands.energy)[:,1])
    fig.canvas.draw_idle()
sdA.on_changed(update)
sdB.on_changed(update)
st.on_changed(update)
sdx.on_changed(update)
sdy.on_changed(update)

#A reset button that takes you back to the initial values of the sliders
resetax = plt.axes([0.79, 0.025, 0.11, 0.04])
resetb = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

def reset(event):
    sdA.reset()
    sdB.reset()
    st.reset()
    sdx.reset()
    sdy.reset()
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
    dx = sdx.val
    dy = sdy.val
    lattice = squarelat2(a, dA, dB, t, dx, dy)
    modellat = pb.Model(lattice, pb.primitive(a1=5,a2=5))
    plt.subplot(111, title="Lattice")
    modellat.plot()
    modellat.lattice.plot_vectors(position=[0.0,0.0])
    plt.show()
latb.on_clicked(showlat)

unitax = plt.axes([0.27, 0.025, 0.1, 0.04])
unitb = Button(unitax, 'Unit', color=axcolor, hovercolor='0.975')

def showunit(event):
    plt.figure(3)
    dx = sdx.val
    dy = sdy.val
    lattice = squarelat2(a, dA, dB, t, dx, dy)
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
