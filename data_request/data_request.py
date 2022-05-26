# from urllib.request import urlopen
import json
from pathlib import Path

import pandas as pd

from . import tables

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
    "https://cordex.org/wp-content/uploads/2022/03/"
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


def clean_df(df, drop=True):
    """tidy up dataframe"""
    # remove unnamed columns
    df = df.loc[:, ~df.columns.str.contains("Unnamed")]
    # lower case column names
    df.columns = df.columns.str.lower()
    # frequency columns to tidy data
    df["frequency"] = df.apply(lambda row: freq_list(row), axis=1)
    df = df.explode("frequency", ignore_index=True)
    df = handle_inconsistencies(df)
    if drop is True:
        df = df.drop(columns=freqs)
        df = df.dropna(how="all")
    return df


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
    data = pd.read_excel(excel_url, sheet_name=sheet_name, skiprows=skiprows)
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


def get_all_variable_entries_by_attributes(how="any", **kwargs):
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
    for t in cmip6_table_list():
        entries = get_variable_entries_by_attributes(t, how=how, **kwargs)
        if entries:
            results[t] = entries
    return results


def create_table_header(name):
    from datetime import date

    today = date.today()
    header = {
        "data_specs_version": "01.00.33",
        "cmor_version": "3.5",
        "table_id": f"Table {name}",
        "realm": "atmos",
        "table_date": today.strftime("%d %B %Y"),
        "missing_value": "1e20",
        "int_missing_value": "-999",
        "product": "model-output",
        "approx_interval": "30.00000",
        "generic_levels": "alevel alevhalf",
        "mip_era": "CMIP6",
        "Conventions": "CF-1.7 CMIP-6.2",
    }
    return header


def create_cmor_table(name, df):
    return dict(
        Header=create_table_header(name),
        variable_entry=df.set_index("output variable name").to_dict(
            orient="index"
        ),
    )


def create_cmor_tables(df, groupby="frequency"):
    """Create cmor tables depending on grouped attribute"""

    def name(g):
        if isinstance(g, tuple):
            return "_".join(g)
        return g

    gb = df.groupby(groupby)
    return {
        name(g): create_cmor_table(name(g), gb.get_group(g)) for g in gb.groups
    }


def table_to_json(table):
    import json

    table_id = table["Header"]["table_id"].split()[1]
    filename = f"CORDEX-CMIP6_{table_id}.json"
    print(f"writing: {filename}")
    with open(filename, "w") as fp:
        json.dump(table, fp, indent=4)
