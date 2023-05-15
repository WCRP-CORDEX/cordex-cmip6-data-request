import json
import os

from .const import table_prefix


def table_to_json(table, dir=None, prefix=None):
    if dir is None:
        dir = "./"
    if prefix is None:
        prefix = table_prefix
    if not os.path.isdir(dir):
        os.makedirs(dir)
    table_id = table["Header"]["table_id"].split()[1]
    filename = os.path.join(dir, f"{prefix}_{table_id}.json")
    print(f"writing: {filename}")
    with open(filename, "w") as fp:
        json.dump(table, fp, indent=4)
