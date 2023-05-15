import re

from .const import dim_table


def create_coord(dim_type, value):
    coord_entry = dim_table[dim_type].copy()
    coord_entry["value"] = str(100 * int(value)) if dim_type == "p" else value
    return coord_entry


def get_value_from_str(out_name):
    try:
        return re.search(r"\d+", out_name).group()
    except Exception:
        return None


def get_unique_dims(df):
    dims_list = list(df.dimensions.unique())
    splits = []
    for d in dims_list:
        splits.extend(d.split())
    return list(dict.fromkeys(splits))


def create_dimension_entry(dim):
    dim_type = re.sub(r"[0-9]", "", dim)  # remove digits
    if dim_type in ["heightm", "p"]:
        value = get_value_from_str(dim)
        return create_coord(dim_type, value)
    return dim_table[dim].copy()


def get_coordinate_table(df):
    dims = get_unique_dims(df)
    dims.sort()
    print(f"found: {dims}")
    return {"axis_entry": {d: create_dimension_entry(d) for d in dims}}
