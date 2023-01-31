# flake8: noqa
"""Maximum/minimum values and averaging

Maximum/minimum values (tasmax, tasmin, sfcWindmax and wsgsmax) are defined as the
maximum/minimum from all integrated time steps per day. Daily Maximum Hourly Precipitation
Rate (prhmax) is defined as the maximum of the precipitation rate averaged over the whole hour.
Daily output is an average of subdaily output with exception of maximum/minimum
variables (tasmax, tasmin, sfcWindmax, prhmax and wsgsmax) and accumulated sunshine
duration (sund). Monthly output for all variables is an average of daily values.
"""

cell_methods = {}

cell_methods["areacella"] = {"fx": "area: sum"}
"""
CMIP6_6hrPlev.json-        "prhmax": {
CMIP6_6hrPlev.json-            "frequency": "6hr",
CMIP6_6hrPlev.json-            "modeling_realm": "atmos",
CMIP6_6hrPlev.json-            "standard_name": "precipitation_flux",
CMIP6_6hrPlev.json-            "units": "kg m-2 s-1",
CMIP6_6hrPlev.json:            "cell_methods": "area: mean time: mean within hours time: maximum over hours",

--
CMIP6_Eday.json-        "prhmax": {
CMIP6_Eday.json-            "fr®equency": "day",
CMIP6_Eday.json-            "modeling_realm": "atmos",
CMIP6_Eday.json-            "standard_name": "precipitation_flux",
CMIP6_Eday.json-            "units": "kg m-2 s-1",
CMIP6_Eday.json:            "cell_methods": "area: mean time: mean within hours time: maximum over hours",

CMIP6_Emon.json-        "prhmax": {
CMIP6_Emon.json-            "frequency": "mon",
CMIP6_Emon.json-            "modeling_realm": "atmos",
CMIP6_Emon.json-            "standard_name": "precipitation_flux",
CMIP6_Emon.json-            "units": "kg m-2 s-1",
CMIP6_Emon.json:            "cell_methods": "area: mean time: mean within hours time: maximum over hours",
--

"""

cell_methods["prhmax"] = {
    "6hr": "area: mean time: mean within hours time: maximum over hours",
    "day": "area: mean time: mean within hours time: maximum over hours",
    "mon": "area: mean time: mean within hours time: maximum over hours",
}


"""

CMIP6_Amon.json-        "tasmax": {
CMIP6_Amon.json-            "frequency": "mon",
CMIP6_Amon.json-            "modeling_realm": "atmos",
CMIP6_Amon.json-            "standard_name": "air_temperature",
CMIP6_Amon.json-            "units": "K",
CMIP6_Amon.json:            "cell_methods": "area: mean time: maximum within days time: mean over days",
CMIP6_Amon.json-            "cell_measures": "area: areacella",
CMIP6_Amon.json-            "long_name": "Daily Maximum Near-Surface Air Temperature",
CMIP6_Amon.json:            "comment": "maximum near-surface (usually, 2 meter) air temperature (add cell_method attribute 'time: max')",

CMIP6_day.json-        "tasmax": {
CMIP6_day.json-            "frequency": "day",
CMIP6_day.json-            "modeling_realm": "atmos",
CMIP6_day.json-            "standard_name": "air_temperature",
CMIP6_day.json-            "units": "K",
CMIP6_day.json:            "cell_methods": "area: mean time: maximum",
CMIP6_day.json-            "cell_measures": "area: areacella",
CMIP6_day.json-            "long_name": "Daily Maximum Near-Surface Air Temperature",
CMIP6_day.json:            "comment": "maximum near-surface (usually, 2 meter) air temperature (add cell_method attribute 'time: max')",

--
"""

cell_methods["tasmax"] = {
    "mon": "area: mean time: maximum within days time: mean over days",
    "day": "area: mean time: maximum",
}

"""
--
CMIP6_Amon.json-        "tasmin": {
CMIP6_Amon.json-            "frequency": "mon",
CMIP6_Amon.json-            "modeling_realm": "atmos",
CMIP6_Amon.json-            "standard_name": "air_temperature",
CMIP6_Amon.json-            "units": "K",
CMIP6_Amon.json:            "cell_methods": "area: mean time: minimum within days time: mean over days",
CMIP6_Amon.json-            "cell_measures": "area: areacella",
CMIP6_Amon.json-            "long_name": "Daily Minimum Near-Surface Air Temperature",
CMIP6_Amon.json:            "comment": "minimum near-surface (usually, 2 meter) air temperature (add cell_method attribute 'time: min')",


CMIP6_day.json-        "tasmin": {
CMIP6_day.json-            "frequency": "day",
CMIP6_day.json-            "modeling_realm": "atmos",
CMIP6_day.json-            "standard_name": "air_temperature",
CMIP6_day.json-            "units": "K",
CMIP6_day.json:            "cell_methods": "area: mean time: minimum",
CMIP6_day.json-            "cell_measures": "area: areacella",
CMIP6_day.json-            "long_name": "Daily Minimum Near-Surface Air Temperature",
CMIP6_day.json:            "comment": "minimum near-surface (usually, 2 meter) air temperature (add cell_method attribute 'time: min')",

"""

cell_methods["tasmin"] = {
    "mon": "area: mean time: minimum within days time: mean over days",
    "day": "area: mean time: minimum",
}


"""


CMIP6_Emon.json-        "sfcWindmax": {
CMIP6_Emon.json-            "frequency": "mon",
CMIP6_Emon.json-            "modeling_realm": "atmos",
CMIP6_Emon.json-            "standard_name": "wind_speed",
CMIP6_Emon.json-            "units": "m s-1",
CMIP6_Emon.json:            "cell_methods": "area: mean time: maximum within days time: mean over days",

--
CMIP6_day.json-        "sfcWindmax": {
CMIP6_day.json-            "frequency": "day",
CMIP6_day.json-            "modeling_realm": "atmos",
CMIP6_day.json-            "standard_name": "wind_speed",
CMIP6_day.json-            "units": "m s-1",
CMIP6_day.json:            "cell_methods": "area: mean time: maximum",
--

"""

cell_methods["sfcWindmax"] = {
    "mon": "area: mean time: maximum within days time: mean over days",
    "day": "area: mean time: maximum",
}


"""
--
CMIP6_day.json-        "hursmax": {
CMIP6_day.json-            "frequency": "day",
CMIP6_day.json-            "modeling_realm": "atmos",
CMIP6_day.json-            "standard_name": "relative_humidity",
CMIP6_day.json-            "units": "%",
CMIP6_day.json:            "cell_methods": "area: mean time: maximum",


CMIP6_AERday.json-        "minpblz": {
CMIP6_AERday.json-            "frequency": "day",
CMIP6_AERday.json-            "modeling_realm": "aerosol",
CMIP6_AERday.json-            "standard_name": "atmosphere_boundary_layer_thickness",
CMIP6_AERday.json-            "units": "m",
CMIP6_AERday.json:            "cell_methods": "area: mean time: minimum",
CMIP6_AERday.json-            "cell_measures": "area: areacella",
CMIP6_AERday.json-            "long_name": "Minimum PBL Height",
CMIP6_AERday.json:            "comment": "minimum boundary layer height during the day (add cell_methods attribute: 'time: minimum')",

--
CMIP6_Eday.json-        "hursminCrop": {
CMIP6_Eday.json-            "frequency": "day",
CMIP6_Eday.json-            "modeling_realm": "atmos",
CMIP6_Eday.json-            "standard_name": "relative_humidity",
CMIP6_Eday.json-            "units": "%",
CMIP6_Eday.json:            "cell_methods": "area: mean where crops time: minimum",
--
CMIP6_Eday.json-        "tasminCrop": {
CMIP6_Eday.json-            "frequency": "day",
CMIP6_Eday.json-            "modeling_realm": "atmos",
CMIP6_Eday.json-            "standard_name": "air_temperature",
CMIP6_Eday.json-            "units": "K",
CMIP6_Eday.json:            "cell_methods": "area: mean where crops time: minimum",
CMIP6_Eday.json-            "cell_measures": "area: areacella",
CMIP6_Eday.json-            "long_name": "Daily Minimum Near-Surface Air Temperature over Crop Tile",
CMIP6_Eday.json:            "comment": "minimum near-surface (usually, 2 meter) air temperature (add cell_method attribute 'time: min')",
--
CMIP6_Emon.json-        "hursminCrop": {
CMIP6_Emon.json-            "frequency": "mon",
CMIP6_Emon.json-            "modeling_realm": "atmos",
CMIP6_Emon.json-            "standard_name": "relative_humidity",
CMIP6_Emon.json-            "units": "%",
CMIP6_Emon.json:            "cell_methods": "area: mean where crops time: minimum within days time: mean over days",
--
CMIP6_Emon.json-        "tasminCrop": {
CMIP6_Emon.json-            "frequency": "mon",
CMIP6_Emon.json-            "modeling_realm": "atmos",
CMIP6_Emon.json-            "standard_name": "air_temperature",
CMIP6_Emon.json-            "units": "K",
CMIP6_Emon.json:            "cell_methods": "area: mean where crops time: minimum within days time: mean over days",
CMIP6_Emon.json-            "cell_measures": "area: areacella",
CMIP6_Emon.json-            "long_name": "Daily Minimum Near-Surface Air Temperature over Crop Tile",
CMIP6_Emon.json:            "comment": "minimum near-surface (usually, 2 meter) air temperature (add cell_method attribute 'time: min')",
--
CMIP6_Omon.json-        "mlotstmin": {
CMIP6_Omon.json-            "frequency": "mon",
CMIP6_Omon.json-            "modeling_realm": "ocean",
CMIP6_Omon.json-            "standard_name": "ocean_mixed_layer_thickness_defined_by_sigma_t",
CMIP6_Omon.json-            "units": "m",
CMIP6_Omon.json:            "cell_methods": "area: mean time: minimum",
--
CMIP6_day.json-        "hursmin": {
CMIP6_day.json-            "frequency": "day",
CMIP6_day.json-            "modeling_realm": "atmos",
CMIP6_day.json-            "standard_name": "relative_humidity",
CMIP6_day.json-            "units": "%",
CMIP6_day.json:            "cell_methods": "area: mean time: minimum",
--


"""
