# **************************************************************************************

# @package        gnssrtc
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import time

from gnssrtc.gps import GPSUARTDeviceInterface

# **************************************************************************************

gps = GPSUARTDeviceInterface(port="/dev/ttyAMA0", baudrate=115200)

# **************************************************************************************

if __name__ == "__main__":
    gps.connect()

    try:
        while gps.is_ready():
            data = gps.get_nmea_data()

            if data:
                print(data)

            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        gps.disconnect()

# **************************************************************************************
