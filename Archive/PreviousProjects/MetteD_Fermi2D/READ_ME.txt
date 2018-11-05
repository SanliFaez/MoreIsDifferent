About the project

This project is a demonstration of how the band gap arises in the nearly free electron model. In the program I have used a square lattice and introduced a periodic potential. The size of the band gap can be controlled by changing the strength of the potential. The potential can also be turned off completely and we are left with the normal dispersion relation E = hbar/(2m)*(kx^2+ky^2).
In the program I have chosen to set hbar=1 and m=1.
It is also possible to plot the Fermi level. Depending on where this Fermi level is placed the material will either be a metal, a semi-conductor or an insulator. If one of the bands are completely full the material will either be a semi-conductor or an insulator depending on the size of the gap. If one of the bands are not completely full the electrons will be able to conduct and we have a metal.
If the atoms on the lattice each have one valence electron the lower band will be half full. For a semi-conductor the Fermi level will lie (approximately) in the middle of the band gap.
It is also possible to arrange the potential and Fermi level such that the Fermi level cuts two bands. This will result in a semi-metal.


How to control the program

* The strength of the potential can be  easiest regulated by changing the value of V0 (e.g. V0=3.0).
* The height of the Fermi level can be regulated by changing the value of Ef (e.g. Ef=5.0)
* More bands can be added to the plot by changing the xrange in line 71 (xrange(0,2) gives the two lowest bands xrange(0,3) the three lowest and so on)


Author
Mette Dybdahl Mortensen
Utrecht University
St.no. 5986133
