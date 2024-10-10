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
from transit_model import scale_h

# constants
G = 6.674e-11  # m^3 kg^-1 s^-2
jovian_mass = 1.2668653e17 # m^3 s^-2
jovian_radius = 7.1492e7  # m/R_J
GM_j = jovian_mass / jovian_radius**2  # R_J^2 m s^-2

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

# partial fraction of water, according to Peter et al 2024
log_f_h2o = -3.80  # log base 10

p0 = 1  # assume complete opacity at 1 barr
mass_water = 18
mass_h2 = 2.3
water_ratio = 10**log_f_h2o
mass_average = (1 - water_ratio)*mass_h2 + water_ratio*mass_water

M_p = 1.76  # Jupiter masses
R_p = 1.21

g_p = GM_j * M_p/R_p**2

# smooth to R=40,000


# calculate cross correlation S/N






