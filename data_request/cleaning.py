# from urllib.request import urlopen
import json
from pathlib import Path

import pandas as pd

from . import attributes as attrs
from . import cmip6_table_names as tables
from .cell_methods import cell_methods

sheet_id = "1qUauozwXkq7r1g-L4ALMIkCNINIhhCPx"
sheet_name = "Atmos%20CORE"
url = (
    "https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/"
    "tq?tqx=out:csv&sheet={sheet_name}"
)

freqs = ["mon", "day", "6hr", "3hr", "1hr"]


table_map = {
    "mon": "CMIP6_Amon",
    "day": "CMIP6_day",
    "6hr": "CMIP6_3hr",
    "3hr": "CMIP6_3hr",
    "1hr": "CMIP6_3hr",
    "fx": "CMIP6_fx",
}


sheet_names = ["Atmos CORE", "Atmos Tier 1", "Atmos Tier 2"]

excel_url = (
    "https://cordex.org/wp-content/uploads/2022/09/"
    + "CORDEX_CMIP6_Atmosphere_Variable_List.xlsx"
)


# def cmip6_table_list(only=None):
#     """get list of cmip6 cmor tables from github repo"""
#     from github import Github

#     grids = [
#         "CMIP6_CV.json",
#         "CMIP6_coordinate.json",
#         "CMIP6_grids.json",
#         "CMIP6_formula_terms.json",
#     ]
#     drops = []
#     if only is None:
#         only = "variables"
#     if only == "variables":
#         drops = ["CMIP6_input_example.json"] + grids
#     elif only == "grid":
#         return grids
#     g = Github()
#     repo = g.get_repo("PCMDI/cmip6-cmor-tables")
#     contents = repo.get_contents("Tables")
#     return [
#         os.path.basename(c.path)
#         for c in contents
#         if os.path.basename(c.path) not in drops
#     ]


def cmip6_table_list(only=None):
    """get list of cmip6 cmor tables from github repo"""
    if only is None:
        only = "variables"
    if only == "variables":
        return tables.variables
    elif only == "grids":
        return tables.grids
    elif only == "all":
        return tables.variables + tables.grids
    else:
        raise Exception("only should be any variables, grids or all")


def sheet_url(sheet_name):
    """create google spreadsheet url based on sheet name"""
    sheet_name = sheet_name.replace(" ", "%20")
    return url.format(sheet_id=sheet_id, sheet_name=sheet_name)


def retrieve_google_sheet(sheet_name, skiprows=4, clean=True):
    """retrieve single sheet of data request"""
    df = pd.read_csv(sheet_url(sheet_name), skiprows=skiprows)
    if clean is True:
        return clean_df(df)
    return df


def freq_list(row):
    """create list of frequencies from boolean entries ('x')"""
    if row["mon"] == "fx":
        return ["fx"]
    return [f for f in freqs if row[f] == "x"]


def handle_inconsistencies(df):
    """handle some random inconsistencies"""
    df.loc[df["priority"] == "TIER 2", "priority"] = "TIER2"
    df.loc[df["priority"] == "TIER 1", "priority"] = "TIER1"
    return df


def handle_special_cell_methods(df):
    for var, v in cell_methods.items():
        for f, cm in v.items():
            df.loc[(df.out_name == var) & (df.frequency == f), "cell_methods"] = cm
    return df


def clean_df(df, drop=True):
    """tidy up dataframe"""
    # remove unnamed columns
    df = df.loc[:, ~df.columns.str.contains("Unnamed")]

    # lower case column names and renaming to cmip6 formats
    df.columns = df.columns.str.lower()
    df.rename(
        columns={"output variable name": "out_name", "comments": "comment"},
        inplace=True,
    )

    # frequency columns to tidy data
    df["frequency"] = df.apply(lambda row: freq_list(row), axis=1)
    df = df.explode("frequency", ignore_index=True)

    df = handle_inconsistencies(df)  # set correct frequency name for point values

    subdaily_pt = (df["frequency"].isin(["1hr", "3hr", "6hr"])) & (df["ag"] == "i")
    # set frequency, we don't do that anymore,
    # see https://github.com/WCRP-CORDEX/cordex-cmip6-data-request/issues/24
    # df.loc[subdaily_pt, "frequency"] = df[subdaily_pt].frequency + "Pt"

    # set cell methods depending on frequency
    df["cell_methods"] = "area: mean time: mean"
    df.loc[subdaily_pt, "cell_methods"] = "area: mean time: point"

    # update some more cell_methods
    df = update_cell_methods(df)

    # remove trailing formatters
    df.replace(r"\n", " ", regex=True, inplace=True)
    strip_cols = ["standard_name", "long_name"]
    for col in strip_cols:
        df[col] = df[col].str.strip()
    if drop is True:
        df.drop(columns=freqs, inplace=True)
        df.drop(columns=["ag"], inplace=True)
        df = df.dropna(subset=["out_name", "frequency"], how="all")

    # handle min max cell_methods
    df.loc[df.out_name.str.contains("min"), "cell_methods"] = "area: mean time: minimum"
    df.loc[df.out_name.str.contains("max"), "cell_methods"] = "area: mean time: maximum"

    # handle special cases
    df = handle_special_cell_methods(df)

    # set these to lowercase
    lowercase = ["CAPE", "LI", "CIN", "CAPEmax", "LImax", "CINmax"]
    lc = df.out_name.isin(lowercase)

    df.loc[lc, "out_name"] = df[lc].out_name.str.lower()

    return df


def update_cell_methods(df):
    # special fx cases
    df.loc[df.frequency == "fx", "cell_methods"] = "area: mean"

    # flux units, see https://github.com/WCRP-CORDEX/cordex-cmip6-data-request/issues/23
    df.loc[df.units == "W m-2", "cell_methods"] = "area: time: mean"

    return df


# def update_df(df):
#    subdaily_pt = df["frequency"].isin(["1hrPt", "3hrPt", "6hrPt"])
#    df["cell_methods"] = "area: mean time: mean"
#    df.loc[subdaily_pt, "cell_methods"] = "area: mean time: point"
#    return df


def get_jsonparsed_data(url):
    """
    Cache the content of ``url``, parse it as JSON and return the object.
    """
    import pooch

    filename = pooch.retrieve(url, known_hash=None)
    with open(filename, "r") as f:
        return json.load(f)


def get_cmip6_cmor_table(table):
    """get cmip6 cmor table"""
    table = Path(table).stem
    if "CMIP6" not in table:
        table = "CMIP6_" + table
    url = (
        "https://raw.githubusercontent.com/PCMDI/cmip6-cmor-tables/"
        f"master/Tables/{table}.json"
    )
    return get_jsonparsed_data(url)


def retrieve_data_request(sheet_name=None, skiprows=6, clean=True):
    """retrieve data from cordex data request website

    Retrieves data from
    https://cordex.org/wp-content/uploads/2022/03/CORDEX_CMIP6_Atmosphere_Variable_List.xlsx
    and merges all sheets and cleans table structure.

    """
    if sheet_name is None:
        sheet_name = sheet_names
    data = pd.read_excel(
        excel_url,
        sheet_name=sheet_name,
        skiprows=skiprows,
        converters={"units": str},
    )
    try:
        df = pd.concat(data.values())
    except Exception:
        df = data
    if clean is True:
        return clean_df(df)
    return df


def get_variable_entry(table, variable):
    """retrieve variable entry from a CMIP6 cmor table"""
    return get_cmip6_cmor_table(table)["variable_entry"][variable]


def get_variable_entries_by_attributes(table, how=None, **kwargs):
    """retrieve variable entry from a CMIP6 cmor table

    Returns all variable entries from a CMIP6 cmor table depending
    on kwargs.

    Parameters
    ----------
    table : str
        CMIP6 cmor table name
        e.g. 'CMIP_Amon' or 'Amon', ...
    how : str
        How to evaluate search results, can be ``"any"`` or ``"all"``.
        Defaults to ``"all"``
    **kwargs:
        Keyword arguments used for searching in variable entry attributes.

    Returns
    -------
    results : dict
        Dictionary of variable entries.

    """
    if how is None:
        how = "all"
    variable_entries = get_cmip6_cmor_table(table)["variable_entry"]
    results = {}
    for key, entry in variable_entries.items():
        founds = [entry[attr] == value for attr, value in kwargs.items()]
        if eval(f"{how}({founds})") is True:
            results[key] = entry
    return results


def get_all_variable_entries_by_attributes(how="any", tables=None, **kwargs):
    """retrieve variable entry from all cmor tables

    Returns all variable entries from all CMIP6 cmor table depending
    on kwargs.

    Parameters
    ----------
    how : str
        How to evaluate search results, can be ``"any"`` or ``"all"``.
        Defaults to ``"all"``
    **kwargs:
        Keyword arguments used for searching in variable entry attributes.

    Returns
    -------
    results : dict
        Dictionary of cmip6 cmor tables with variable entries.

    """
    results = {}
    if tables is None:
        tables = cmip6_table_list()
    for t in tables:
        entries = get_variable_entries_by_attributes(t, how=how, **kwargs)
        if entries:
            results[t] = entries
    return results


def retrieve_cmip6_mip_tables():
    """retrieve and concat all cmip6 mip tables from
    https://c6dreq.dkrz.de/docs/CMIP6_MIP_tables.xlsx
    """
    cols = [
        "frequency",
        "modeling_realm",
        "standard_name",
        "units",
        "cell_methods",
        "cell_measures",
        "long_name",
        "comment",
        "dimensions",
        "out_name",
        "type",
        "positive",
        "valid_min",
        "valid_max",
        "ok_min_mean_abs",
        "ok_max_mean_abs",
        "cmip6_table",
    ]
    cmip6_mip_tables_url = "https://c6dreq.dkrz.de/docs/CMIP6_MIP_tables.xlsx"
    tables = pd.read_excel(cmip6_mip_tables_url, sheet_name=None)
    del tables["Notes"]

    def add_table_name(df, table):
        df["cmip6_table"] = table
        return df

    df = pd.concat(add_table_name(df, table) for table, df in tables.items())
    df.rename(
        columns={
            "CF Standard Name": "standard_name",
            "Long name": "long_name",
            "Variable Name": "out_name",
        },
        inplace=True,
    )
    return df[cols].drop_duplicates(ignore_index=True)


def add_coordinates(row):
    return attrs.get_coordinates(row.out_name, row.long_name, row.cell_methods)


def add_cmip6_attributes(df):
    df = df.copy()
    attrs = {
        "frequency": "",
        "modeling_realm": "atmos",
        "standard_name": "",
        "units": "K",
        "cell_methods": "",
        "cell_measures": "area: areacella",
        "long_name": "",
        "comment": "",
        "dimensions": "",
        "out_name": "tas",
        "type": "real",
        "positive": "",
        "valid_min": "",
        "valid_max": "",
        "ok_min_mean_abs": "",
        "ok_max_mean_abs": "",
    }
    for key, value in attrs.items():
        if key not in df:
            df[key] = value
    df["dimensions"] = df.apply(add_coordinates, axis=1)
    return df
