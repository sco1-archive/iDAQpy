# iDAQpy
Python Toolkit for the Wamore iDAQ


### iDAQ Data Log Specification
The following table describes the full output of the Wamore iDAQ.

| Parameter<sup>1</sup> | Description                                             |        Unit     |
|:---------------------:|:-------------------------------------------------------:|:---------------:|
| `time`                | Time since DAQ was powered on                           | millisecond     |
| `xgyro`               | X gyro output, with 0.05 deg/sec resolution             | deg/sec         |
| `ygyro`               | Y gyro output, with 0.05 deg/sec resolution             | deg/sec         |
| `zgyro`               | Z gyro output, with 0.05 deg/sec resolution             | deg/sec         |
| `xaccel`              | X accelerometer output, with 0.00333 G resolution       | Gee             |
| `yaccel`              | Y accelerometer output, with 0.00333 G resolution       | Gee             |
| `zaccel`              | Z accelerometer output, with 0.00333 G resolution       | Gee             |
| `link1`               | Raw strain link ADC data, must be converted to force    |                 |
| `link2`               | Raw strain link ADC data, must be converted to force    |                 |
| `link3`               | Raw strain link ADC data, must be converted to force    |                 |
| `link4`               | Raw strain link ADC data, must be converted to force    |                 |
| `link5`               | Raw strain link ADC data, must be converted to force    |                 |
| `adc1`                | Internal DAQ value, engineering use only                |                 |
| `adc2`                | On-board 5V supply monitor                              |                 |
| `adc3`                | Internal DAQ value, engineering use only                |                 |
| `adc4`                | Internal DAQ value, engineering use only                |                 |
| `adc5`                | Approximate battery voltage                             |                 |
| `adc6`                | On-board 3.3V supply monitor                            |                 |
| `adc7`                | User input analog voltage #1, 0V to 4.0V                |                 |
| `adc8`                | User input analog voltage #2, 0V to 4.0V                |                 |
| `adctemp`             | Internal DAQ value, engineering use only                |                 |
| `din1`                | Digital input #1 - Lanyard switch status                | Bool            |
| `din2`                | General purpose digital input: 0-Low 1-High             | Bool            |
| `din3`                | General purpose digital input: 0-Low 1-High             | Bool            |
| `din4`                | General purpose digital input: 0-Low 1-High             | Bool            |
| `pwrsw`               | Power switch status: 0-Pressed 1- Open                  | Bool            |
| `pstemp`              | Temperature reported by the pressure sensor             | Degrees Celsius |
| `pressure`            | Temperature reported by the pressure sensor             | Pascal          |
| `GPSMsgs`             | Number of NMEA GPS mesages received from the GPS module | Int             |
| `GPSValid`            | GPS valid signal: V-Navigation warning A-Valid Data     | Str             |
| `GPSMode`             | GPS mode: M-Manual A-Automatic                          | Str             |
| `GPSFixMode`          | GPS fix mode; 1-Fix not available 2-2D fix 3-3D fix     | Int             |
| `GPSDateTime`         | GPS date and time, YYYYMMDD-HHMMSS                      | Str             |
| `GPSSatsInView`       | Number of satellites in view                            | Int             |
| `GPSSatsInUse`        | Number of satellites in use                             | Int             |
| `GPSLatitude`         | GPS Latitude                                            | Decimal Degree  |
| `GPSLongitude`        | GPS Longitude                                           | Decimal Degree  |
| `GPSAltitude`         | GPS Altitude, meters                                    | Meter           |
| `GPSGroundSpeed`      | GPS Groundspeed, knots true                             | Knots True      |

1. Parameter names correspond to the raw CSV output of the logdecoder

**NOTE:** The default sample rate is 1000 Hz. Data acquired at a lower rate is interpolated on the hardware/decoder side to match the timestamps.
