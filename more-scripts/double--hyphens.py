import os
import json

metadata_files = os.listdir("metadata")

for name in metadata_files:
    with open(f"metadata/{name}", "r") as file:
        file_data = json.load(file)

    # Edit the below
    set_name = file_data["masterSetData"]["setName"]
    if "--" in set_name:
        split_names = set_name.split("--")
        file_data["masterSetData"]["setName"] = "-".join(split_names)

    with open(f"metadata/{name}", "w") as file:
        json.dump(file_data, file, indent=2)