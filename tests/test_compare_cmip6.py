import os
import sys

import pandas as pd
from pytest import fixture

from data_request.cleaning import retrieve_cmip6_mip_tables

sys.path.append(os.path.dirname(__file__) + "/..")


@fixture
def df_cordex():
    return pd.read_csv("./tables/cordex-cmip6-data-request-extended.csv").fillna("")


@fixture
def df_cmip6():
    return retrieve_cmip6_mip_tables()


def test_compare_cmip6(df_cordex, df_cmip6):
    # merge both tables
    merge = pd.merge(
        df_cordex, df_cmip6, on="long_name", suffixes=("_cordex", "_cmip6")
    )
    # check if units are consisten with CMIP6 standard
    units_diff = merge[(merge.units_cordex != merge.units_cmip6)]
    assert units_diff.empty

    # check if types are consisten with CMIP6 standard
    types_diff = merge[merge.type_cordex != merge.type_cmip6]
    assert types_diff.empty
