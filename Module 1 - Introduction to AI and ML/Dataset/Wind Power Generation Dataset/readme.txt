The columns in the data are as follows:

Time - Hour of the day when readings occurred
temperature_2m - Temperature in degrees Fahrenheit at 2 meters above the surface
relativehumidity_2m - Relative humidity (as a percentage) at 2 meters above the surface
dewpoint_2m - Dew point in degrees Fahrenheit at 2 meters above the surface
windspeed_10m - Wind speed in meters per second at 10 meters above the surface
windspeed_100m - Wind speed in meters per second at 100 meters above the surface
winddirection_10m - Wind direction in degrees (0-360) at 10 meters above the surface (see notes)
winddirection_100m - Wind direction in degrees (0-360) at 100 meters above the surface (see notes)
windgusts_10m - Wind gusts in meters per second at 100 meters above the surface
Power - Turbine output, normalized to be between 0 and 1 (i.e., a percentage of maximum potential output)

Notes:
	1) Likely many of these variables will not be very relevant. They are included here but do not need to be included in the final models.
	2) Degrees are measured from 0 to 360. Since 0 and 360 represent the same spot on a circle, consider transforming these using sine and/or cosine. Also consider converting them to radians, instead of degrees.
	3) Each location can have a different model. There is no reason to build one model to work for all locations.

