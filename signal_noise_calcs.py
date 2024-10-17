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
resolution = 40000


# open files
gemini_trans_file = 'data/mktrans_zm_16_15.dat'
mk_trans_data = np.loadtxt(gemini_trans_file)

wl = mk_trans_data[:, 0]  # um
raw_spectrum = mk_trans_data[:, 1]

# filter the data down to the resolution, using a gaussian
sigma = 1/2.355 * np.mean(wl)/np.mean(np.diff(wl)) * 1/resolution

filtered_spectrum = gaussian_filter(raw_spectrum, sigma)

# plot the results of the filter
test_fig, test_ax = plt.subplots(figsize=(8, 6))
test_ax.plot(wl, filtered_spectrum, label=f'R={resolution}')
test_ax.plot(wl, raw_spectrum, label='Raw spectrum data', color='r', alpha=0.5)
test_ax.set_xlabel('wavelength (um)')
test_ax.set_ylabel('Fractional Transmission')
test_ax.legend()





