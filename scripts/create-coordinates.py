import json
from os import path as op

import pandas as pd

import data_request as dr

table_dir = "./"


def table_to_json(table):
    filename = op.join(table_dir, f"{dr.table_prefix}_coordinate.json")
    print(f"writing: {filename}")
    with open(filename, "w") as fp:
        json.dump(table, fp, indent=4)


if __name__ == "__main__":
    df = pd.read_csv("./tables/cordex-cmip6-data-request-extended.csv").fillna("")
    coords = dr.get_coordinate_table(df)
    table_to_json(coords)
