"""
This file is for calculating the optical parameters of the hi-res instrument
First, calculate the parameters for the igrins instrument.
Then translate those parameters to two different versions of hi-rest: one with a superbit (0.5 m telescope) platform, and the
other with a gigabit (1.35 m telescope) platform.
Reuse appropiate parameters from igrins, such as the grating and the resolution. Tweak as little as possible, to start.

Igrins has R~45,000, but only ~ 20,000 resolution elements. This is due to the gap between H and K, caused by the
atmospheric absorption peak. They require a 2K x 2K detector to image both spectrums

Number of illuminated grooves determines the number of resolution elements per order. IGRINs uses a lithographic
Si immersed grating. Si immersion increases the effective resolution by n (3.4). Uses a single detector.
Immersion grating has a 60 mK stability requirement, to prevent instablility in the index of refraction of Si.
"""

import numpy as np

D_gem = 8.1
F_gem = 16
D_super = 0.5
D_giga = 1.35

wl_igrins = np.linspace(1.47, 2.5, num=40000)  # bandpass wavelengths, um
F_igrins = 10
R_gem = 45000
phi_gem = np.radians(0.34/3600)  # arcseconds to radians. Typicak k-band Gemini seeing is 0.6-0.4 arcseconds
F_igrins = 8.8
f1_igrins = 250  # mm
n_grating = 3.435  # at 130 Kelvin, longward of 1 um
delta_igrins = np.radians(71.56)  # R3 grating
# delta_r1 = np.arctan(1)  # R1 grating example
grating_density = 36.5  # number of lines/mm
hband_orders = np.arange(98, 122+1, step=2)  # number of orders to cover k band
kband_orders = np.arange(72, 92+1, step=2)  # number of orders to cover h band
lam_b_hband = np.array((1823.59, 1788.03, 1753.89, 1721.08, 1689.52, 1659.15, 1629.15, 1601.71, 1574.53, 1548.30, 1522.97, 1498.50, 1474.85))  # nm
lam_b_kband = np.array((2467.88, 2402.10, 2339.80, 2224.62, 2171.27, 2120.49, 2072.09, 2025.92, 1981.81, 1939.65))  # nm

f_camera = 126.6  # mm
px_sampling = 3.66  # pixels per wavelength element
d1_igrins = 25  # mm

F_2 = f_camera/d1_igrins

'''Calculate the space the spectrum takes up'''
# assume theta is 1 degree
theta = np.radians(1.6)

alpha_igrins = delta_igrins + theta
beta_blaze = delta_igrins - theta
r_igrins = np.cos(alpha_igrins)/np.cos(beta_blaze)
# r should be ~1
print(f'r={r_igrins:.2f}')
fold1_clearance = 2 * F_igrins * d1_igrins * theta  # small angle approximation
print(f'f1 fold mirror clearance: {fold1_clearance:.2f} mm')

W_igrins = d1_igrins/np.sin(alpha_igrins)
sigma_igrins = 1/grating_density

lam_b_test = 2*sigma_igrins*1e6 * np.sin(delta_igrins) * np.cos(theta) * n_grating/hband_orders  # in nm

R_igrins = lam_b_hband*1e-9 / (phi_gem * D_gem) * hband_orders / (sigma_igrins * np.cos(alpha_igrins)) * d1_igrins
print(f'Resolution R={R_igrins}')

lam_blaze_igrins = 2*sigma_igrins/hband_orders * n_grating*np.sin(delta_igrins) * 1e6  # convert from mm to nm
# note: the above calculation is slightly off from IGRINS published numbers, with the magnitude of error depending on
# the wavelength. This is most likely due to wavelength dependency of n

free_spectral_range = lam_blaze_igrins/hband_orders

'''
Calculate the specs for the proposed hi-res instrument. 
Start with the direct specs of IGRINS, but with full band coverage (no gap between H and K band)
Calculate how much detector space I need.
Then start tweaking parameters to see if I can fit it onto one detector.
A good place to start is noting the spectrum in IGRINS is over-sampled, at 3.66 pixels per wavelength element
'''

hires_orders = np.arange(72, 122+1)
R_hires = 40000
delta_hires = delta_igrins
sigma_hires = sigma_igrins
alpha_hires = delta_hires + theta
beta_b_hires = delta_hires - theta
px_pitch = 18.e-6  # um
F_hires = 12  # assume F/10 telescope

wl_crit = 1.5e-6  # wavelength driving slit criteria, m
m_crit = np.round(n_grating * sigma_hires*1e-3 / wl_crit * (np.sin(beta_b_hires) + np.sin(alpha_hires)))
print(f'criteria order: {m_crit}')


d1_gem = R_gem * D_gem/2 * np.cos(alpha_igrins)/(np.sin(delta_igrins) * np.cos(theta)) *  phi_gem/2 * F_igrins/F_gem
print(f'Gemini collimated beam diameter: {d1_gem*1e3: .2f} mm')

phi_super = 2*wl_crit/D_super  # set slit sky angle to diffract limit at 1.5 um
slit_width = 2*wl_crit*F_hires*1e6  # convert m to um
print(f'hires slit wide: {slit_width} um')

print(f'hires slit sky angle, superbit: {np.degrees(phi_super)*3600: .2f} arcseconds')

d1_super = R_hires * wl_crit/2 * np.cos(alpha_hires) / (np.sin(delta_hires) * np.cos(theta)) * 1e3  # convert to mm
print(f'Hires collimated beam diameter, half meter telescope: {d1_super:.2f} mm')

f2_super = d1_super/wl_crit * 2*px_pitch
print(f'f camera, {D_super} m telescope: {f2_super} mm')

print('------------------------')
phi_giga = 2*wl_crit/D_giga
print(f'hires slit sky angle, gigabit: {np.degrees(phi_giga)*3600: .2f} arcseconds')
d1_giga = R_hires * wl_crit/2 * np.cos(alpha_hires) / (np.sin(delta_hires) * np.cos(theta)) * 1e3  # convert to mm
print(f'Hires collimated beam diameter, 1.35 meter telescope: {d1_giga:.2f} mm')

f2_giga = d1_giga/wl_crit * 2*px_pitch
print(f'f camera, {D_giga} m telescope: {f2_giga} mm')

f1_super = d1_super * F_hires
print(f'collimating optic: fp={f1_super: .1f}')




