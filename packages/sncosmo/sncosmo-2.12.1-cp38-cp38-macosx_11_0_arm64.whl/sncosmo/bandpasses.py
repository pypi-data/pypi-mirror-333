# Licensed under a 3-clause BSD style license - see LICENSE.rst

import copy

import astropy.units as u
import numpy as np
from astropy.io import ascii
from astropy.utils import lazyproperty
from scipy.interpolate import splev, splrep, interp1d, RegularGridInterpolator
from numpy.polynomial.polynomial import polyval2d

from ._registry import Registry
from .constants import HC_ERG_AA, SPECTRUM_BANDFLUX_SPACING
from .utils import integration_grid

__all__ = ['get_bandpass', 'read_bandpass', 'Bandpass', 'AggregateBandpass',
           'BandpassInterpolator', 'GeneralBandpassInterpolator', 'Transforms']

_BANDPASSES = Registry()
_BANDPASS_INTERPOLATORS = Registry()


def get_bandpass(name, *args, **kwargs):
    """Get a Bandpass from the registry by name.

    This function can return several types of Bandpass objects depending on
    the bandpass's variability on the focal plane:

    - **Static Bandpass:** If the bandpass does not vary spatially on the
      focal plane, `get_bandpass` returns a `Bandpass` instance directly.

    - **Radially Variable Bandpass:** For bandpasses with radial variability
      (e.g., `megacampsf`), an `AggregateBandpass` instance is returned, which
      adjusts the bandpass shape based on the specified radius.

    - **Position-Dependent Bandpass:** For bandpasses that vary with position
      on the sensor plane (e.g., `ztf`, `megacam6`, `hsc`), the returned
      object depends on the specified coordinates and sensor ID. If a single
      location is requested, an interpolated `Bandpass` instance is returned;
      if multiple positions are specified, an array of bandpass objects is
      generated to represent the spatial variations.

    Refer to the Examples section for more detailed usage scenarios.

    Parameters
    ----------
    name : str or `Bandpass`
        The name of the Bandpass to retrieve from the registry, or an existing
        Bandpass object. If a Bandpass object is passed, it is returned
        directly.

    *args : tuple, optional
        Additional positional arguments, used primarily for radially variable
        bandpasses (e.g., radius for radial interpolations).

    **kwargs : dict, optional
        Named arguments to customize the Bandpass retrieval:
            - 'radius' : float, optional
                Radius for radial bandpasses (default: 0).
            - 'wave' : array-like, optional
                Wavelength grid for an interpolated Bandpass.
            - 'x', 'y' : float, optional
                Spatial coordinates for 2D interpolation.
            - 'sensor_id' : int, optional
                Sensor ID for multi-sensor configurations (default: 1).
            - 'filter_frame' : bool, optional
                If True, applies a filter frame (default: False).

    Returns
    -------
    Bandpass or ndarray
        - If the name corresponds to a static Bandpass: returns the Bandpass
          object.
        - If the Bandpass is radially variable: returns the interpolated
          Bandpass object at the specified radius.
        - For general interpolated Bandpasses (2D or multi-sensor): returns an
          array of transmission values, or a Bandpass object if only one
          spatial filter is evaluated.

    Raises
    ------
    TypeError
        If the parameters provided in `*args` and `**kwargs` are invalid

    Notes
    -----
    - Uses _BANDPASSES and _BANDPASS_INTERPOLATORS to retrieve static
      and interpolated Bandpasses, respectively.
    - The general case applies to configurations like ZTF, MegaCam, and HSC,
      where multidimensional interpolation grids are used.

    Examples
    --------
    Basic usage with a static Bandpass:
    >>> bandpass = get_bandpass('ztfg')

    Using a radial Bandpass with a specific radius:
    >>> radial_bandpass = get_bandpass('megacampsf::r', radius=1.2)

    Specifying spatial coordinates and a sensor ID for the Bandpasses managed
    by a `GeneralBandpassInterpolator`
    >>> interpolated_bandpass = get_bandpass(
    ...     'megacam6::g', x=2355.22, y=1222.4, sensor_id=12)

    Specifying a vector of spatial coordinates and sensor ids
    >>> x = numpy.random.uniform(0., 2048., size=100)
    >>> y = numpy.random.uniform(0., 4600., size=100)
    >>> sensor_id = numpy.random.randint(0, 36, size=100)
    >>> interpolated_bandpasses = get_bandpass(
    ...     'megacam6::z', x=x, y=y, sensor_id=sensor_id)

    Using a custom wavelength grid
    >>> x = numpy.random.uniform(0., 3000., size=100)
    >>> y = numpy.random.uniform(0., 3000., size=100)
    >>> sensor_id = numpy.random.randint(0, 65, size=100)
    >>> wave_grid = numpy.random.linspace(3000., 11000., 8000)
    >>> custom_wave_bandpass = get_bandpass('ztf::r', wave=wave_grid)

    """
    if isinstance(name, Bandpass):
        return name

    # static bandpass
    if len(kwargs) + len(args) == 0:
        return _BANDPASSES.retrieve(name)

    # radially variable bandpass (snfit-like version)
    interp = _BANDPASS_INTERPOLATORS.retrieve(name)
    if isinstance(interp, BandpassInterpolator):
        # arguments check: the `pos` argument to BandpassInterpolator.at can be
        # passed as a positional argument or by the 'radius' keyword argument
        if args and kwargs:
            raise TypeError(
                'keyword and positional arguments cannot be mixed')
        if not args and list(kwargs.keys()) != ['radius']:
            raise TypeError(
                'unexpected keyword arguments {}'.format(
                    ', '.join(set(kwargs.keys()) - {'radius'})))

        return interp.at(*args or (kwargs.get('radius', 0),))

    # general case (e.g. ZTF, MegaCam, HSC), at this point `interp` is an
    # instance of GeneralBandpassInterpolator
    unexpected_kwargs = set(
        kwargs.keys() - {'x', 'y', 'sensor_id', 'wave'})
    if unexpected_kwargs:
        raise TypeError(
            'unexpected keyword arguments {}'.format(
                ', '.join(unexpected_kwargs)))

    wavegrid = kwargs.get('wave', interp.wavegrid)
    trans = interp.eval_at(
        kwargs.get('x', 0.),
        kwargs.get('y', 0.),
        kwargs.get('sensor_id', 1),
        wavegrid,
        filter_frame=kwargs.get('filter_frame', False))
    if trans.shape[0] == 1:
        return Bandpass(wavegrid, trans.squeeze(), name=name)
    return trans


def read_bandpass(fname, fmt='ascii', wave_unit=u.AA,
                  trans_unit=u.dimensionless_unscaled,
                  normalize=False, trim_level=None, name=None):
    """Read bandpass from two-column ASCII file containing wavelength and
    transmission in each line.

    Parameters
    ----------
    fname : str
        File name.
    fmt : {'ascii'}
        File format of file. Currently only ASCII file supported.
    wave_unit : `~astropy.units.Unit` or str, optional
        Wavelength unit. Default is Angstroms.
    trans_unit : `~astropy.units.Unit`, optional
        Transmission unit. Can be `~astropy.units.dimensionless_unscaled`,
        indicating a ratio of transmitted to incident photons, or units
        proportional to inverse energy, indicating a ratio of transmitted
        photons to incident energy. Default is ratio of transmitted to
        incident photons.
    normalize : bool, optional
        If True, normalize fractional transmission to be 1.0 at peak.
        It is recommended to set to True if transmission is in units
        of inverse energy. (When transmission is given in these units, the
        absolute value is usually not significant; normalizing gives more
        reasonable transmission values.) Default is False.
    name : str, optional
        Identifier. Default is `None`.

    Returns
    -------
    band : `~sncosmo.Bandpass`
    """

    if fmt != 'ascii':
        raise ValueError("format {0} not supported. Supported formats: 'ascii'"
                         .format(fmt))
    t = ascii.read(fname, names=['wave', 'trans'])
    return Bandpass(t['wave'], t['trans'], wave_unit=wave_unit,
                    trans_unit=trans_unit, normalize=normalize,
                    trim_level=trim_level, name=name)


def slice_exclude_below(a, minvalue, grow=1):
    """Contiguous range in 1-d array `a` that excludes values less than
    `minvalue`. Range is expanded by `grow` in each direction."""

    idx = np.flatnonzero(a >= minvalue)
    i0 = max(idx[0] - grow, 0)
    i1 = min(idx[-1] + 1 + grow, len(a))  # exclusive

    return slice(i0, i1)


class Bandpass(object):
    """Transmission as a function of spectral wavelength.

    Parameters
    ----------
    wave : list_like
        Wavelength. Monotonically increasing values.
    trans : list_like
        Transmission fraction.
    wave_unit : `~astropy.units.Unit` or str, optional
        Wavelength unit. Default is Angstroms.
    trans_unit : `~astropy.units.Unit`, optional
        Transmission unit. Can be `~astropy.units.dimensionless_unscaled`,
        indicating a ratio of transmitted to incident photons, or units
        proportional to inverse energy, indicating a ratio of transmitted
        photons to incident energy. Default is ratio of transmitted to
        incident photons.
    normalize : bool, optional
        If True, normalize fractional transmission to be 1.0 at peak.
        It is recommended to set normalize=True if transmission is in units
        of inverse energy. (When transmission is given in these units, the
        absolute value is usually not significant; normalizing gives more
        reasonable transmission values.) Default is False.
    trim_level : float, optional
        If given, crop bandpass to region where transmission is above this
        fraction of the maximum transmission. For example, if maximum
        transmission is 0.5, ``trim_level=0.001`` will remove regions where
        transmission is below 0.0005. Only contiguous regions on the sides
        of the bandpass are removed.
    name : str, optional
        Identifier. Default is `None`.

    Examples
    --------
    Construct a Bandpass and access the input arrays:

    >>> b = Bandpass([4000., 4200., 4400.], [0.5, 1.0, 0.5])
    >>> b.wave
    array([ 4000.,  4200.,  4400.])
    >>> b.trans
    array([ 0.5,  1. ,  0.5])

    Bandpasses act like continuous 1-d functions (linear interpolation is
    used):

    >>> b([4100., 4300.])
    array([ 0.75,  0.75])

    The effective (transmission-weighted) wavelength is a property:

    >>> b.wave_eff
    4200.0

    The ``trim_level`` keyword can be used to remove "out-of-band"
    transmission upon construction. The following example removes regions of
    the bandpass with tranmission less than 1 percent of peak:

    >>> band = Bandpass([4000., 4100., 4200., 4300., 4400., 4500.],
    ...                 [0.001, 0.002,   0.5,   0.6, 0.003, 0.001],
    ...                 trim_level=0.01)

    >>> band.wave
    array([ 4100.,  4200.,  4300.,  4400.])

    >>> band.trans
    array([ 0.002,  0.5  ,  0.6  ,  0.003])

    While less strictly correct than including the "out-of-band" transmission,
    only considering the region of the bandpass where transmission is
    significant can improve model-bandpass overlap as well as performance.
    """

    def __init__(self, wave, trans, wave_unit=u.AA,
                 trans_unit=u.dimensionless_unscaled, normalize=False,
                 name=None, trim_level=None):
        wave = np.asarray(wave, dtype=np.float64)
        trans = np.asarray(trans, dtype=np.float64)
        if wave.shape != trans.shape:
            raise ValueError('shape of wave and trans must match')
        if wave.ndim != 1:
            raise ValueError('only 1-d arrays supported')

        # Ensure that units are actually units and not quantities, so that
        # `to` method returns a float and not a Quantity.
        wave_unit = u.Unit(wave_unit)
        trans_unit = u.Unit(trans_unit)

        if wave_unit != u.AA:
            wave = wave_unit.to(u.AA, wave, u.spectral())

        # If transmission is in units of inverse energy, convert to
        # unitless transmission:
        #
        # (transmitted photons / incident photons) =
        #      (photon energy) * (transmitted photons / incident energy)
        #
        # where photon energy = h * c / lambda
        if trans_unit != u.dimensionless_unscaled:
            trans = (HC_ERG_AA / wave) * trans_unit.to(u.erg**-1, trans)

        # Check that values are monotonically increasing.
        # We could sort them, but if this happens, it is more likely a user
        # error or faulty bandpass definition. So we leave it to the user to
        # sort them.
        if not np.all(np.ediff1d(wave) > 0.):
            raise ValueError('bandpass wavelength values must be monotonically'
                             ' increasing when supplied in wavelength or '
                             'decreasing when supplied in energy/frequency.')

        if normalize:
            trans /= np.max(trans)

        # Trim "out-of-band" transmission
        if trim_level is not None:
            s = slice_exclude_below(trans, np.max(trans) * trim_level, grow=1)
            wave = wave[s]
            trans = trans[s]

        # if more than one leading or trailing transmissions are zero, we
        # can remove them.
        if ((trans[0] == 0.0 and trans[1] == 0.0) or (trans[-1] == 0.0 and
                                                      trans[-2] == 0.0)):
            i = 0
            while i < len(trans) and trans[i] == 0.0:
                i += 1
            if i == len(trans):
                raise ValueError('all zero transmission')
            j = len(trans) - 1
            while j >= 0 and trans[j] == 0.0:
                j -= 1

            # back out to include a single zero
            if i > 0:
                i -= 1
            if j < len(trans) - 1:
                j += 1

            wave = wave[i:j+1]
            trans = trans[i:j+1]

        self.wave = wave
        self.trans = trans

        # Set up interpolation.
        # This appears to be the fastest-evaluating interpolant in
        # scipy.interpolate.
        self._tck = splrep(self.wave, self.trans, k=1)

        self.name = name

    def minwave(self):
        return self.wave[0]

    def maxwave(self):
        return self.wave[-1]

    @lazyproperty
    def wave_eff(self):
        """Effective wavelength of bandpass in Angstroms."""
        wave, _ = integration_grid(self.minwave(), self.maxwave(),
                                   SPECTRUM_BANDFLUX_SPACING)
        weights = self(wave)
        return np.sum(wave * weights) / np.sum(weights)

    def __call__(self, wave):
        return splev(wave, self._tck, ext=1)

    def __repr__(self):
        name = ''
        if self.name is not None:
            name = ' {!r}'.format(self.name)
        return "<{:s}{:s} at 0x{:x}>".format(self.__class__.__name__, name,
                                             id(self))

    def shifted(self, factor, name=None):
        """Return a new Bandpass instance with all wavelengths
        multiplied by a factor."""
        return Bandpass(factor * self.wave, self.trans, name=name)


class _SampledFunction(object):
    """Represents a 1-d continuous function, used in AggregateBandpass."""

    def __init__(self, x, y):
        self.x = np.asarray(x, dtype=np.float64)
        self.y = np.asarray(y, dtype=np.float64)
        self.xmin = x[0]
        self.xmax = x[-1]
        self._tck = splrep(self.x, self.y, k=1)

    def __call__(self, x):
        return splev(x, self._tck, ext=1)


class AggregateBandpass(Bandpass):
    """Bandpass defined by multiple transmissions in series.

    Parameters
    ----------
    transmissions : list of (wave, trans) pairs.
        Functions defining component transmissions.
    prefactor : float, optional
        Scalar factor to multiply transmissions by. Default is 1.0.
    name : str, optional
        Name of bandpass.
    family : str, optional
        Name of "family" this bandpass belongs to. Such an identifier can
        be useful for identifying bandpasses belonging to the same
        instrument/filter combination but different focal plane
        positions.
    """

    def __init__(self, transmissions, prefactor=1.0, name=None, family=None):
        if len(transmissions) < 1:
            raise ValueError("empty list of transmissions")

        # Set up transmissions as `_SampledFunction`s.
        #
        # We allow passing `_SampledFunction`s directly to allow
        # RadialBandpassGenerator to generate AggregateBandpasses a
        # bit more efficiently, even though _SampledFunction isn't
        # part of the public API.
        self.transmissions = [t if isinstance(t, _SampledFunction)
                              else _SampledFunction(t[0], t[1])
                              for t in transmissions]
        self.prefactor = prefactor
        self.name = name
        self.family = family

        # Determine min/max wave: since sampled functions are zero outside
        # their domain, minwave is the *largest* minimum x value, and
        # vice-versa for maxwave.
        self._minwave = max(t.xmin for t in self.transmissions)
        self._maxwave = min(t.xmax for t in self.transmissions)

    def minwave(self):
        return self._minwave

    def maxwave(self):
        return self._maxwave

    def __str__(self):
        return ("AggregateBandpass: {:d} components, prefactor={!r}, "
                "range=({!r}, {!r}), name={!r}"
                .format(len(self.transmissions), self.prefactor,
                        self.minwave(), self.maxwave(), self.name))

    def __call__(self, wave):
        t = self.transmissions[0](wave)
        for trans in self.transmissions[1:]:
            t *= trans(wave)
        t *= self.prefactor
        return t

    def shifted(self, factor, name=None, family=None):
        """Return a new AggregateBandpass instance with all wavelengths
        multiplied by a factor."""

        transmissions = [(factor * t.x, t.y) for t in self.transmissions]
        return AggregateBandpass(transmissions,
                                 prefactor=self.prefactor,
                                 name=name, family=family)


class BandpassInterpolator(object):
    """Bandpass generator defined as a function of focal plane position.

    Instances of this class are not Bandpasses themselves, but
    generate Bandpasses at a given focal plane position. This class
    stores the transmission as a function of focal plane position and
    interpolates between the defined positions to return the bandpass
    at an arbitrary position.

    Parameters
    ----------
    transmissions : list of (wave, trans) pairs
        Transmissions that apply everywhere in the focal plane.
    dependent_transmissions :  list of (value, wave, trans)
        Transmissions that depend on some parameter. Each `value` is the
        scalar parameter value, `wave` and `trans` are 1-d arrays.
    prefactor : float, optional
        Scalar multiplying factor.
    name : str

    Examples
    --------

    Transmission uniform across focal plane:

    >>> uniform_trans = ([4000., 5000.], [1., 0.5])  # wave, trans

    Transmissions as a function of radius:

    >>> trans0 = (0., [4000., 5000.], [0.5, 0.5])  # radius=0
    >>> trans1 = (1., [4000., 5000.], [0.75, 0.75]) # radius=1
    >>> trans2 = (2., [4000., 5000.], [0.1, 0.1]) # radius=2


    >>> band_interp = BandpassInterpolator([uniform_trans],
    ...                                    [trans0, trans1, trans2],
    ...                                    name='my_band')

    Min and max radius:

    >>> band_interp.minpos(), band_interp.maxpos()
    (0.0, 2.0)

    Get bandpass at a given radius:

    >>> band = band_interp.at(1.5)

    >>> band
    <AggregateBandpass 'my_band at 1.500000' at 0x7f7a2e425668>

    The band is aggregate of uniform transmission part,
    and interpolated radial-dependent part.

    >>> band([4500., 4600.])
    array([ 0.65625,  0.6125 ])

    """
    def __init__(self, transmissions, dependent_transmissions,
                 prefactor=1.0, name=None):

        # create sampled functions for normal transmissions
        self.transmissions = [_SampledFunction(t[0], t[1])
                              for t in transmissions]

        # ensure dependent transmissions are sorted
        sorted_trans = sorted(dependent_transmissions, key=lambda x: x[0])
        self.dependent_transmissions = [(t[0], _SampledFunction(t[1], t[2]))
                                        for t in sorted_trans]

        self.prefactor = prefactor

        self.name = name

    def minpos(self):
        """Minimum positional parameter value."""
        return self.dependent_transmissions[0][0]

    def maxpos(self):
        """Maximum positional parameter value."""
        return self.dependent_transmissions[-1][0]

    def at(self, pos):
        """Return the bandpass at the given position"""

        if pos < self.minpos() or pos >= self.maxpos():
            raise ValueError("Position outside bounds")

        # find index such that t[i-1] <= pos < t[i]
        i = 1
        while (i < len(self.dependent_transmissions) and
               pos > self.dependent_transmissions[i][0]):
            i += 1

        # linearly interpolate second transmission onto first
        v0, f0 = self.dependent_transmissions[i-1]
        v1, f1 = self.dependent_transmissions[i]
        w1 = (pos - v0) / (v1 - v0)
        w0 = 1.0 - w1
        x = f0.x
        y = w0 * f0.y + w1 * f1(x)
        f = _SampledFunction(x, y)

        transmissions = copy.copy(self.transmissions)  # shallow copy the list
        transmissions.append(f)

        name = "" if self.name is None else (self.name + " ")
        name += "at {:f}".format(pos)

        return AggregateBandpass(transmissions, prefactor=self.prefactor,
                                 name=name, family=self.name)


class Transforms(object):
    """Provides transformations from pixel coordinates to focal plane and
    filter coordinates.

    The `Transforms` class is designed to map x, y pixel coordinates to
    corresponding focal plane and filter coordinates based on simple polynomial
    transformations. These transformations are accurate within a few
    millimeters and do not account for astrometric distortion, focusing instead
    on efficient and approximate coordinate mappings.

    Bandpasses managed with the `GeneralBandpassInterpolator` class are
    distributed with `Transforms` to map (x, y, sensor) coordinates (typically,
    what we measure) to filter-frame coordinates.

    .. note::
       These transformations are not intended for astrometric precision.

    Parameters
    ----------
    to_focalplane : dict
        Dictionary mapping each sensor ID to polynomial coefficients for
        conversion from pixel coordinates to focal plane coordinates. The
        coefficients are used for 2D polynomial evaluation.

    to_filter : dict
        Dictionary mapping each sensor ID to polynomial coefficients for
        conversion from pixel coordinates to filter frame coordinates. The
        coefficients are used for 2D polynomial evaluation.

    """
    def __init__(self, to_focalplane, to_filter):
        self._to_focalplane = to_focalplane
        self._to_filter = to_filter

    @staticmethod
    def _to_coords(x, y, sensor_id, coords):
        x_out = np.zeros_like(x)
        y_out = np.zeros_like(y)
        for s_id in np.unique(sensor_id):
            idx = s_id == sensor_id
            x_out[idx] = polyval2d(x[idx], y[idx], coords[s_id][0])
            y_out[idx] = polyval2d(x[idx], y[idx], coords[s_id][1])
        return x_out, y_out

    def to_focalplane(self, x, y, sensor_id):
        """
        Maps (x, y, sensor) coordinates to focal plane coordinates.

        Parameters
        ----------
        x : array-like
            x-coordinates in the sensor frame (in pixels)
        y : array-like
            y-coordinates in the sensor frame (in pixels)
        sensor_id : array-like
            Sensor IDs for each x, y coordinate, used to select the appropriate
            focal plane transformation.

        Returns
        -------
        tuple of arrays
            Transformed X, Y coordinates in the focal plane frame.
        """
        return self._to_coords(x, y, sensor_id, self._to_focalplane)

    def to_filter(self, x, y, sensor_id):
        """
        Maps (x, y sensor_id) coordinates to filter frame coordinates.

        Parameters
        ----------
        x : array-like
            x-coordinates in the sensor frame (pixels)
        y : array-like
            Y-coordinates in the sensor frame (pixels)
        sensor_id : array-like
            Sensor IDs for each x, y coordinate, used to select the appropriate
            filter transformation.

        Returns
        -------
        tuple of arrays
            Transformed X, Y coordinates in the filter frame.
        """
        return self._to_coords(x, y, sensor_id, self._to_filter)


class GeneralBandpassInterpolator(object):
    """A general-purpose interpolator for bandpasses with spatial or
    sensor-specific variability.

    This class provides a flexible interpolation for bandpass transmissions
    that may vary across the focal plane due to spatial position,
    sensor-specific quantum efficiency (QE), and/or radial dependence.

    Instances of this class are not Bandpasses themselves, but generate
    Bandpasses at a given focal plane position. This class stores the
    transmission as a function of focal plane position and interpolates between
    the defined positions to return the bandpass at an arbitrary position.

    Parameters
    ----------
    static_transmissions : list of arrays
        Each element is an array representing a static bandpass transmission
        profile over wavelength. The static transmissions are defined
        independently of sensor position.

    specific_sensor_qe : dict, optional
        Dictionary of sensor-specific quantum efficiency (QE) profiles. Keys
        are sensor IDs, and values are arrays defining the wavelength and QE
        values.

    variable_transmission : tuple, optional
        Defines position-dependent transmission. Can be either a radial
        transmission or a 2D spatial transmission, specified as:
            - Radial: (radius, wavelength, transmission)
            - Spatial: (x, y, wavelength, transmission)

    transforms : object, optional
        Transformation object for converting between coordinate frames (e.g.,
        CCD and filter frames).

    prefactor : float, default=1.0
        Scaling factor applied to the transmission values.

    name : str, optional
        Name identifier for the bandpass interpolator instance.

    """
    def __init__(self, static_transmissions, specific_sensor_qe=None,
                 variable_transmission=None, transforms=None, prefactor=1.0,
                 name=None):

        # static transmissions
        self.static_transmissions = [
            interp1d(*tr.T, bounds_error=False, fill_value=0.)
            for tr in static_transmissions]

        # we also need to track the wavelength range on which all the static
        # transmissions are defined
        wl = np.array(
            [(tr[:, 0].min(), tr[:, 0].max()) for tr in static_transmissions])
        static_wl_range = wl[:, 0].max(), wl[:, 1].min()

        # specific sensor quantum efficiencies
        if specific_sensor_qe is not None:
            self.specific_sensor_qe = {
                key: interp1d(
                    *specific_sensor_qe[key].T,
                    bounds_error=False,
                    fill_value=0.)
                for key in specific_sensor_qe}
        else:
            self.specific_sensor_qe = None

        # and finally, the transmissions which vary smoothly as a function of a
        # location parameters, which may be either a radius or a
        self.variable_transmission = None
        if variable_transmission is not None:
            if len(variable_transmission) == 3:
                rad, wl, tr = variable_transmission
                idx = (wl >= static_wl_range[0]) & (wl <= static_wl_range[1])
                wl, tr = wl[idx], tr[:, idx]
                self.wavegrid = wl
                self.wave = (wl.min(), wl.max())
                self.pos = (rad.min(), rad.max())
                self.variable_transmission = \
                    RegularGridInterpolator(
                        [rad, wl],
                        tr,
                        bounds_error=False,
                        fill_value=0.)
                self.radial = True
            elif len(variable_transmission) == 4:
                x, y, wl, tr = variable_transmission
                idx = (wl >= static_wl_range[0]) & (wl <= static_wl_range[1])
                wl, tr = wl[idx], tr[:, :, idx]
                self.wavegrid = wl
                self.wave = (wl.min(), wl.max())
                self.pos = (x.min(), y.min()), (x.max(), y.max())
                self.variable_transmission = \
                    RegularGridInterpolator(
                        [x, y, wl],
                        tr,
                        bounds_error=False,
                        fill_value=0.)
                self.radial = False
            else:
                raise ValueError('unable to handle the transmission data')

        self.transforms = transforms if transforms is not None else None
        self.prefactor = prefactor
        self.name = name

    def minwave(self):
        """Returns the minimum wavelength over which the bandpass is defined"""
        return self.wave[0]

    def maxwave(self):
        """Returns the maximum wavelength over which the bandpass is defined"""
        return self.wave[1]

    def minpos(self):
        """Returns the minimum position in the spatial grid for variable
        bandpasses"""
        return self.pos[0]

    def maxpos(self):
        """Returns the maximim position in the spatial grid for variable
        bandpasses"""
        return self.pos[1]

    def at(self, x, y, sensor_id):
        """Return the bandpass at the specified position

        Parameters
        ----------
        x : float or ndarray
            X-coordinate in pixels or mm, depending on `filter_frame`.
        y : float or ndarray
            Y-coordinate in pixels or mm, depending on `filter_frame`.
        sensor_id : int or ndarray
            Identifier for sensor-specific configurations.

        Returns
        -------
        Bandpass
            The interpolated Bandpass at the specified position.
        """
        trans = self.eval_at(x, y, sensor_id, self.wavegrid).squeeze()
        return Bandpass(self.wavegrid, trans)

    def eval_at(self, x, y, sensor_id, wl, filter_frame=False):
        """Evaluates transmission values at given positions and wavelengths.

        Parameters
        ----------
        x : float or ndarray
            X-coordinates in pixels or mm (depending on `filter_frame`).
        y : float or ndarray
            Y-coordinates in pixels or mm (depending on `filter_frame`).
        sensor_id : int or ndarray
            Sensor ID(s) to specify the quantum efficiency profile.
        wl : ndarray
            Wavelength grid for transmission evaluation.
        filter_frame : bool, default=False
            If True, interprets x and y as coordinates in the filter frame
            (mm), otherwise assumes CCD coordinates (pixels).

        Returns
        -------
        ndarray
            Transmission values array of shape `(len(wl), len(x))`.

        """
        trans = None

        x = np.atleast_1d(x).astype(float)
        y = np.atleast_1d(y).astype(float)
        sensor_id = np.atleast_1d(sensor_id).astype(int)

        if not filter_frame:
            X, Y = self.transforms.to_filter(x, y, sensor_id)
        else:
            X, Y = x, y

        if self.variable_transmission:
            if not self.radial:
                XY = np.vstack((X, Y))
                v = np.array([
                    self.variable_transmission(np.array([
                        np.full(len(wl), x),
                        np.full(len(wl), y), wl]).T)
                    for x, y in XY.T])
                trans = trans * v if trans is not None else v
            else:
                rad = np.sqrt(X**2 + Y**2)
                v = np.array(
                    [self.variable_transmission(np.array([
                        np.full(len(wl), r), wl]).T)
                     for r in rad])
                trans = trans * v if trans is not None else v

        # if not defined, we assume that the qe is in the static transmissions
        if self.specific_sensor_qe:
            # many requested positions may be on the same senors. it is better
            # then to pre-compute the QE's once for all
            qe = {}
            for s_id in np.unique(sensor_id, axis=0):
                qe[s_id] = self.specific_sensor_qe[s_id](wl)
            # and then, we combine them together
            v = np.array([qe[s_id] for s_id in sensor_id])
            trans = trans * v if trans is not None else v

        for tr in self.static_transmissions:
            v = tr(wl)
            trans = trans * v if trans is not None else v

        return trans
