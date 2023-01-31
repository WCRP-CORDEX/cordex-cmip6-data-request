import pandas as pd

import data_request as dr

df = pd.read_csv("./tables/cordex-cmip6-data-request-extended.csv").fillna("")
df

for table in dr.create_cmor_tables(df).values():
    dr.table_to_json(table)
