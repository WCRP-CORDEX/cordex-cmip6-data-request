height_key_template = "height{value}m"
pressure_key_template = "p{value}"


height = {
    "standard_name": "height",
    "units": "m",
    "axis": "Z",
    "long_name": "height",
    "climatology": "",
    "formula": "",
    "must_have_bounds": "no",
    "out_name": "height",
    "positive": "up",
    "requested": "",
    "requested_bounds": "",
    "stored_direction": "increasing",
    "tolerance": "",
    "type": "double",
    "valid_max": "",
    "valid_min": "",
    "value": "",
    "z_bounds_factors": "",
    "z_factors": "",
    "bounds_values": "",
    "generic_level_name": "",
}


pressure = {
    "standard_name": "air_pressure",
    "units": "Pa",
    "axis": "Z",
    "long_name": "pressure",
    "climatology": "",
    "formula": "",
    "must_have_bounds": "no",
    "out_name": "plev",
    "positive": "down",
    "requested": "",
    "requested_bounds": "",
    "stored_direction": "",
    "tolerance": "",
    "type": "double",
    "valid_max": "",
    "valid_min": "",
    "value": "",
    "z_bounds_factors": "",
    "z_factors": "",
    "bounds_values": "",
    "generic_level_name": "",
}


def create_coord(type, value):
    if type == "height":
        coord = height.copy()
        coord["value"] = value
        return coord
    elif type == "p":
        coord = pressure.copy()
        coord["value"] = 100 * value
        return coord
