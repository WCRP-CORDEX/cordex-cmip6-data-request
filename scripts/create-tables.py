import pandas as pd

import data_request as dr
from data_request.utils import table_to_json

if __name__ == "__main__":
    df = pd.read_csv("./tables/cordex-cmip6-data-request-extended.csv").fillna("")
    for table in dr.create_cmor_tables(df).values():
        table_to_json(table)
