"""
    MoreIsDifferent.methods.sinewave.py
    ==================================
    Example fundtion

    .. lastedit:: 17/11/2017
    .. sectionauthor:: Sanli Faez <s.faez@uu.nl>
"""
import numpy as np

def sine_wave(x, peak=1, wavelength=20, phase = 0):
    """generates a sine function

    Parameters
    ----------
    x: coordinate index, 1d array of numbers
    peak: peak value of the generated wave
    wavelength: wavelength
    phase: phase at x=0

    Returns
    -------
    waveform:
    """
    twopi = 2 * np.pi
    waveform = peak * np.sin(twopi * x / wavelength + phase)

    return waveform