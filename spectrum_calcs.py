"""
This script is for comparing the spectrum access of IGRINS vs a balloon platform, with the goal of determining the
potential benefits of having access to the opaque windows in Earth's atmosphere.

The idea is that water is of high interest to exoplanet science. Unfortunately, Earth's atmosphere is opaque in the
majority of water spectral features, making those features unavailable to the large, ground-based high-resolution spectrographs
that are the current state-of-the-art. This script will quantify how spectral information would be gained by moving
IGRINS to a balloon platform.

For now, teat only water species
"""

'''
The cross correlation measurement SNR goes as follows.   Consider the raw SNR for the host star, which is about 200 per 
bin, after a 120s integration.  The cross correlation SNR is then:

SNR_cc = SNR*(exposure_time/120)^(1/2) (A/A_gemini)^(1/2) * (signal_planet/signal_star) * [ Sum_i line_depth_i ]^(1/2)

The ratio of the planet signal to the star signal (in the continuum) is about 10^(-3).  For Wasp 127b, their exposure 
time was 4.7 hours for a transit.  Consider the CO2 lines between 1.56 and 1.62 microns in your file 
mktrans_zm_16_15.dat .  The lines are over-sampled by a factor of about 3.  I find a [ Sum_i line_depth_i ] of about 20.

x,t=loadtxt('mktrans_zm_16_15.dat',unpack=True)
j=(x>1.56)*(x<1.62)
print ((1-t)[j].sum()/3)   # returns 20.7

So, SNR_cc = 200*sqrt(3600*4.7/120) * sqrt(1) * 1.e-3 * sqrt( 20.7 ) = 10.8 , which is about what they measured.

The SNR_cc for an EXCITE like instrument will go down as A^(1/2).  However, the line depth sum can become much larger, 
particularly for the water lines, which are deep and numerous. 

For example, if you could use everything between 1 and 2.5 microns:

j=(x>1)*(x<2.5)
print ((1-t)[j].sum()/3)   # returns 4261

So, the SNR_cc would be ~10 for a 0.5-meter telescope (as compared to 8-meter).   You could also likely burn more 
observing time as compared to Gemini.
'''

'''
The way I thought about his for Krishna's quals was:

SNR_cc = SNR*(exposure_time/120)^(1/2) (A/A_gemini)^(1/2) * (signal_planet/signal_star) * Nlines^(1/2)

Here, SNR = sqrt(signal_star), so SNR_planet = signal_plante/sqrt(signal_star) = SNR*(signal_planet/signal_star).  In 
principle you could more accurately write SNR_planet = signal_planet/sqrt(all_signal), but all_signal is approximately 
signal_star.

Nlines is the effect number of fully absorbing lines (ie, where the planet spectrum goes to zero.  This is determined 
from a cross correlation.

In the cross correlation of the model transmission spectrum T, one is correlating T with T plus noise.  The expected 
value at the peak is Sum (1-T)^2, and the variance is noise^2 * Sum (1-T)^2.  So, the SNR of
the cross correlation is [ Sum (1-T)^2 ]^(1/2) / noise.   Hence, a better calculation is Nlines = Sum (1-T)^2, summed 
over the usable spectral range.  

x,t=loadtxt('mktrans_zm_16_15.dat',unpack=True)
j=(x>1.56)*(x<1.62)  #  CO2 lines
Nlines = ((1-t[j])**2).sum()   # 10.4

Which can be compared to the full spectral range 1-2.5 microns:
j=(x>1)*(x<2.5)
Nlines = ((1-t[j])**2).sum() # 8534.1

This leads to an even larger increase in SNR_cc, and it also doesn't require worrying about the spectral sampling of T.


If you want to take into account the change in signal with wavelength, then you could also do:

SNR_cc = [ Sum planet_counts * (1-T)^2 ] / [ Sum star_counts * (1-T)^2 ]^(1/2) , summed over pixels or resolution 
elements.  

This would reduce to the previous formula when planet_counts ~ constant and star_counts ~ constant (with wavelength).
'''
# generate a water spectrum


# smooth to R=40,000


# calculate cross correlation S/N






