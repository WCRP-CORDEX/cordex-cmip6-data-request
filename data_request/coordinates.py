import re
from .const import height, pressure


def get_vertical_dimension(df, name="height"):
    """Returns a list of vertical coordinates required for the data request"""
    dims = df[df["dimensions"].str.contains(name)].dimensions.unique()
    vdims = [d.split(" ")[-1] for d in dims]
    return list(dict.fromkeys(vdims))


def create_coord(type, value):
    if type == "height":
        coord = height.copy()
        coord["value"] = value
        return coord
    elif type == "p":
        coord = pressure.copy()
        coord["value"] = str(100 * int(value))
        return coord



def get_value_from_str(out_name):
    try:
        return re.search(r"\d+", out_name).group()
    except Exception:
        return None
    
    
def get_coordinates(df):
    coords = []
    for t in ["height", "p"]:
        vdims = get_vertical_dimension(df, t)
        for dim in vdims:
            value = get_value_from_str(dim)
            print(value)
            coords.append(create_coord(t, value))
    return coords
