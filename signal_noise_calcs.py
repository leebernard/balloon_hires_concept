"""
This script is for calculating simple signal/noise for the hi-res feasibility study.

To keep things simple, this uses an Earth atmosphere absorption spectrum, which I happened to have lying around.
"""

import matplotlib
matplotlib.use("qt5agg")
import numpy as np
import matplotlib.pyplot as plt

from scipy.ndimage import gaussian_filter

# housekeeping variables
debug=False
resolution = 40000
R_gem = 8.1/2  # m
R_super = 0.5/2  # m
R_giga = 1.35/2  # m

# open files
gemini_trans_file = 'data/mktrans_zm_16_15.dat'
mk_trans_data = np.loadtxt(gemini_trans_file)

wl = mk_trans_data[:, 0]  # um
raw_spectrum = mk_trans_data[:, 1]

# filter the data down to the resolution, using a gaussian
sigma = 1/2.355 * np.mean(wl)/np.mean(np.diff(wl)) * 1/resolution

filtered_spectrum = gaussian_filter(raw_spectrum, sigma)

if debug:
    # plot the results of the filter
    test_fig, test_ax = plt.subplots(figsize=(8, 6))
    test_ax.plot(wl, filtered_spectrum, label=f'R={resolution}')
    test_ax.plot(wl, raw_spectrum, label='Raw spectrum data', color='r', alpha=0.5)
    test_ax.set_xlabel('wavelength (um)')
    test_ax.set_ylabel('Fractional Transmission')
    test_ax.legend()


# calculate SNR estimates
planet_contrast = 1e-3
snr_gem = 200
oversample = 1/2 * filtered_spectrum.size / resolution
exposure_time = 120  # s

N_lines = np.sqrt(np.sum(1-filtered_spectrum)/3)
snr_cc = snr_gem * np.sqrt(exposure_time/120) * R_gem/R_gem * planet_contrast * np.sqrt(N_lines)

