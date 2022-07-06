import os
import sys

import pandas as pd
from pytest import fixture

sys.path.append(os.path.dirname(__file__) + "/..")

import data_request as dr  # noqa: E402


@fixture
def df_cordex():
    return pd.read_csv("./tables/cordex-cmip6-data-request-extended.csv").fillna("")


@fixture
def df_cmip6():
    return dr.retrieve_cmip6_mip_tables()


def test_compare_cmip6(df_cordex, df_cmip6):
    # merge both tables
    merge = pd.merge(
        df_cordex, df_cmip6, on="long_name", suffixes=("_cordex", "_cmip6")
    )
    # check if untis differ
    units_diff = merge[(merge.units_cordex != merge.units_cmip6)]
    assert units_diff.empty
