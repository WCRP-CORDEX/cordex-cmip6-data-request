import re

from . import const


def get_coordinates(out_name, long_name, frequency=None):
    """create the coordinates data request column entry
    
    Requires out_name and long_name which might determine the vertical
    coordinate. The frequency might determine the time coordinate.
    
    """
    time = get_time_axis(frequency)
    vertical = derive_vertical_coord(out_name, long_name)
    coords = "longitude latitude"
    if time is not None:
        coords += f" {time}"
    if vertical is not None:
        # print(vertical)
        vertical = vertical["key"]
        coords += f" {vertical}"
    return coords


def derive_vertical_coord(out_name, long_name=None):
    """derive level type and value from outname

    Be aware that something like od550aer should not
    result in a pressure nor height level.

    """
    if long_name is None:
        long_name = ""
    
    value = get_value_from_out_name(out_name)

    if value is None or int(value) == 0:
        # see https://github.com/WCRP-CORDEX/cordex-cmip6-data-request/issues/7
        if "Near-Surface Wind" in long_name:
            value = "10"
            trail = "m"
        elif "Near-Surface" in long_name:
            value = "2"
            trail = "m"
        else:
            return None
    else:
        trail = out_name.split(value)[1]

    if trail == "m":
        key = const.height_key_template.format(value=value)
        return {"type": "height", "key": key, "value": value}
    elif trail == "":
        key = const.pressure_key_template.format(value=value)
        return {"type": "p", "key": key, "value": value}


def get_time_axis(frequency):
    """Returns time axis name based on frequency"""
    if frequency == "fx" or frequency is None:
        return None
    elif "Pt" in frequency:
        return "time1"
    return "time"


def get_value_from_out_name(out_name):
    """Derive a height or pressure level value from out_name"""
    try:
        return re.search(r"\d+", out_name).group()
    except Exception:
        return None


# old routine to copy attributes from CMIP6 tables
#
# def get_attrs(cmip6, long_name, frequency, out_name):
#     subday = ["1hr", "3hr", "6hr"]
#     subday_pt = ["1hrPt", "3hrPt", "6hrPt"]
#     # attrs = cmip6[(cmip6.long_name == long_name)]
#     var = cmip6[(cmip6.long_name == long_name)]
#     if var.empty:
#         var = cmip6[(cmip6.out_name == out_name)]
#     attrs = var[(var.frequency == frequency)]
#     if len(attrs) == 1:
#         # print(f"found {long_name}, {frequency}")
#         return attrs
#     if len(attrs) > 1:
#         # print(f"not unique: {long_name}, {frequency}, found {len(attrs)}")
#         # print(attrs)
#         attrs = attrs[(attrs.modeling_realm == "atmos")]
#         if len(attrs) == 1:
#             return attrs
#     if attrs.empty:
#         if frequency in subday:
#             for f in subday:
#                 attrs = var[(var.frequency == f)]
#                 if len(attrs) == 1:
#                     print(f"found {long_name}, {f}, {attrs.frequency.values}")
#                     return attrs
#         if frequency in subday_pt:
#             for f in subday_pt:
#                 attrs = var[(var.frequency == f)]
#                 if len(attrs) == 1:
#                     print(f"found {long_name}, {f}, {attrs.frequency.values}")
#                     return attrs
#     print(f"nothing found for {long_name}, {out_name}, {frequency}")
#     return attrs
#
#     # result is not unique, try modeling_realm
#
#
# def add_cmip_data(row):
#     attrs = get_attrs(row.long_name, row.frequency, row.out_name)
#     attrs.rename(
#         columns={"frequency": "frequency_cmip6", "out_name": "out_name_cmip6"},
#         inplace=True,
#     )
#     if attrs.empty:
#         return row
#     for c in attrs:
#         row[c] = attrs[c].values[0]
#     return row
