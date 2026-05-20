#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 09:52:05 2018

@author: yann
"""

from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from astropy.convolution import convolve, convolve_fft
import scipy.io as sio
from scipy import signal
import progressbar


def psf2otf(psf, s):
    """
    Get OTF (Optical Transfer Function) from PSF (Point Spread Function)
    OTF is basically the Fourier Transform of the PSF, centered
    psf: PSF 
    s: shape of the result, zero-padding is used to center is Fourier Transform
    """
    
    # computes padding values
    sh = np.array(psf.shape)
    s = np.array(s)
    pad = s - sh
    
    # centers psf
    h_centered = np.pad(psf, ((pad[0]//2+1, pad[0]-pad[0]//2-1), (pad[1]//2+1, pad[1]-pad[1]//2-1)), mode='constant')

    plt.imshow(h_centered)
    plt.title("psf centered")
    plt.show()
    # Fourier transform (aka OTF) of the psf
    h_centered = np.fft.fftshift(h_centered)
    H = np.fft.fft2(h_centered, s)
    
    # Keep only real values (simple approximation)
    H = np.real(H)
    return H

def checkerboard(s=8):
    return np.kron([[1, 0] * 4, [0, 1] * 4] * 4, np.ones((s, s)))
