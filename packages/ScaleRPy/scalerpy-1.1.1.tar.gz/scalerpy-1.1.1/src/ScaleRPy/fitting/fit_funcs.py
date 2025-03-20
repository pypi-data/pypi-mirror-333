"""
Contains ridge-finding and fitting functions for SpatGalDat objects

Copyright 2025 Bryanne McDonough
Apache License, Version 2.0

"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from scipy.optimize import curve_fit
import numpy.ma as ma
import math
from scipy.stats import gaussian_kde
from ScaleRPy.formatting.tol_colors import tol_cmap


def find_ridge(x, y, xrange=None, yrange=None, numxbins=40, numybins=40, fittype='kde', makeplot=False, xlabel='', ylabel='', fontsize=12, kde_bwmode='scott', kde_error='bw_approx', cmap=tol_cmap('iridescent'), ridgeptcol='m'):
    """
    This function creates a ridge line fit by constructing a 2D histogram of the x and y data, 
    identifying the "ridge" of the data (the value of y where the most spaxels are in a given column of x), 
    and performing a fit to those ridge points.

    x: a 1D array of length N containing the x values for the spatially resolved relationship (e.g., stellar mass surface density for N spaxels)
    y: a 1D array of length N the y values for the spatially resolved relationship (e.g., SFR surface density for N spaxels)
    xrange: the range in x that the scaling relation fit should be performed over; should exclude outlying data
    yrange: the range in y that the scaling relation fit should be performed over; should exclude outlying data
    numxbins: the number of bins the x data will be divided into. Smaller bins are recommended for smaller data samples
    numybins: the number of bins the y data will be divided into
    fittype: the type of ridgeline fit to perform, the options are currently 'max' or 'kde' 
        max    : from a 2D histogram, the fit will be done to the max value of a given column

        kde (default):    Modes and errors obtained from a kernel density estimate of spaxel SFRs within bins of mass
    xlabel (str) : the label for the x-axis of the plot
    ylabel (str) : the label for the y-axis of the plot
    fontsize (int) : the fontsize for the labels
    kde_bwmode (str) : the bandwidth method for the KDE, see scipy.stats.gaussian_kde for options
    kde_error (str) : the method for estimating the error on the mode from the KDE, options are 'bw_approx' and 'half_max'
    cmap (matplotlib colormap) : the colormap to use for the 2D histogram
    ridgeptcol (str) : the color of the ridge points on the plot

    Assumes spaxel sample has already been reasonably cleaned to remove spaxels with e.g., low mass surface density (<10^6 M_sun/kpc^2)
    """

    if xrange is None: xrange = (min(x), max(x))
    if yrange is None: yrange = (min(y), max(y))

    if makeplot:
        histfig, ax = plt.subplots()

    xbin = np.linspace(xrange[0], xrange[1], num=numxbins)
    ybin = np.linspace(yrange[0], yrange[1], num=numybins)

    norm = colors.LogNorm()
    # construct 2D histogram from data
    hist, xedges, yedges = np.histogram2d(x, y, bins=(xbin, ybin))

    if makeplot:
        hist, xedges, yedges, image = ax.hist2d(x, y, bins=(xbin, ybin), norm=norm, cmin=1, cmap=cmap, zorder=1)  # cmin=1 to exclude any bins with no data
        cbar = histfig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
        cbar.set_label(r'$\mathrm{N_{samples}}$', rotation=90, fontsize=fontsize)

    # mask any points without data
    mask = np.isinf(hist)
    goodhist = ma.masked_array(hist, mask=mask)

    # arrays to store the x and y values that will be fit to    
    fx = np.empty(len(hist[:, 0]))  # the middle value of each x bin
    fy = np.empty(len(hist[:, 0]))  # the middle value of the y bin that contains the most amount of spaxels in a given x bin
    fyerr = np.empty(len(hist[:, 0]))  # stores the error in fy if fittype='Gauss'

    # find the (x,y) points where histogram is peaked (ridge points)
    for i in range(0, len(xedges) - 1):
        col = goodhist[i, :]
        fx[i] = (xedges[i] + xedges[i + 1]) / 2.
        if fittype == 'max':
            hmax = np.nanargmax(col)
            fy[i] = (yedges[hmax] + yedges[hmax + 1]) / 2.
            fyerr = None
        elif fittype == 'kde':
            whx = np.nonzero((x > xedges[i]) & (x <= xedges[i + 1]) & (np.isfinite(y)))
            # require at least 5 points to fit KDE
            if len(whx[0]) < 5:
                fy[i] = np.nan
                fyerr[i] = np.nan
                continue
            fy[i], fyerr[i] = kde_mode(y[whx], bandwidth=kde_bwmode, error_mode=kde_error)
        else:
            print(fittype + ' is not a recognized input for fittype, please check inputs and try again')
            return

    ridge = np.asarray([fx, fy, fyerr])

    if makeplot:
        ax.set_xlabel(xlabel, fontsize=fontsize)
        ax.set_ylabel(ylabel, fontsize=fontsize)
        ax.errorbar(fx, fy, yerr=fyerr, fmt='.', color=ridgeptcol, zorder=4)
        return (histfig, ax), ridge, hist, xedges, yedges
    else:
        return ridge

def fit_double(ridge, curve_fit_method = 'trf'):
    """ 
    Fit a double linear to the ridge points

    Parameters
    ridge: a 3xN array containing the x and y values of the ridge points and the error in y
    """
    fx = ridge[0,:]
    fy = ridge[1,:]
    fyerr = ridge[2,:]
    #set bounds such that x0 is within xrange
    bounds = ((-1*np.inf, -1*np.inf, -1*np.inf, min(fx)), (np.inf, np.inf, np.inf, max(fx)))
    popt, pcov = curve_fit(doubline, fx, fy, sigma=fyerr, nan_policy='omit', bounds=bounds, method = curve_fit_method)
    # obtain errors from the covariant matrix
    perr = np.sqrt(np.diag(pcov))
    return(popt,perr)

def fit_single(ridge, curve_fit_method = 'trf'):
    #set bounds such that x0 is within xrange
    fx = ridge[0,:]
    fy = ridge[1,:]
    fyerr = ridge[2,:]
    bounds = ((-1*np.inf, -1*np.inf), (np.inf, np.inf))
    popt, pcov = curve_fit(line, fx, fy, sigma=fyerr, nan_policy='omit', bounds=bounds, method = curve_fit_method)
    # obtain errors from the covariant matrix
    perr = np.sqrt(np.diag(pcov))
    return(popt,perr)

def kde_mode(data, bandwidth = 'scott', error_mode ='bw_approx'):
    """
    Estimate the error on the mode using KDE.
    Written by Copilot

    Parameters:
    data (array-like): Input data.
    bandwidth (str or float): Bandwidth for KDE. Maps to bw_method in gaussian_kde.
    error_mode(str): Method for estimating the error on the mode. Options are 'bw_approx' and 'half_max'.
                    'bw_approx' uses the bandwidth as an approximation of the error
                    'half_max' uses the width of the peak at half maximum as the error. (Not recommended)
                    'bootstrap' uses bootstrapping to estimate the error on the mode using 1000 bootstrap resamplings. (Will take significantly longer)

    Returns:
    float: Estimated error on the mode.
    """
    kde = gaussian_kde(data, bw_method=bandwidth)
    x = np.linspace(min(data), max(data), 1000)
    kde_values = kde(x)
    mode = x[np.argmax(kde_values)]
    
    # Estimate the width of the peak at half maximum
    half_max = np.max(kde_values) / 2
    peak_indices = np.where(kde_values >= half_max)[0]
    peak_width = x[peak_indices[-1]] - x[peak_indices[0]]
    
    bw_approxerror = kde.factor * np.std(data)
    if error_mode == 'bw_approx':
        return(mode, bw_approxerror)
    elif error_mode == 'half_max':
        return(mode, peak_width / 2)
    elif error_mode == 'bootstrap':
        return(mode, bootstrap_mode_error(data))
    
def bootstrap_mode_error(data, num_samples=1000):
    """
    Estimate the error on the mode using bootstrapping.
    Will take a long time for large datasets!

    Parameters:
    data (array-like): Input data.
    num_samples (int): Number of bootstrap samples.

    Returns:
    float: Standard error of the mode.
    """
    modes = []
    for _ in range(num_samples):
        sample = np.random.choice(data, size=len(data), replace=True)
        kde = gaussian_kde(sample)
        x = np.linspace(min(sample), max(sample), 1000)
        kde_values = kde(x)
        mode = x[np.argmax(kde_values)]
        modes.append(mode)
    return np.std(modes)

#add a double gauss??
"""
def gauss(x, mean, std): #retain for fitting columns with Gaussian to obtain max with errors
    return(0.3989/std * math.e**(-.5*((x-mean)/std)**2)) #constant is 1/sqrt(2pi)
"""
def line(x,m,b):
    return(m*x+b)

def doubline(x,m1,b1,m2,x0):
    b2 = m1*x0 + b1 - m2*x0
    y = np.zeros_like(x)
    y[x<x0] = m1*x[x<x0]+b1
    y[x>=x0] = m2*x[x>=x0]+b2
    return(y)

"""
def double_gaussian(x, params):
    (amp1, m1, sigma1, amp2, m2, sigma2) = params
    y =   amp1 * np.exp( - (x - m1)**2.0 / (2.0 * sigma1**2.0) ) \
          + amp2 * np.exp( - (x - m2)**2.0 / (2.0 * sigma2**2.0) )
    return y
"""

