"""
Copyright (C) 2017-2025, Michele Cappellari

E-mail: michele.cappellari_at_physics.ox.ac.uk

Updated versions of the software are available from my web page
https://purl.org/cappellari/software

If you have found this software useful for your research, 
I would appreciate an acknowledgement to the use of
"the MGE fitting method and software by Cappellari (2002)".

https://ui.adsabs.harvard.edu/abs/2002MNRAS.333..400C

This software is provided as is without any warranty whatsoever.
Permission to use, for non-commercial purposes is granted.
Permission to modify for personal or internal use is granted,
provided this copyright and disclaimer are included unchanged
at the beginning of the file. All other rights are reserved.
In particular, redistribution of the code is not allowed.

#####################################################################

Changelog
---------
- V1.0.0: Written by Michele Cappellari, Oxford, 20 March 2017
- V1.1.0: Adapted for distribution in the MgeFit package, 10 March 2025

"""
import numpy as np
import matplotlib.pylab as plt
from astropy.stats import biweight_scale, biweight_location

from capfit.capfit import capfit

###############################################################################

def sky_level(img, plot=False, itmax=5):
    """
    Estimate the sky background level by robustly fitting a Gaussian to the
    image histogram.

    This procedure should be used when the majority of the pixels in the image
    are sky background. It cannot be used when the galaxy fills the whole image.

    This function fits a Gaussian function to the histogram of the image counts
    to estimate the sky background level. The algorithm assumes that the sky
    counts follow a Gaussian distribution, with a positive tail potentially
    affected by real sources (e.g., galaxies) and an unperturbed negative tail.
    The fitting process is iterative, continuing until the change in the
    estimated mean is smaller than its error or until the maximum number of
    iterations is reached.

    Parameters
    ----------
    img : array_like
        The input image data from which the sky level is computed.
    plot : bool, optional
        If True, generate diagnostic plots illustrating the histogram, the
        Gaussian fit, and the fitted range. Default is False.
    itmax : int, optional
        The maximum number of fitting iterations to perform. Default is 5.

    Returns
    -------
    mean : float
        The estimated mean value of the sky (background) distribution.
    sigma : float
        The estimated standard deviation of the sky distribution.

    Notes
    -----
    The initial estimates for the mean and sigma are computed using robust
    statistics (via biweight_location and biweight_sigma). A histogram of the image
    counts is then constructed over a range defined by these initial values. In
    each iteration, an asymmetric range is selected around the current mean,
    and a Gaussian model is fitted to the histogram data in this range. The
    iterative process terminates when the change in the mean is less than the
    estimated error from the fit.
    """
    # Initial estimates
    mean0 = biweight_location(img)
    sig0 = biweight_scale(img)

    # Plotted range
    maxcnt = mean0 - 5*sig0
    mincnt = mean0 + 5*sig0

    yhist, hbin = np.histogram(img, range=(maxcnt, mincnt), bins='auto')
    xhist = (hbin[1:] + hbin[:-1])/2
    ymax0 = yhist.max()

    for j in range(itmax):  # Do at most itmax iterations

        # Asymmetric fitted range
        x1 = mean0 - 2.5*sig0
        x2 = mean0 + 0.5*sig0

        w = (xhist > x1) & (xhist < x2) & (yhist > 0)
        xgood  = xhist[w]
        ygood = yhist[w]

        gau = lambda peak, x0, sig: peak*np.exp(-0.5*((x0 - xgood)/sig)**2) 
        resid = lambda pars: gau(*pars) - ygood
        p0 = [ymax0, mean0, sig0]
        sol = capfit(resid, p0)

        if abs(sol.x[1] - mean0) < sol.x_err[1]*np.sqrt(sol.chi2/len(sol.x)):
            break

        ymax0, mean0, sig0 = sol.x

    if plot:
        plt.clf()
        plt.plot(xhist, yhist, 'o', c='limegreen')
        plt.plot(xgood, ygood, 'bo')
        xgood = xhist
        plt.plot(xhist, gau(*sol.x), 'r')
        plt.axvline(x=sol.x[1], color='r')
        plt.axvspan(x1, x2, alpha=0.3, color='gold')
        plt.xlabel('Counts')
        plt.ylabel('Number of Pixels')

    return sol.x[1:]    # mean, sigma

###############################################################################
