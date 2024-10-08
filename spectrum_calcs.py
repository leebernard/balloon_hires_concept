"""
This script is for comparing the spectrum access of IGRINS vs a balloon platform, with the goal of determining the
potential benefits of having access to the opaque windows in Earth's atmosphere.

The idea is that water is of high interest to exoplanet science. Unfortunately, Earth's atmosphere is opaque in the
majority of water spectral features, making those features unavailable to the large, ground-based high-resolution
spectrographs that are the current state-of-the-art. This script will quantify how spectral information would be gained
by moving IGRINS to a balloon platform.

For now, teat only water species
"""
import matplotlib
matplotlib.use("qt5agg")
import numpy as np
import matplotlib.pyplot as plt

from toolkit import open_cross_section

# wavelenght range
wl_start = 1.47
wl_end = 2.5
wn_end = 1e4/wl_start  # wavenumber start is reversed from wavelength start
wn_start = 1e4/wl_end


# generate a water spectrum
water_filename = './line_lists/H2O_30mbar_1500K.txt'

wno_water, cross_sections_water = open_cross_section(water_filename, wn_range=(wn_start, wn_end))

wl_water = 1e4/wno_water

fig, ax = plt.subplots(figsize=(8,6))
ax.plot(wl_water, cross_sections_water, label='H2O, 30 mb 1500 K')

ax.set_xlabel('wavelength (um)')
ax.set_ylabel('absorption cross-section')
# smooth to R=40,000


# calculate cross correlation S/N






