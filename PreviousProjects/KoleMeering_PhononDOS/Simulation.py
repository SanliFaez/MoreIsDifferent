#!/usr/bin/env python3

import numpy as np


class Simulation():

    def __init__(self):
        self.latticeConstants = np.array([400, 400, 400])  # in picometer
        self.speedOfSound = np.full(3, 6000e12)  # in picometer per second
        self.atomCount = 10  # amount of atoms for each direction

        # 3 for x,y,z and 1 to count boundary atoms properly
        self.atomCoords = np.empty((self.atomCount**3, 3+1))
        self.kStateCoords = np.empty((self.atomCount**3, 3+1))

        self.dispersionRelationType = 0  # 0 = linear, 1 = harmonic

        self.updateSimulationValues()

    def updateSimulationValues(self):
        """
        calculate the frequencyCutoff for the selected dispersionRelationType,
        set omegaList from 0 to the cutoff using atomCount as the number of
        steps
        """
        if self.dispersionRelationType == 0:
            self.freqCutoff = np.pi/max(self.latticeConstants) * \
                                min(self.speedOfSound)
        elif self.dispersionRelationType == 1:
            self.freqCutoff = 2*np.pi*1e13
            # 1e13 Hz, was a typical crystal vibration frequency we found here:
            # www.tf.uni-kiel.de/matwis/amat/iss/kap_4/illustr/s4_1_2.html

        self.omegaList = np.arange(0, self.freqCutoff,
                                   self.freqCutoff/self.atomCount)

    def generateCoords(self):
        """
        we only generate atoms in the first octant and count atoms at
        boundaries accordingly, this to speed up the calculation considerably
        """
        counter = 0
        max = self.atomCount
        for x in range(0, max):
            for y in range(0, max):
                for z in range(0, max):
                    nmbrOfNonZeros = int(bool(x)) + int(bool(y)) + int(bool(z))
                    if nmbrOfNonZeros == 0:  # origin
                        self.atomCoords[counter] = np.array([x, y, z, 1])
                    elif nmbrOfNonZeros == 1:  # on axis
                        self.atomCoords[counter] = np.array([x, y, z, 2])
                    elif nmbrOfNonZeros == 2:  # in xy, xz, yz plane
                        self.atomCoords[counter] = np.array([x, y, z, 4])
                    else:  # interior
                        self.atomCoords[counter] = np.array([x, y, z, 8])
                    counter += 1
        self.atomCoords[:, :3] *= self.latticeConstants

    def generateKStates(self):
        """
        alowed state are given by 2*pi*i/(N*a) with i an integer, N the number
        of atoms in a direction and a the lattice constant in that direction.
        The position of atoms is given by i*a, so we can convert atomCoords to
        kState by multiplying with 2pi and dividing by N*a^2
        """
        self.kStateCoords[:, :3] = (
            self.atomCoords[:, :3] * np.full(3, 2*np.pi) /
            (np.square(self.latticeConstants) * (self.atomCount*2 - 1)))
        self.kStateCoords[:, 3] = self.atomCoords[:, 3]

    def calcDOS(self):
        """
        calculates dos for the selected dispersionRelationType by counting
        states with frequency between zero and omega and taking the numerical
        derivative
        """
        steps = self.atomCount

        dos = np.zeros(steps)
        if self.dispersionRelationType == 0:
            for j in range(0, 3):
                kList = self.omegaList / self.speedOfSound[j]

                nList = np.zeros(steps)
                for kCoord in self.kStateCoords:
                    for i in range(0, steps):
                        if np.dot(kCoord[:3], kCoord[:3]) <= kList[i]*kList[i]:
                            nList[i:] += kCoord[3]
                            break
                dos += np.gradient(nList, self.freqCutoff/steps)

        elif self.dispersionRelationType == 1:
            a = np.mean(self.latticeConstants)
            omegaM = 2*np.pi*1e13  # vibration frequency of atoms in crystal
            kList = 2/a * np.arcsin(self.omegaList / omegaM)

            nList = np.zeros(steps)
            for kCoord in self.kStateCoords:
                for i in range(0, steps):
                    if np.dot(kCoord[:3], kCoord[:3]) <= kList[i]*kList[i]:
                        nList[i:] += kCoord[3]
                        break
            dos = np.gradient(nList, self.freqCutoff/steps)

        return dos
