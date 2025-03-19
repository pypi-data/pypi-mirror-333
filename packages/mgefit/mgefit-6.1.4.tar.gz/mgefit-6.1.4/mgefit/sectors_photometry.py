"""
Copyright (C) 1999-2025, Michele Cappellari

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

Modification History
--------------------
- V1.0.0: First implementation for the NGC2681 photometric modeling.
          Michele Cappellari, ESO Garching, 27 September 1999
- V2.0.0: Major revisions, to use it with MGE_FIT_SECTORS. Leiden, January 2000, MC
- V2.1.0: Further updates, Padova, August 2000, MC
- V2.1.1: Added compilation options. MC, Leiden, 20 May 2002
- V2.1.2: Allow for N_SECTORS=1 to get a single profile centered at a given PA.
          Use biweight mean instead of sigma-clipped mean. MC, Leiden, 30 April 2004
- V2.1.3: Reduced amount of verbose output. MC, Leiden, 24 October 2004
- V2.1.4: Replaced LOGRANGE keyword in example with the new MAGRANGE. MC, Leiden, 1 May 2005
- V2.1.5: Forces image to be positive when computing weighted radius
          to prevent possible negative radii at large radii. Thanks to Michael Williams
          for reporting the problem and the fix. MC, Oxford, 16 February 2009
- V3.0.0: Translated from IDL into Python. MC, Aspen Airport, 8 February 2014
- V3.0.1: Support both Python 2.6/2.7 and Python 3.x. MC, Oxford, 25 May 2014
- V3.1.0: Improved image visualization of sampled photometric grid.
          Sample angles uniformly in eccentric anomaly rather than polar angle.
          Removed Scipy dependency. MC, Oxford, 23 September 2014
- V3.1.1: Show badpixels as empty in checkerboard plot.
          Define input badpixels as a boolean mask. MC, Oxford, 30 May 2015
- V3.1.2: Stop profile if cnt <= 0. MC, Paris, 7 April 2016
- V3.1.3: Use interpolation='nearest' to avoid crash on MacOS. MC, Oxford, 14 June 2016
- V3.1.4: Fix NaN in biweight_mean() when most values are zero.
          This can happen with synthetic images from N-body simulations.
          Check for NaN in input image. MC, Oxford, 13 February 2017
- V3.1.5: Properly drop last radial value from checkerboard plot. MC, Oxford, 9 May 2017
- V3.1.6: Fixed DeprecationWarning in Numpy 1.9. MC, Oxford, 11 August 2020
- Vx.x.xx: Additional changes are now documented in the global CHANGELOG.rst 
           file of the MgeFit package

"""
import numpy as np
import matplotlib.pyplot as plt

#----------------------------------------------------------------------------

def biweight_mean(y, itmax=10):
    """
    Biweight estimate of the location (mean).
    Implements the approach described in
    "Understanding Robust and Exploratory Data Analysis"
    Hoaglin, Mosteller, Tukey ed., 1983

    """
    y = np.ravel(y)
    c = 6.
    fracmin = 0.03*np.sqrt(0.5/(y.size - 1))
    y0 = np.median(y)
    mad = np.median(np.abs(y - y0))
    if mad == 0:   # can happen when most pixels are zero
        return np.mean(y)

    for it in range(itmax):
        u2 = ((y - y0)/(c*mad))**2
        u2 = u2.clip(0, 1)
        w = (1 - u2)**2
        y0 += np.sum(w*(y - y0))/np.sum(w)
        mad_old = mad
        mad = np.median(np.abs(y - y0))
        frac = np.abs(mad_old - mad)/mad
        if frac < fracmin:
            break

    return y0

#----------------------------------------------------------------------------

def coordinates(q, pos_ang, xc, yc, s):

    ang = np.radians(90 - pos_ang)              # x-axis is major axis
    x, y = np.ogrid[-xc:s[0] - xc, -yc:s[1] - yc]
    x, y = x*np.cos(ang) - y*np.sin(ang), x*np.sin(ang) + y*np.cos(ang)
    x2, y2 = x**2, y**2
    rad = np.sqrt(x2 + y2)                      # Radius
    rell = np.sqrt(x2 + y2/q**2)                # Elliptical radius
    ecc = np.arctan2(np.abs(y/q), np.abs(x))    # Eccentric anomaly [0, pi/2]
 
    return rad, rell, ecc

#----------------------------------------------------------------------------

class sectors_photometry:
    """
    mge.sectors_photometry
    ======================

    Purpose
    -------
    
    Perform photometry of a galaxy image along sectors equally spaced in angle.

    This routine assumes four-fold symmetry, where measurements from the four
    quadrants are averaged together. It is useful to generate the input
    photometry required by the MGE fitting routine `mge_fit_sectors`.

    Parameters
    ----------
    img : 2D array-like
        The galaxy image.
    eps : float
        The galaxy "average" ellipticity: ``eps = 1 - b/a = 1 - q'``.
        Photometry will be measured along elliptical annuli with constant
        axial ellipticity `eps`. This parameter, along with `theta`, `xpeak`,
        and `ypeak`, can be measured with the routine `find_galaxy`.
    theta : float
        The position angle (in degrees), measured counterclockwise from the
        image Y-axis to the galaxy's major axis.
    xpeak : float
        The X-coordinate of the galaxy center in pixels.
    ypeak : float
        The Y-coordinate of the galaxy center in pixels.
    badpixels : 2D boolean array, optional
        Boolean image mask with the same dimensions as `img`. `True` values
        are masked and ignored in the photometry.
    n_sectors : int, optional
        Number of sectors equally spaced in eccentric anomaly from the galaxy's
        major axis to the minor axis (one quadrant). Defaults to 19, which
        corresponds to a sector width of 5 degrees.
    mask : 2D boolean array, optional
        Boolean image mask with the same dimensions as `img`. `False` values
        are masked and ignored in the photometry. This is an alternative way
        of specifying `badpixels` (note: `mask = ~badpixels`).
    minlevel : float, optional
        The minimum `counts` level to include in the photometry. The measurement
        along one profile stops when the `counts` first go below this level.
    sector_width : float, optional
        The angular width of each sector in degrees (default: 5 degrees).
    plot : bool, optional
        If `True`, produces a plot of the photometric grid (default: `False`).

    Returns
    -------
    radius : 1D array
        The radius of the surface brightness measurements from the galaxy center
        (units: pixels).
    angle : 1D array
        The polar angle of the surface brightness measurements, measured from the
        galaxy's major axis (units: degrees).
    counts : 1D array
        The actual surface brightness measurements (units: counts) at the specified
        polar coordinates. Has the same length as `radius` and `angle`.

    Notes
    -----
    This function assumes a galaxy image with four-fold symmetry. It averages
    measurements across all four quadrants.

    Examples
    --------
    >>> import mgefit as mge
    >>> s = mge.sectors_photometry(img, eps, theta, xpeak, ypeak)

    References
    ----------
    Cappellari, M. (2002). MNRAS, 333, 400.
    https://ui.adsabs.harvard.edu/abs/2002MNRAS.333..400C
    """

    def __init__(self, img, eps, ang, xc, yc, badpixels=None,
                 n_sectors=19, mask=None, minlevel=0, plot=False):
        
        assert np.all(np.isfinite(img)), "Input image contains NaN"
        xc, yc = int(round(xc)), int(round(yc))
        s = img.shape
        q = 1 - eps
        minlevel = max(minlevel, 0)

        rad, rell, ecc = coordinates(q, ang, xc, yc, s)
        rad[xc, yc] = 0.38  # Average radius within the central pixel
        rell[xc, yc] = 0.38

        if plot:
            self.grid = np.zeros_like(img, dtype=bool)

        # Sample radii with 24 isophotes per decade: factor 1.1 spacing.
        # Sample eccentric anomaly with n_sectors from 0-pi/2

        rell = np.round(24.2*np.log10(rell)).astype(int)
        ecc = np.round(2*(n_sectors - 1)/np.pi*ecc).astype(int)

        if mask is not None:
            assert mask.dtype == bool, "MASK must be a boolean array"
            assert mask.shape == img.shape, "MASK and IMG must have the same shape"
            assert badpixels is None, "BADPIXELS and MASK cannot be used together"
            badpixels = ~mask

        if badpixels is not None:
            assert badpixels.dtype == bool, "BADPIXELS must be a boolean array"
            assert badpixels.shape == img.shape, "BADPIXELS and IMG must have the same shape"
            ecc[badpixels] = -1  # Negative flag value

        self.radius = self.counts = self.angle = self.npix = []
        eccGrid = np.linspace(0, np.pi/2, n_sectors)       # Eccentric anomaly
        angGrid = np.degrees(np.arctan(np.tan(eccGrid)*q)) # Polar angle

        for k, angj in enumerate(angGrid):
            radj, cntj, npixj = self._profile(
                    img, xc, yc, rad, rell, ecc, k, plot, minlevel)
            self.radius = np.append(self.radius, radj)
            self.counts = np.append(self.counts, cntj)
            self.npix = np.append(self.npix, npixj)
            self.angle = np.append(self.angle, np.full_like(radj, angj))

        if plot:
            plt.imshow(np.log(img.clip(img[xc, yc]/1e4)), cmap='hot',
                       origin='lower', interpolation='nearest')
            if badpixels is not None:
                self.grid[badpixels] = False
            plt.imshow(self.grid, cmap='binary', alpha=0.3,
                       origin='lower', interpolation='nearest')
            plt.xlabel("pixels")
            plt.ylabel("pixels")

#----------------------------------------------------------------------------

    def _profile(self, data, xc, yc, rad, rell, ecc, k, plot, minlevel):

        if ecc[xc, yc] != -1:
            ecc[xc, yc] = k  # Always include central pixel unless bad
        sector = np.flatnonzero(ecc == k)
        irad = rell.flat[sector]
        levels = np.unique(irad)  # get unique levels within sector
        cnt, radius, npix = np.empty((3, levels.size))

        for j, lev in enumerate(levels):
            sub = sector[irad == lev]
            npix[j] = sub.size
            if npix[j] > 9:   # Evaluate a biweight mean
                cnt[j] = biweight_mean(data.flat[sub])
            else:
                cnt[j] = np.mean(data.flat[sub])  # Usual mean

            if (cnt[j] <= minlevel):   # drop last value
                cnt = cnt[:j]
                radius = radius[:j]
                npix = npix[:j]
                break

            # Luminosity-weighted average radius in pixels
            flx = data.flat[sub].clip(0)
            radius[j] = np.sum(rad.flat[sub]*flx)/np.sum(flx)

            if plot:
                self.grid.flat[sub] = (lev + k % 2) % 2

        j = np.argsort(radius)
        cnt = cnt[j]
        radius = radius[j]

        return radius, cnt, npix

#----------------------------------------------------------------------------
