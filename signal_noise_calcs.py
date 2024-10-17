"""
This script is for calculating simple signal/noise for the hi-res feasibility study.

To keep things simple, this uses an Earth atmosphere absorption spectrum, which I happened to have lying around.
"""

import matplotlib
matplotlib.use("qt5agg")
import numpy as np
import matplotlib.pyplot as plt

from scipy.ndimage import gaussian_filter

from toolkit import snr_calculator

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
exposure_time = 3600 * 4.7  # s

usable_spectrum = (wl > 1.56) * (wl < 1.62)
N_lines_gem = np.sum((1-filtered_spectrum[usable_spectrum])**2)
snr_cc_gem = snr_calculator(snr_gem, exposure_time, R_gem, planet_contrast, N_lines_gem, r_ref=R_gem)

print(f'SNR cc, Gemini: {snr_cc_gem: .2f}')

usable_spectrum = (wl > 1.47) * (wl < 2.5)
N_lines_super = np.sum((1-filtered_spectrum[usable_spectrum])**2)
snr_cc_superbit = snr_calculator(snr_gem, exposure_time, R_super, planet_contrast, N_lines_super, r_ref=R_gem)
print(f'SNR cc, Superbit platform: {snr_cc_superbit: .2f}')

snr_cc_gigabit = snr_calculator(snr_gem, exposure_time, R_giga, planet_contrast, N_lines_super, r_ref=R_gem)
print(f'SNR cc, Gigabit platform: {snr_cc_gigabit: .2f}')
