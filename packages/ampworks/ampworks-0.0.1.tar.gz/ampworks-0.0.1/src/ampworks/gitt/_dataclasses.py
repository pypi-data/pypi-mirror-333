from __future__ import annotations

from typing import TYPE_CHECKING
from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt

if TYPE_CHECKING:  # pragma: no cover
    import numpy.typing as npt


@dataclass(slots=True)
class CellDescription:
    """
    Cell description wrapper

    A dataclass to describe the cell. Requires cell geometry, microstructure,
    and material properties information. Make sure parameters are input with
    the correct units, as described in the documentation.

    Parameters
    ----------
    thick_ed : float
        Electrode thickness [m].
    area_ed : float
        Projected electrode area (e.g., pi*R**2 for coin cells, L*W for pouch
        cells, etc.) [m2].
    eps_el : float
        Electrolyte/pore volume fraction [-].
    eps_CBD : float
        Carbon-binder-domain volume fraction [-]. See notes for more info.
    radius_AM : float
        Active material particle radius [m].
    rho_AM : float
        Active material mass density [kg/m3].
    mass_AM : float
        Total active material mass [kg].
    molar_mass_AM : float
        Active material molar mass [kg/kmol].

    Returns
    -------
    None.

    Notes
    -----
    A "convenient" way to get ``eps_CBD`` requires knowledge of the densities
    and masses for all solid phases in your slurry (carbon additive, binder,
    and active material). The volume fraction for any phase :math:`m` is

    .. math::

        \\varepsilon_{m} = f_{m} \\varepsilon_{\\rm s},

    where :math:`f_{m}` is the volume of phase :math:`m` per volume of solid
    phase and :math:`\\varepsilon_{\\rm s} = 1 - \\varepsilon_{\\rm el}` is
    the total solid-phase volume fraction. :math:`f_{m}` is calculated as

    .. math::

        f_{m} = \\frac{m_{m} / \\rho_{m}}{\\sum_{i=1}^{N} m_{i} / \\rho_{i}},

    Here, the numerator uses the mass and density of phase :math:`m` to get
    its individual volume, and the denominator sums over all :math:`N` solid
    phases to calculate the total solid-phase volume. Using these expressions,
    you can separately calculate volume fractions for the carbon additive and
    binder. Finally, adding their values together gives

    .. math::

        \\varepsilon_{\\rm CBD} = \\varepsilon_{\\rm C}
                                + \\varepsilon_{\\rm B}.

    """

    thick_ed: float
    area_ed: float
    eps_el: float
    eps_CBD: float
    radius_AM: float
    rho_AM: float
    mass_AM: float
    molar_mass_AM: float

    @property
    def volume_ed(self) -> float:
        """Electrode volume [m3]."""
        return self.thick_ed*self.area_ed

    @property
    def spec_capacity_AM(self) -> float:
        """Active material theoretical specific capacity [Ah/kg]."""
        return 96485.33e3 / (3600.*self.molar_mass_AM)

    @property
    def molar_vol_AM(self) -> float:
        """Active material molar volume [m3/kmol]."""
        return self.molar_mass_AM / self.rho_AM

    @property
    def eps_AM(self) -> float:
        """Active material volume fraction [-]."""
        return 1. - self.eps_el - self.eps_CBD

    @property
    def surf_area_AM(self) -> float:
        """Total active material surface area [m2]."""
        return 3.*self.eps_AM*self.volume_ed / self.radius_AM


class GITTDataset:
    """GITT dataclass wrapper"""

    def __init__(self, time: npt.ArrayLike, current: npt.ArrayLike,
                 voltage: npt.ArrayLike, avg_temperature: float,
                 invert_current: bool = False) -> None:
        """
        A dataclass to wrap experimental GITT data.

        Parameters
        ----------
        time : ArrayLike, shape(n,)
            Recorded test times [s].
        current : ArrayLike, shape(n,)
            Timeseries current data [A].
        voltage : ArrayLike, shape(n,)
            Timeseries voltage data [V].
        avg_temperature : float
            Average temperature of the experiment [K].
        invert_current : bool, optional
            Inverts the 'current' sign values. Charge and discharge currents
            should be positive and negative, respectively. Defaults to False.

        Returns
        -------
        None.

        Raises
        ------
        ValueError
            'time' array must be increasing.

        """

        self.time = np.asarray(time)
        self.current = np.asarray(current)
        self.voltage = np.asarray(voltage)
        self.avg_temperature = avg_temperature

        if not all(np.diff(self.time) >= 0.):
            raise ValueError("'time' array must be increasing.")

        if invert_current:
            self.current *= -1.

    def find_pulses(self, pulse_sign: int, plot: bool = False) -> tuple[int]:
        """
        Finds the indices in the data where pulses start and end. The algorithm
        depends on there being a rest period both before and after each pulse.

        Parameters
        ----------
        pulse_sign : int
            The sign of the current pulses to find. Use `+1` or `-1` for
            positive and negative pulses, respectively.
        plot : bool, optional
            Whether or not to plot the result. The default is False.

        Returns
        -------
        start : int
            Indices where pulse starts were detected.
        stop : int
            Indices where pulse stops were detected.

        Raises
        ------
        ValueError
            Invalid pulse_sign value, must be +1 or -1.
        ValueError
            Size mismatch: The number of detected pulse starts and stops do
            not agree. This typically occurs due to a missing rest. You will
            likely need to manually remove affected pulse(s).

        """

        I_pulse = self._avg_pulse_current(pulse_sign)

        if pulse_sign == 1:
            I_tmp = np.where(self.current > 0.5*I_pulse, 1, 0)
        elif pulse_sign == -1:
            I_tmp = np.where(self.current < 0.5*I_pulse, 1, 0)

        idx1 = np.where(np.diff(I_tmp) > 0.9)[0]
        idx2 = np.where(I_tmp > -0.9)[0]
        start = np.intersect1d(idx1, idx2)

        idx1 = np.where(I_tmp > 0.9)[0]
        idx2 = np.where(np.diff(I_tmp) < -0.9)
        stop = np.intersect1d(idx1, idx2)

        if plot:
            plt.figure()
            plt.plot(self.time / 3600., 1e3*self.current, '-k')
            plt.plot(self.time[start] / 3600., 1e3*self.current[start], 'sg')
            plt.plot(self.time[stop] / 3600., 1e3*self.current[stop], 'or')

            plt.xlabel('Time [h]')
            plt.ylabel('Current [mA]')

            plt.show()

        return start, stop

    def get_stats(self, pulse_sign: int) -> dict:

        time = self.time.copy()
        I_pulse = self._avg_pulse_current(pulse_sign)
        start, stop = self.find_pulses(pulse_sign, plot=False)

        stats = {
            'num pulses': start.size,
            'avg I_pulse [A]': I_pulse,
            'avg t_pulse [s]': np.mean(time[stop] - time[start]),
            'avg t_rest [s]': np.mean(time[start[1:]] - time[stop[:-1]]),
        }

        return stats

    def plot(self, y_key: str, t_units: str = 'h') -> None:

        plt.figure()
        if y_key == 'current':
            y, ylabel = self.current.copy(), 'Current [A]'
        elif y_key == 'voltage':
            y, ylabel = self.voltage.copy(), 'Voltage [V]'
        else:
            raise ValueError()

        converter = {
            's': lambda t: t,
            'min': lambda t: t / 60.,
            'h': lambda t: t / 3600.,
            'day': lambda t: t / 3600. / 24.,
        }

        x, xlabel = converter[t_units](self.time), f"Time [{t_units}]"

        plt.plot(x, y)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        plt.show()

    def _avg_pulse_current(self, pulse_sign: int) -> float:

        if pulse_sign == 1:
            I_pulse = np.mean(self.current[self.current > 0.])
        elif pulse_sign == -1:
            I_pulse = np.mean(self.current[self.current < 0.])
        else:
            raise ValueError(f"Invalid {pulse_sign=}, must be +1 or -1.")

        return I_pulse
