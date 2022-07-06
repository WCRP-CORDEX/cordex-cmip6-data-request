import re

import coordinates as coords


def derive_vertical_coord_from_outname(outname):
    """derive level type and value from outname

    Be aware that something like od550aer should not
    result in a pressure nor height level.

    """
    value = get_value_from_outname(outname)
    trail = outname.split(value)[1]
    if value is None or int(value) == 0:
        return None
    elif trail == "m":
        key = coords.height_key_template.format(value=value)
        return {"type": "height", "key": key, "value": value}
    elif trail == "":
        key = coords.pressure_key_template.format(value=value)
        return {"type": "p", "key": key, "value": value}


def get_vertical_coord_attrs(outname):
    pass


def get_time_axis(frequency):
    if frequency == "fx" or frequency is None:
        return None
    elif "Pt" in frequency:
        return "time1"
    return "time"


def get_coordinates(outname, frequency=None):
    time = get_time_axis(frequency)
    vertical = derive_vertical_coord_from_outname(outname)
    coords = "longitude latitude"
    if time is not None:
        coords += f" {time}"
    if vertical is not None:
        coords += f" {vertical}"
    return coords


def get_value_from_outname(outname):
    try:
        return re.search(r"\d+", outname).group()
    except Exception:
        return None
