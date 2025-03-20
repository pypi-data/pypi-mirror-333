"""Custom Astropy units.

Notes
-----
Executing ``u.Unit("scan")`` without importing ``neclib`` will fail.
To use the units defined here, please import (contents of) ``neclib``, even if they
don't explicitly appear in your script.

"""

__all__ = ["scan", "point", "scan_to_points", "dBm"]

from typing import List

import astropy.units as u

from .types import EquivalencyType

scan = u.def_unit("scan")
"""Custom unit to handle number of scan lines."""

point = u.def_unit("point")
"""Custom unit to handle number of pointing positions."""

dBm: u.DecibelUnit = u.dB(u.mW)
"""Custom unit to handle power in dBm."""

# Enable the use of the units in parsing it like ``u.Unit('scan')``, or other astropy
# functions e.g. ``scan.find_equivalent_units()``
u.add_enabled_units([scan, point])
u.add_enabled_aliases({"dBm": dBm})


def scan_to_points(points_per_scan: int) -> List[EquivalencyType]:
    """Astropy units equivalency, between scan and point.

    Parameters
    ----------
    points_per_scan
        Number of observation points per 1 scan.

    Examples
    --------
    >>> eq = neclib.units.scan_to_point_equivalency(5)
    >>> u.Quantity("5scan").to(neclib.units.point, equivalencies=eq)
    25

    """
    return [(scan, point, lambda x: points_per_scan * x, lambda x: x / points_per_scan)]
