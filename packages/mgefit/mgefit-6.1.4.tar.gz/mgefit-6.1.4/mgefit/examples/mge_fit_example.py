#!/usr/bin/env python

"""
    This example illustrates how to obtain an MGE fit from a galaxy image
    using the mge.fit_sectors package and how to verify the results.

    V1.0.0: Translated NGC4342 example from the corresponding IDL version.
        Michele Cappellari, Aspen Airport, 8 February 2014
    V1.0.1: Fixed incorrect offset in high-res contour plot.
        Use arcsec pixel scale. MC, Oxford, 18 September 2014
    V1.1.0: Translated M32 example of fitting to two images simultaneously.
        MC, Oxford, 18 June 2015
    V1.1.1: Support both Pyfits and Astropy to read FITS files.
        MC, Oxford, 23 October 2015
    V1.1.2: Make files paths relative to this file, to run the example
        from any directory. MC, Oxford, 20 January 2017
    V1.1.3: Included fit_1d() example. Added important note about
        mge.fit_sectors_regularized(). MC, Oxford, 14 February 2017
    V1.2.0: Illustrates how to efficiently mask an object before MGE fitting.
        Included dist_circle() function. MC, Oxford, 17 March 2017
    V1.3.0: Modified comment about import of mge.fit_sectors_regularized.
        Thanks to Evgeny Vasilyev (Oxford) for the suggestion.
        Included fit_ngc5831_twist() example and corresponding imports.
        MC, Oxford, 27 July 2017
    V1.3.1: Make path relative to package to run the example from any directory.
        MC, Oxford, 17 April 2018
    V1.4.0: Use new keyword `minlevel` in `mge.print_contours`.
        MC, Oxford, 31 March 2023
    V1.4.1: Use new single-line mgefit import. MC, Oxford, 17 January 2025

"""

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from pathlib import Path

import mgefit as mge

#----------------------------------------------------------------------------

def dist_circle(xc, yc, s):
    """
    Returns an array in which the value of each element is its distance from
    a specified center. Useful for masking inside a circular aperture.

    The (xc, yc) coordinates are the ones one can read on the figure axes
    e.g. when plotting the result of my mge.find_galaxy() procedure.

    """
    x, y = np.ogrid[-yc : s[0] - yc, -xc : s[1] - xc]   # note yc before xc
    rad = np.sqrt(x**2 + y**2)

    return rad

#----------------------------------------------------------------------------

def fit_1d():
    """
    Usage example for mge.fit_1d().
    This example reproduces Figure 3 in Cappellari (2002)
    https://ui.adsabs.harvard.edu/abs/2002MNRAS.333..400C
    It takes <1s on a 2.5 GHz computer

    """
    n = 300  # number of sampled points
    x = np.geomspace(0.01, 300, n)  # logarithmically spaced radii
    y = (1 + x)**-4  # The profile *must* be logarithmically sampled!
    plt.clf()
    p = mge.fit_1d(x, y, ngauss=16, plot=True)
    plt.pause(1)  # allow the plot to appear in certain situations

#----------------------------------------------------------------------------

def fit_m32():
    """
    This procedure reproduces Figures 6-7 in Cappellari (2002)
    https://ui.adsabs.harvard.edu/abs/2002MNRAS.333..400C

    This example illustrates how to fit multiple images together and how
    to mask an object before MGE fitting.

    We model an HST/WFPC2/F814W image of M32 and an I-band ground-based one.

    """
    scale1 = 0.0455     # (arcsec/pixel) PC1. This is used as scale and flux reference!
    scale2 = 0.549      # (arcsec/pixel) ING (Peletier 1993)
    scaleRatio = scale1/scale2
    fluxRatio = 0.9579  # = flux1/flux2 (ratio of observed counts/pixel at give radius)

    # IMPORTANT: use the *same* eps to run mge.sectors_photometry on both images
    eps = 0.2

    # Perform photometry on the HST/WFPC2/F814W (I-band) image
    # The geometric parameters below were obtained using my mge.find_galaxy program
    ang1 = 165.4
    xc1 = 377
    yc1 = 314

    package_dir = Path(mge.__file__).parent  # path of mgefit

    file = package_dir / 'images/m32_f814w_pc.fits'
    hdu = fits.open(file)
    img1 = hdu[0].data
    img1 -= 4.48  # subtract sky obtained by matching the profiles in the region of overlap

    plt.clf()
    s1 = mge.sectors_photometry(img1, eps, ang1, xc1, yc1, minlevel=0, plot=1)
    plt.pause(1)  # Allow plot to appear on the screen

    # Perform photometry on Peletier (1993) ING/I-band image
    # The geometric parameters below were obtained using my mge.find_galaxy program
    ang2 = 22.9
    xc2 = 376
    yc2 = 184

    file = package_dir / 'images/m32_i.fits'
    hdu = fits.open(file)
    img2 = hdu[0].data

    sky, skysig = mge.sky_level(img2, plot=True)  # estimate sky level
    plt.pause(1)    # Allow plot to appear on the screen
    
    img2 -= sky     # subtract sky
    minlevel = skysig/2  # minimum level for the photometry

    # Illustrates how to mask an object.
    # IMPORTANT: The masking of such a small star is actually *totally*
    # unnecessary, as the procedure is very robust to *much* larger residuals.
    # Here I simply show how the masking can be done in principle.
    r = dist_circle(216, 542, img2.shape)  # distance matrix from (216, 542)
    mask = r > 30                 # selects pixels more distant than 30 pixels

    plt.clf()
    s2 = mge.sectors_photometry(img2, eps, ang2, xc2, yc2, minlevel=minlevel, 
                                plot=1, mask=mask)
    plt.pause(1)  # Allow plot to appear on the screen
    s2.radius /= scaleRatio  # Bring all radii and fluxes on the same scale
    s2.counts *= fluxRatio

    # Exclude pixels at small radii (<3") in Peletier's image to avoid
    # PSF effects and merges the profiles of the different images.
    # The HST image is used as flux and spatial scale reference,
    # the ground-based data were simply scaled to the HST units.
    w = s2.radius > 3/scale1
    radius = np.append(s1.radius, s2.radius[w])
    angle = np.append(s1.angle, s2.angle[w])
    counts = np.append(s1.counts, s2.counts[w])

    # The PSF needs to be the one for the high-resolution image used in the centre.
    # Here this is the WFPC2/PC1/F814W image (we use a Gaussian PSF for simplicity)
    sigmapsf = 0.8
    ngauss = 11

    # Do the actual MGE fit
    # *********************** IMPORTANT ***********************************
    # For the final publication-quality MGE fit one should include the line:
    #
    # from mge.fit_sectors_regularized import mge.fit_sectors_regularized as mge.fit_sectors
    #
    # at the top of this file and re-run the procedure.
    # See the documentation of mge.fit_sectors_regularized for details.
    # *********************************************************************
    plt.clf()
    m = mge.fit_sectors(radius, angle, counts, eps, ngauss=ngauss,
                        sigmapsf=sigmapsf, scale=scale1, plot=1, linear=0)
    plt.pause(1)  # Allow plot to appear on the screen

    plt.clf()
    plt.subplot(121)
    # Plot MGE contours of the HST image
    mge.print_contours(img1, ang1, xc1, yc1, m.sol, scale=scale1,
                       binning=4, sigmapsf=sigmapsf)

    # Scale the solution parameters to the ground-based image
    m.sol[0] *= scaleRatio**2/fluxRatio  # Gaussians total counts
    m.sol[1] *= scaleRatio               # sigma of the Gaussians
    sigmapsf = 1/2.35  # seeing FWHM = 1.0 arcsec for the ground based image

    plt.subplot(122)
    # Plot MGE contours of the ground-based image
    mge.print_contours(img2, ang2, xc2, yc2, m.sol, scale=scale2, binning=7,
                       sigmapsf=sigmapsf, minlevel=minlevel, mask=mask)
    plt.pause(1)  # Allow plot to appear on the screen

#----------------------------------------------------------------------------

def fit_ngc4342():
    """
    This procedure reproduces Figures 8-9 in Cappellari (2002)
    https://ui.adsabs.harvard.edu/abs/2002MNRAS.333..400C
    This example illustrates a simple MGE fit to one single HST/WFPC2 image.

    """
    package_dir = Path(mge.__file__).parent  # path of mgefit

    file = package_dir / 'images/ngc4342_f814w_pc.fits'
    hdu = fits.open(file)
    img = hdu[0].data

    skylev = 0.55   # counts/pixel
    img -= skylev   # subtract sky
    scale = 0.0455  # arcsec/pixel
    minlevel = 0.5  # counts/pixel
    ngauss = 12

    # Here we use an accurate four gaussian MGE PSF for
    # the HST/WFPC2/F814W filter, taken from Table 3 of
    # Cappellari et al. (2002, ApJ, 578, 787)

    sigmapsf = [0.494, 1.44, 4.71, 13.4]      # In PC1 pixels
    normpsf = [0.294, 0.559, 0.0813, 0.0657]  # total(normpsf)=1

    # Here we use mge.find_galaxy directly inside the procedure. Usually you may want
    # to experiment with different values of the FRACTION keyword, before adopting
    # given values of Eps, Ang, Xc, Yc.
    plt.clf()
    f = mge.find_galaxy(img, fraction=0.04, plot=1)
    plt.pause(1)  # Allow plot to appear on the screen

    # Perform galaxy photometry
    plt.clf()
    s = mge.sectors_photometry(img, f.eps, f.theta, f.xpeak, f.ypeak, 
                               minlevel=minlevel, plot=1)
    plt.pause(1)  # Allow plot to appear on the screen

    # Do the actual MGE fit
    # *********************** IMPORTANT ***********************************
    # For the final publication-quality MGE fit one should include the line
    # "from mge.fit_sectors_regularized import mge.fit_sectors_regularized"
    # at the top of this file, rename mge.fit_sectors() into
    # mge.fit_sectors_regularized() and re-run the procedure.
    # See the documentation of mge.fit_sectors_regularized for details.
    # *********************************************************************
    plt.clf()
    m = mge.fit_sectors(s.radius, s.angle, s.counts, f.eps,
                        ngauss=ngauss, sigmapsf=sigmapsf, normpsf=normpsf,
                        scale=scale, plot=1, bulge_disk=0, linear=0)
    plt.pause(1)  # Allow plot to appear on the screen

    # Show contour plots of the results. Bin 9x9 pixels to reduce noise.
    plt.clf()
    plt.subplot(121)
    mge.print_contours(img, f.theta, f.xpeak, f.ypeak, m.sol, scale=scale,
                       sigmapsf=sigmapsf, normpsf=normpsf, binning=9, 
                       minlevel=minlevel)

    # Plot the central part of the image at high resolution without binning.
    # The MGE is centred to fractional pixel accuracy to ease visual comparison.
    plt.subplot(122)
    mge.print_contours(img, f.theta, f.xmed, f.ymed, m.sol, scale=scale, 
                       sigmapsf=sigmapsf, normpsf=normpsf)
    plt.xlim(-2, 2)
    plt.ylim(-2, 2)

    plt.pause(1)  # Allow plot to appear on the screen

#----------------------------------------------------------------------------

def fit_ngc5831_twist():

    """
    This procedure reproduces Figures 11-12 in Cappellari (2002)
    https://ui.adsabs.harvard.edu/abs/2002MNRAS.333..400C

    """
    # These parameters are given by mge.find_galaxy for the mosaic image
    skylevel = 13.0
    sigmapsf = 0.4  # pixels
    eps = 0.28
    ang = 141.0  # major axis in the inner regions (gives a starting guess for the PA)
    xc = 974
    yc = 969
    ngauss = 11
    minlevel = 2.0
    scale = 0.100

    package_dir = Path(mge.__file__).parent  # path of mgefit

    file = package_dir / 'images/ngc5831_f702w_mosaic.fits'
    hdu = fits.open(file)
    img = hdu[0].data

    mask = img > 0   # mask before sky subtraction
    img -= skylevel

    # Mask a nearby galaxy
    mask &= dist_circle(1408.1, 357.7, img.shape) > 200

    # Perform galaxy photometry
    plt.clf()
    s = mge.sectors_photometry_twist(img, ang, xc, yc, minlevel=minlevel, plot=1, mask=mask)
    plt.pause(1)  # Allow plot to appear on the screen

    plt.clf()
    m = mge.fit_sectors_twist(s.radius, s.angle, s.counts, eps, ngauss=ngauss,
                              sigmapsf=sigmapsf, scale=scale, plot=1, negative=True)
    plt.pause(1)  # Allow plot to appear on the screen

    # Show contour plots of the results
    plt.clf()
    mge.print_contours_twist(img, ang, xc, yc, m.sol, scale=scale, binning=15,
                             sigmapsf=sigmapsf, minlevel=minlevel, mask=mask)
    plt.pause(1)  # Allow plot to appear on the screen


#----------------------------------------------------------------------------

if __name__ == '__main__':

    print("\nFitting 1-dim profile-----------------------------------\n")
    fit_1d()

    print("\nFitting M32---------------------------------------------\n")
    fit_m32()

    print("\nFitting NGC4342-----------------------------------------\n")
    fit_ngc4342()

    print("\nFitting NGC5831 twist-----------------------------------\n")
    fit_ngc5831_twist()
