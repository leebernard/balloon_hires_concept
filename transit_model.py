"""
Functions for the transit model.

This was directly copy-pasted from my second project code. This is a very simple model, I expect to make heavy
changes.
"""

import numpy as np


# physical constants
k = 1.38e-23  # boltzmann constant k_b in J/K
amu_kg = 1.66e-27  # kg/amu
g_jovian = 24.79  # m/s^2
r_jovian = 7.1492e7  # meters
r_sun = 6.957e8  # meters
#
# def alpha_lambda(sigma_trace, xi, planet_radius, p0, T, mass, g, star_radius, sigma_filler=None):
#     '''
#
#     Parameters
#     ----------
#     sigma_trace
#     xi
#     planet_radius
#     p0
#     T
#     mass
#     g
#     star_radius
#     sigma_filler
#
#     Returns
#     -------
#     The eclipse depth as a function of wavelength
#     '''
#
#     # convert to meters
#     r_planet = r_jovian * planet_radius
#     r_star = r_sun * star_radius
#
#     z = z_lambda(sigma_trace=sigma_trace,
#                  xi=xi,
#                  p0=p0,
#                  planet_radius=planet_radius,
#                  mass=mass,
#                  T=T,
#                  g=g,
#                  sigma_filler=sigma_filler)
#
#     return (r_planet / r_star)**2 + (2 * r_planet * z)/(r_star**2)



def scale_h(mass, T, g):
    '''
    Calculates the scale height

    Parameters
    ----------
    mass: float
        average mass of atmosphere species, in atomic units
    T: float
        Average temperature of atmosphere
    g: float
        Gravitational constant

    Returns
    -------
    The scale height of an atmosphere
    '''
    return k*T/(mass*amu_kg * g)



def z_lambda(sigma_trace, xi, p0, planet_radius, mass, T, g, sigma_filler=None):
    '''

    Parameters
    ----------
    sigma_trace: array
        Absorption cross-section of atmosphere species as a function of wavelength
    p0: float
        Reference pressure of atmosphere; pressure at z=0
    planet_radius: float
        Minimum radius of planet
    mass: float
        mass of trace atomic species
    T: float
        Effective temperature of planet
    g: float
        gravity of the planet, in m/s
    sigma_filler: float
        cross-section of the filler gas

    Returns
    -------
    z: float, array
        The amount by which the planet's occultation disk is increased by
        opacity of the atmosphere, as a function of wavelength.
    '''
    # convert planet radius to meters
    r_p = r_jovian * planet_radius
    # convert from bars to pa
    pressure = p0 * 100000

    # g = gravity(planet_mass, planet_radius)
    h = scale_h(mass, T, g)

    if sigma_filler is not None:
        # calculate average cross section
        sigma = (1 - np.sum(xi))*sigma_filler + np.sum(xi*sigma_trace, axis=0)
    else:

        sigma = np.sum(xi*sigma_trace, axis=0)

    # set equiv scale height to 0.56 (Line and Parmenteir 2016)
    tau_eq = 0.56

    # calculate beta
    beta = pressure / tau_eq * np.sqrt(2*np.pi*r_p)
    return h * np.log(sigma * 1/np.sqrt(k*mass*amu_kg*T*g) * beta)




