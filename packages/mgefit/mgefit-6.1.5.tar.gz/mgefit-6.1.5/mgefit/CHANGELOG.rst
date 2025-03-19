
Changelog
---------

V6.1.5: MC, Oxford, 11 March 2025
+++++++++++++++++++++++++++++++++

- Introduced a new, convenient single-line import: ``import mgefit as mge``.  
  Previous imports such as:  

  .. code-block:: python  

    from mgefit.find_galaxy import find_galaxy  
    from mgefit.mge_fit_1d import mge_fit_1d  
    from mgefit.mge_fit_sectors import mge_fit_sectors  

    f = find_galaxy(...)  
    m = mge_fit_1d(...)  
    m = mge_fit_sectors(...)  

  Can now be simplified as:  

  .. code-block:: python  

    import mgefit as mge  

    f = mge.find_galaxy(...)  
    m = mge.fit_1d(...)  
    m = mge.fit_sectors(...)  

- ``mge.fit_sectors``: Resolved a bug in the docstring usage example.  
- ``mge.fit_sectors``: Added validation to ensure ``sigmapsf`` matches the size
  of ``normpsf`` when it is provided as a scalar.  
- ``mge.find_galaxy``: Incorporated the pixel indices ``.ind`` of the selected
  region into the output class attributes.  
- ``mge.fit_1d``: Expanded the docstring with additional details, based on
  feedback from Eduardo Vitral (roe.ac.uk).  
- ``mge.fit_1d``: Fixed an issue causing the program to stop when
  ``linear=True`` and ``quiet=False``.  
- ``mge.sky_level``: New function to compute the sky level from a 2D image.
- ``mge_fit_examples``: Updated the example to demonstrate the new
  ``mge.sky_level`` function.
- Updated dosctrings of several procedures to Numpy style.

V6.0.4: MC, Oxford, 3 September 2024
++++++++++++++++++++++++++++++++++++

- 25th anniversary edition :-)
- Replaced the ``mpfit`` non-linear least-squares optimization procedure with
  the more robust ``capfit.capfit`` from Cappellari (2023).
- Eliminated dependency on ``scipy.optimize.nnls`` after the original F77 code
  by Lawson & Hanson was replaced in SciPy v1.12 by an unreliable new function
  which broke my code. Now use my faster and robust ``capfit.lsq_box`` instead.
- ``mge_fit_1d``: New keyword ``linear`` to skip the nonlinear fit and optimize
  only the weights at fixed MGE sigma.
- ``find_galaxy``: replaced ``signal.medfilt`` with ``ndimage.median_filter``
  to avoid a bug introduced in SciPy v1.14.
- ``mge_print_contours``: New keyword ``magstep`` to control the step of the 
  contour levels in magnitudes.

V5.0.15: MC, Oxford, 31 March 2023
++++++++++++++++++++++++++++++++++

- ``mge_print_contours``, ``mge_print_contours_twist``: New keyword `minlevel`.
- ``mge_print_contours``, ``mge_print_contours_twist``: Analytic integral of
  the central pixel.
- ``mge_fit_examples``: Updated to demonstrate ``minlevel`` keyword.
- Included documentation of more functions on PyPi.

V5.0.14: MC, Oxford, 24 June 2021
+++++++++++++++++++++++++++++++++

- Formatted documentation as reStructuredText.

V5.0.13: MC, Oxford, 1 October 2020
+++++++++++++++++++++++++++++++++++

- With ``negative=True`` use NumPy ``linalg.lstsq`` instead of SciPy
  for a better default in the criterion for rank deficiency.
  Fixed ignoring negative weights in output with ``negative=True``.  

V5.0.12: MC, Oxford, 1 October 2018
+++++++++++++++++++++++++++++++++++

- Fixed clock ``DeprecationWarning`` in Python 3.7.
  Use SciPy 1.1 ``maxiter`` keyword in ``nnls``. 

V5.0.11: MC, Oxford, 12 May 2018
++++++++++++++++++++++++++++++++

- Dropped legacy Python 2.7 support. 

V5.0.10: MC, Oxford, 17 April 2018
++++++++++++++++++++++++++++++++++

- Changed imports for ``mgefit`` package. 

V5.0.9: MC, Oxford, 21 November 2017
++++++++++++++++++++++++++++++++++++

- changed ``sigmapsf`` and `normpsf` keywords to lowercase.  

V5.0.8: MC, Oxford, 25 May 2017
+++++++++++++++++++++++++++++++

- ``_fitfunc()`` does not return unused status anymore, for consistency 
  with the corresponding change to ``cap_mpfit``. 

V5.0.7: MC, Oxford, 14 February 2017
++++++++++++++++++++++++++++++++++++

- Make ``plot()`` callable after the program terminates.
  Included ``fignum`` keyword and removed the obsolete ``debug`` keyword.
  Use line colors from the current color cycle. 

V5.0.6: MC, Oxford, 24 January 2017
+++++++++++++++++++++++++++++++++++

- Improved labelling for Matplotlib 2.0. 

V5.0.5: MC, Oxford, 18 June 2015
++++++++++++++++++++++++++++++++

- Fixed plotting issue when combining profiles from multiple images.
  Thanks to Arianna Picotti (MPIA) for the bug report with examples.
  Only plot profiles for the best-fitting MGE. 

V5.0.4: MC, Atlantic Ocean, 6 June 2015
+++++++++++++++++++++++++++++++++++++++

- Fully broadcast ``_fitfunc``. 

V5.0.3: MC, Atlantic Ocean, 28 March 2015
+++++++++++++++++++++++++++++++++++++++++

- Make sure qbounds is a NumPy array. Include ``absdev`` in the class
  attributes. Nicely formatted printed solution. 

V5.0.2: MC, Oxford, 24 September 2014
+++++++++++++++++++++++++++++++++++++

- Improved plotting. 

V5.0.1: MC, Oxford, 25 May 2014
+++++++++++++++++++++++++++++++

- Support both Python 2.7 and Python 3. 

V5.0.0: MC, Aspen Airport, 8 February 2014
++++++++++++++++++++++++++++++++++++++++++

- Translated from IDL into Python. 

V4.1.3: MC, Oxford, 23 January 2013
+++++++++++++++++++++++++++++++++++

- Explained optional usage of SOL in input.
  Removed stop when MPFIT reports over/underflow.  

V4.1.2: MC, Oxford, 24 April 2012
+++++++++++++++++++++++++++++++++

- Small change to the treatment of the innermost unresolved Gaussians. 

V4.1.1: MC, Oxford, 12 November 2010
++++++++++++++++++++++++++++++++++++

- Added keyword /QUIET. 

V4.1.0: MC, Oxford, 22 April 2010
+++++++++++++++++++++++++++++++++

- Allow QBOUNDS to have four elements, to perform bulge/disk
  decompositions similarly to the /BULGE_DISK option.  

V4.0.1: MC, Oxford, 6 June 2009
+++++++++++++++++++++++++++++++

- Added output keyword ABSDEV. Fixed display not being updated
  while iterating under Windows. 

V4.0.0: MC, Windhoek, 5 October 2008
++++++++++++++++++++++++++++++++++++

- Added /BULGE_DISK keyword to perform non-parametric bulge/disk
  decompositions using MGE. Updated MPFIT to version v1.52 2008/05/04,
  to fix a bug with the required parinfo.tied mechanism. In the new
  version of MPFIT, which I again renamed MGE_MPFIT, I implemented
  my previous important modification to improve convergence with
  MGE_FIT_SECTORS. 

V3.9.5: MC, Oxford, 24 September 2008
+++++++++++++++++++++++++++++++++++++

- Force Gaussians smaller than the PSF, which have a degenerate
  axial ratio, to have the same axial ratio as the mean of the first
  two well-determined Gaussians. 

V3.9.4: MC, Oxford, 16 May 2008
+++++++++++++++++++++++++++++++

- Use more robust la_least_squares (IDL 5.6) instead of SVDC with
  /NEGATIVE keyword. 

V3.9.3: MC, Leiden, 18 October 2005
+++++++++++++++++++++++++++++++++++

- Changed axes labels in plots. 

V3.9.2: MC, Leiden, 11 October 2005
+++++++++++++++++++++++++++++++++++

- Print iterations of the longer part at the end, not of the
  short "Gaussian cleaning" part. 

V3.9.1: MC, Leiden, 1 May 2005
++++++++++++++++++++++++++++++

- Replaced LOGRANGE keyword in the example with the new MAGRANGE.

V3.9.0: MC, Leiden, 23 October 2004
+++++++++++++++++++++++++++++++++++

- Allow forcing the outer slope of the surface brightness profile of
  the MGE model to decrease at least as ``R**-n`` at the largest measured
  radius (cfr. version 3.8).
- Clean the solution at the end of the nonlinear fit as already done in
  the /LINEAR implementation. It's almost always redundant, but quick.  

V3.8.1: MC, Vicenza, 23 August 2004
+++++++++++++++++++++++++++++++++++

- Make sure this routine uses the Nov/2000 version of Craig Markwardt
  MPFIT which was renamed MGE_MPFIT to prevent potential conflicts with
  more recent versions of the same routine. 

V3.8.0: MC, Leiden, 8 May 2004
++++++++++++++++++++++++++++++

- Force the surface brightness of the MGE model to decrease at
  least as ``R**-2`` at the largest measured radius. 

V3.7.6: MC, Leiden, 20 March 2004
+++++++++++++++++++++++++++++++++

- Use an updated calling sequence for BVLS. 

V3.7.5: MC, Leiden 23 July 2003
+++++++++++++++++++++++++++++++

- Corrected a small bug introduced in V3.73. Thanks to Arend Sluis. 

V3.7.4: MC, Leiden, 9 May 2003
++++++++++++++++++++++++++++++

- Use N_ELEMENTS instead of KEYWORD_SET to test
  non-logical keywords. 

V3.7.3: MC, Leiden, 7 March 2003
++++++++++++++++++++++++++++++++

- Force the input parameters to the given bounds if they
  fall outside the required range before starting the fit.
  After feedback from Remco van den Bosch.

V3.7.2: MC, Leiden, 13 October 2002
+++++++++++++++++++++++++++++++++++

- Added ERRMSG keyword to MPFIT call.

V3.7.1: MC, Leiden 20 May 2002
++++++++++++++++++++++++++++++

- Added compilation options.

V3.7.0: MC, Leiden, 23 February 2002
++++++++++++++++++++++++++++++++++++

- Added explicit stepsize (STEP) of numerical derivative in
  parinfo structure, after a suggestion by Craig B. Markwardt.

V3.6.0: MC, Leiden, 23 October 2001
+++++++++++++++++++++++++++++++++++

- Modified implementation of /NEGATIVE keyword.
          
V3.5.0: MC, Leiden, 8 October 2001
++++++++++++++++++++++++++++++++++

- Updated documentation.

V3.4.0: MC, Leiden, 20 September 2001
+++++++++++++++++++++++++++++++++++++

- Added /FASTNORM keyword

V3.3.0: MC, Leiden, 26 July 2001
++++++++++++++++++++++++++++++++

- Added MGE PSF convolution, central pixel integration and changed
  program input parameters to make it independent of SECTORS_PHOTOMETRY

V3.2.0: MC, Leiden, 8 July 2001
+++++++++++++++++++++++++++++++

- Graphical changes: always show about 7 sectors on the screen, 
  and print plots with shared axes. 

V3.1.0: MC, Leiden, 27 April 2001
+++++++++++++++++++++++++++++++++

- More robust definition of err in FITFUNC_MGE_SECTORS.

V3.0.0: MC, Padova, July 2000
+++++++++++++++++++++++++++++

- Significant changes.

V2.0.0: MC, Leiden, January 2000
++++++++++++++++++++++++++++++++

- Major revisions.

V1.0.0: Padova, February 1999
+++++++++++++++++++++++++++++

- First implementation by Michele Cappellari.
