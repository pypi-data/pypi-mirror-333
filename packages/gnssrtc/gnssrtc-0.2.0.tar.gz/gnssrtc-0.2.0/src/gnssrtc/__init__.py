# **************************************************************************************

# @package        gnssrtc
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from .gps import (
    BaseDeviceState,
    GPSUARTDeviceInterface,
)
from .nmea import GPCGGNMEASentence
from .zda import GPZDANMEASentence

# **************************************************************************************

__version__ = "0.2.0"

# **************************************************************************************

__license__ = "MIT"

# **************************************************************************************

__all__: list[str] = [
    "BaseDeviceState",
    "GPCGGNMEASentence",
    "GPSUARTDeviceInterface",
    "GPZDANMEASentence",
]

# **************************************************************************************
