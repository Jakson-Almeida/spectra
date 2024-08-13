import numpy as np
import process_spectra as ps
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter
import logging
logger = logging.getLogger(__name__)


def find_wlres(wl, T, lims=[1.5e-6, 1.6e-6], prominence=0.5):
    """
    Resonant wavelength estimation

        Find the spectrum dip and fit it to a loretzian

    Parameters
    ----------
    wl: np.array
        Wavelength

    T: np.array
        Spectrum

    lims: list
        Resonant wavelength bounds

    prominence: float
        Resonant dip prominence

    Returns
    -------
    wlres: float
        Resonant wavelength
    """
    info = {}

    opts = {'wl_range': [min(lims)-10e-9, max(lims)+10e-9],
           'prominence': prominence,
           'valley_width': None}
    x = np.append(wl.reshape(-1, 1), T.reshape(-1, 1), axis=1)
    x, info = ps.funcs.mask_spectrum(x, info, opts['wl_range'],
                                            quiet=True)
    x, _info = ps.funcs.filter_spectrum(x, info, 5, 3,
                                               quiet=True)
    info = {**info, **_info}
    x, _info = ps.funcs.get_approximate_valley(x, info,
                                    prominence=opts['prominence'])
    info = {**info, **_info}
    try:
        wlres = 1e9*info['resonant_wl']
    except KeyError:
        best = info['best_index']
        wlres = 1e9*info[f'resonant_wl_{best}']
    return wlres


def transmission_spectra(x, a, x0, w, bias):
    """
    Approximates a LPFG spectrum by a loretzian

    Parameters
    ----------
    x: np.array
        Wavelength for simulation

    a: float
        Attenuation intensity

    x0: float
        Resonant wavelength

    w: float
        FWHM

    bias: float
        Insertion loss

    Returns
    -------
    spectrum: np.array
        LPFG array

    """
    return -a*(1 + ((x - x0)/(w/(2*abs(a/3 - 1)**0.5)))**2)**(-1) - bias


def lin_interp(x, y, i, half):
    """
    Linear interpolation
    """
    return x[i] + (x[i+1] - x[i]) * ((half - y[i]) / (y[i+1] - y[i]))


def fwhm(x, y):
    """
    Estimate FWHM

    Parameters
    ----------
    x: np.array
        x-var

    y: np.array
        y-var

    Returns
    -------
    fwhm: float
    """
    half = max(y) - 3.010299956639812
    signs = np.sign(np.add(y, -half))
    zero_crossings = (signs[0:-2] != signs[1:-1])
    zero_crossings_i = np.where(zero_crossings)[0]
    crossings = [lin_interp(x, y, zero_crossings_i[0], half),
                 lin_interp(x, y, zero_crossings_i[1], half)]
    return max(crossings) - min(crossings)


def lorentz(x, a, x0, w, b):
    """
    Loretzian function
    """
    return a*(1 + ((x - x0)/(w/2))**2)**(-1) + b


def gaussian(x, a, x0, s):
    """
    Gaussian function
    """
    arg = -(x - x0)**2 / (2*s**2)
    return a * np.exp(arg)