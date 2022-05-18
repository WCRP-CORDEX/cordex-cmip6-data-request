

import pandas as pd


sheet_id = "1qUauozwXkq7r1g-L4ALMIkCNINIhhCPx"
sheet_name = "Atmos%20CORE"
url = "https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

freqs = ["mon", "day", "6hr", "3hr", "1hr"]

sheet_names = ["Atmos CORE", "Atmos Tier 1", "Atmos Tier 2"]

excel_url = "https://cordex.org/wp-content/uploads/2022/03/CORDEX_CMIP6_Atmosphere_Variable_List.xlsx"

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
    if row["mon"] == "fx":
        return ["fx"]
    return [f for f in freqs if row[f] == "x"]


def handle_inconsistencies(df):
    """handle random inconsistencies"""
    df.loc[df["priority"] == "TIER2", "priority"] = "TIER 2"
    df.loc[df["priority"] == "TIER1", "priority"] = "TIER 1"
    return df


def clean_df(df, drop=True):
    """tidy up dataframe"""
    # remove unnamed columns
    df = df.loc[:, ~df.columns.str.contains('Unnamed')]
    # lower case column names
    df.columns= df.columns.str.lower()
    # frequency columns to tidy data
    df['frequency'] = df.apply (lambda row: freq_list(row), axis=1)
    df = df.explode("frequency", ignore_index=True)
    df = handle_inconsistencies(df)
    if drop is True:
        df = df.drop(columns=freqs)
        df = df.dropna(how="all")
    return df


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






    