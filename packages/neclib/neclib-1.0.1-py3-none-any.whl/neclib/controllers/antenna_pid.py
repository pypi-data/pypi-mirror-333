r"""PID controller for telescope main dish.

Optimum control parameter is calculated using a simple function consists of
Proportional, Integral and Derivative terms:

.. math::

    u(t) = K_\mathrm{p} \, e(t)
    + K_\mathrm{i} \int e(\tau) \, \mathrm{d}\tau
    + K_\mathrm{d} \frac{ \mathrm{d}e(t) }{ \mathrm{d}t }

where :math:`K_\mathrm{p}, K_\mathrm{i}` and :math:`K_\mathrm{d}` are non-negative
constants, :math:`u(t)` is the controller's objective parameter, and :math:`e(t)` is the
error between desired and actual values of explanatory parameter.

.. note::

    This script will be executed in high frequency with no vectorization, and there are
    many arrays updated frequently. These mean that the use of Numpy may not be the best
    choice to speed up the calculation. Measure the execution time first, then
    implement.

"""

__all__ = ["PIDController"]

import time as pytime
from contextlib import contextmanager
from typing import ClassVar, Dict, Generator, Literal, Optional, Tuple, Union

import astropy.units as u
import numpy as np
from scipy.interpolate import interp1d

from .. import utils
from ..core import math
from ..core.types import AngleUnit
from ..utils import ParameterList
from ..data import LinearExtrapolate

# Indices for parameter lists.
Last = -2
Now = -1


# Default values for PIDController.
DefaultK_p = 1.0
DefaultK_i = 0.5
DefaultK_d = 0.3
DefaultMaxSpeed = 1.6 << u.deg / u.s
DefaultMaxAcceleration = 1.6 << u.deg / u.s**2
DefaultErrorIntegCount = 50
DefaultThreshold = {
    "cmd_coord_change": 400 << u.arcsec,  # type: ignore
    "accel_limit_off": 20 << u.arcsec,  # type: ignore
    "target_accel_ignore": 2 << u.deg / u.s**2,
}
ThresholdKeys = Literal["cmd_coord_change", "accel_limit_off", "target_accel_ignore"]


class PIDController:
    """PID controller for telescope antenna.

    PID controller, a classical but sophisticated controller for system which has some
    delay on response to some input. This controller handles only 1 device, so use 2
    instances for Az-El control of telescope antenna.

    Parameters
    ----------
    pid_param
        Coefficients for PID formulation, list of [K_p, K_i, K_d].
    max_speed
        Maximum speed for telescope motion.
    max_acceleration
        Maximum acceleration for telescope motion.
    error_integ_count
        Number of error data to be stored for integral term calculation.
    threshold
        Thresholds for conditional executions. Interpreted keys are:

        - ``cmd_coord_change`` (angle)
            If separation between new command coordinate and last one is larger than
            this value, this controller assumes the target coordinate has been changed
            and resets the error integration.
        - ``accel_limit_off`` (angle)
            If separation between encoder reading and command coordinate is smaller than
            this value, this controller stops applying acceleration limit for quick
            convergence of drive.
        - ``target_accel_ignore`` (angular acceleration)
            If acceleration of target coordinate exceeds this value, the
            ``target_speed`` term is ignored as such commands most likely caused by
            software bug or network congestion.

    Attributes
    ----------

    k_p: float
        Proportional term coefficient.
    k_i: float
        Integral term coefficient.
    k_d: float
        Derivative term coefficient.
    k_c: float
        Constant term coefficient.
    max_speed: float
        Upper limit of drive speed in [``ANGLE_UNIT`` / s].
    max_acceleration: float
        Upper limit of drive acceleration in [``ANGLE_UNIT`` / s^2].
    error_integ_count: int
        Number of data stored for error integration.
    threshold: Dict[str, u.Quantity]
        Thresholds for conditional controls.
    cmd_speed: ParameterList[float]
        List of last 2 PID calculation results in unit [``ANGLE_UNIT`` / s].
    time: ParameterList[float]
        List of last ``error_integ_count`` UNIX timestamps the calculations are done.
    cmd_coord: ParameterList[float]
        List of last 2 command coordinates in [``ANGLE_UNIT``].
    enc_coord: ParameterList[float]
        List of last 2 encoder readings in [``ANGLE_UNIT``].
    error: ParameterList[float]
        List of last ``error_integ_count`` deviation values between ``cmd_coord`` and
        ``enc_coord``.
    target_speed: ParameterList[float]
        List of last 2 rate of change of command coordinates in [``ANGLE_UNIT`` / s].

    Notes
    -----
    This controller adds constant term to the general PID formulation. This is an
    attempt to follow constant motions such as raster scanning and sidereal motion
    tracking. ::

        speed = (K_c * target_speed)
            + (k_p * error)
            + (k_i * error_integral)
            + (k_d * error_derivative)

    This class keeps last 50 error values (by default) for integral term. This causes
    optimal PID parameters to change according to PID calculation frequency, as the time
    interval of the integration depends on the frequency.

    Tip
    ---
    All methods assume the argument is given in ``ANGLE_UNIT``, and return the results
    in that unit. If you need to change it, substitute ``ANGLE_UNIT`` before
    instantiating this class.

    Examples
    --------
    >>> neclib.controllers.PIDController.ANGLE_UNIT
    deg
    >>> controller = neclib.controllers.PIDController(
    ...     pid_param=[1.5, 0, 0],
    ...     max_speed="1000 arcsec/s",
    ...     max_acceleration="1.6 deg/s",
    ... )
    >>> target_coordinate, encoder_reading = 30, 10  # deg
    >>> controller.get_speed(target_coordinate, encoder_reading)
    1.430511474609375e-05  # deg/s
    >>> controller.get_speed(target_coordinate, encoder_reading)
    0.20356178283691406  # deg/s

    """

    ANGLE_UNIT: ClassVar[AngleUnit] = "deg"
    """Unit in which all public functions accept as its argument and return."""

    def __init__(
        self,
        *,
        pid_param: Tuple[float, float, float] = (DefaultK_p, DefaultK_i, DefaultK_d),
        max_speed: Union[str, u.Quantity] = DefaultMaxSpeed,
        max_acceleration: Union[str, u.Quantity] = DefaultMaxAcceleration,
        error_integ_count: int = DefaultErrorIntegCount,
        threshold: Dict[ThresholdKeys, Union[str, u.Quantity]] = DefaultThreshold,  # type: ignore  # noqa: E501
    ) -> None:
        self.k_p, self.k_i, self.k_d = pid_param
        self.k_c = 1
        self.max_speed = utils.parse_quantity(max_speed, unit=self.ANGLE_UNIT).value
        self.max_acceleration = utils.parse_quantity(
            max_acceleration, unit=self.ANGLE_UNIT
        ).value
        self.error_integ_count = error_integ_count
        _threshold = DefaultThreshold.copy()
        _threshold.update(threshold)
        self.threshold = {
            k: utils.parse_quantity(v, unit=self.ANGLE_UNIT).value
            for k, v in _threshold.items()
        }

        self.coord_extrapolate = LinearExtrapolate(
            align_by="time", attrs=["time", "coord"]
        )

        # Initialize parameter buffers.
        self._initialize()

    @property
    def dt(self) -> float:
        """Time interval of last 2 PID calculations."""
        return self.enc_time[Now] - self.enc_time[Last]

    @property
    def error_integral(self) -> float:
        """Integral of error."""
        _time, _error = np.array(self.enc_time), np.array(self.error)
        dt = _time[1:] - _time[:-1]
        error_interpolated = (_error[1:] + _error[:-1]) / 2
        return np.nansum(error_interpolated * dt)  # type: ignore

    @property
    def error_derivative(self) -> float:
        """Derivative of error."""
        return (self.error[Now] - self.error[Last]) / self.dt

    def _set_initial_parameters(self, cmd_coord: float, enc_coord: float) -> None:
        """Initialize parameters, except necessity for continuous control."""
        self._initialize()
        now = pytime.time()
        if np.isnan(self.cmd_speed[Now]):
            for i in range(2):
                self.cmd_speed.push(0)
        for i in range(50):
            self.cmd_time.push(now)
            self.cmd_coord.push(cmd_coord)
            self.target_speed.push(0)
        for i in range(2 * int(self.error_integ_count / 2)):
            self.enc_time.push(now)
            self.enc_coord.push(enc_coord)
            self.error.push(cmd_coord - enc_coord)

    def _initialize(self) -> None:
        """Define control loop parameters."""
        if not hasattr(self, "cmd_speed"):
            self.cmd_speed = ParameterList.new(2)
        self.cmd_time = ParameterList.new(50)
        self.enc_time = ParameterList.new(2 * int(self.error_integ_count / 2))
        self.cmd_coord = ParameterList.new(50)
        self.enc_coord = ParameterList.new(2 * int(self.error_integ_count / 2))
        self.error = ParameterList.new(2 * int(self.error_integ_count / 2))
        self.target_speed = ParameterList.new(50)

    def get_speed(
        self,
        cmd_coord: float,
        enc_coord: float,
        stop: bool = False,
        *,
        cmd_time: Optional[float] = None,
        enc_time: Optional[float] = None,
    ) -> float:
        """Modulated drive speed.

        Parameters
        ----------
        cmd_coord
            Instructed Az/El coordinate.
        enc_coord
            Az/El encoder reading.
        stop
            If ``True``, the telescope won't move regardless of the inputs.

        """
        delta_cmd_coord = cmd_coord - self.cmd_coord[Now]
        if (
            np.isnan(self.cmd_time[Now])
            or np.isnan(self.enc_time[Now])
            or (abs(delta_cmd_coord) > self.threshold["cmd_coord_change"])
        ):
            self._set_initial_parameters(cmd_coord, enc_coord)
            # Set default values on initial run or on detection of sudden jump of error,
            # which may indicate a change of command coordinate.
            # This will give too small `self.dt` later, but that won't propose any
            # problem, since `current_speed` goes to 0, and too large target_speed will
            # be ignored in `_calc_pid`.

        current_speed = self.cmd_speed[Now]
        # Encoder readings cannot be used, due to the lack of stability.
        self.enc_time.push(pytime.time() if enc_time is None else enc_time)
        self.enc_coord.push(enc_coord)

        self.cmd_time.push(pytime.time() if cmd_time is None else cmd_time)
        self.cmd_coord.push(cmd_coord)
        error, exted_cmd = self._calc_err()
        self.error.push(error)

        self.target_speed.push(
            (self.cmd_coord[Now] - self.cmd_coord[Last])
            / (self.cmd_time[Now] - self.cmd_time[Last])
        )

        # Calculate and validate drive speed.
        speed = self._calc_pid()

        if abs(self.error[Now]) > self.threshold["accel_limit_off"]:
            # When error is small, smooth control delays the convergence of drive.
            # When error is large, smooth control can avoid overshooting.
            max_diff = max(0, abs(self.max_acceleration) * self.dt)
            # Limit acceleration.
            speed = math.clip(speed, current_speed - max_diff, current_speed + max_diff)
        # Limit speed.
        speed = math.clip(speed, abs(self.max_speed))

        acceleration = (speed - self.cmd_speed[Now]) / self.dt

        if abs(acceleration) > self.max_acceleration:
            max_diff = max(0, abs(self.max_acceleration) * self.dt)
            # Limit acceleration.
            speed = math.clip(speed, current_speed - max_diff, current_speed + max_diff)

        if stop:
            self.cmd_speed.push(0)
        else:
            self.cmd_speed.push(speed)
        return self.cmd_speed[Now]

    def _calc_err(self):
        _cmd = np.array(self.cmd_coord)
        _cmd_time = np.array(self.cmd_time)

        cmd_time = _cmd_time[_cmd_time < self.enc_time[Now]]

        if len(cmd_time) < 2:
            cmd_time = _cmd_time[-2:]
            cmd = _cmd[-2:]
        else:
            cmd = _cmd[: len(cmd_time)]
            cmd_time = cmd_time[-2:]
            cmd = cmd[-2:]

        f = interp1d(cmd_time, cmd, fill_value="extrapolate")
        exted_cmd = float(f(self.enc_time[Now]))
        return exted_cmd - self.enc_coord[Now], exted_cmd

    def _calc_pid(self) -> float:
        # Rate of difference of commanded coordinate. This includes sidereal motion,
        # scan speed, and other non-static component of commanded value.
        target_acceleration = (self.target_speed[Now] - self.target_speed[Last]) / (
            self.cmd_time[Now] - self.cmd_time[Last]
        )
        target_speed = self.target_speed[Now]
        if abs(target_acceleration) > self.threshold["target_accel_ignore"]:
            target_speed = 0

        return (
            self.k_c * target_speed
            + self.k_p * self.error[Now]
            + self.k_i * self.error_integral
            + self.k_d * self.error_derivative
        )

    @contextmanager
    def params(self, **kwargs) -> Generator[None, None, None]:
        original_attrs = {
            "k_p": self.k_p,
            "k_i": self.k_i,
            "k_d": self.k_d,
            "k_c": self.k_c,
            "max_speed": self.max_speed,
            "max_acceleration": self.max_acceleration,
            "error_integ_count": self.error_integ_count,
        }
        original_thresholds = self.threshold.copy()

        for k, v in kwargs.items():
            if k in original_attrs:
                setattr(self, k, v)
            elif k in original_thresholds:
                self.threshold[k] = v
            else:
                raise ValueError(f"Invalid parameter: {k}")

        try:
            yield
        finally:
            for k in original_attrs.keys():
                setattr(self, k, original_attrs[k])
            for k in original_thresholds.keys():
                self.threshold[k] = original_thresholds[k]
