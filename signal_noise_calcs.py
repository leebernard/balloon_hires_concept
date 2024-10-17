"""
This script is for calculating simple signal/noise for the hi-res feasibility study.

To keep things simple, this uses an Earth atmosphere absorption spectrum, which I happened to have lying around.
"""

import matplotlib
matplotlib.use("qt5agg")
import numpy as np
import matplotlib.pyplot as plt

from scipy.ndimage import gaussian_filter

# open files
gemini_trans_file = 'data/mktrans_zm_16_15.dat'
mk_trans_data = np.loadtxt(gemini_trans_file)












