import os
import json

metadata_files = os.listdir("metadata")

for name in metadata_files:
    with open(f"metadata/{name}", "r") as file:
        file_data = json.load(file)

    # Edit the below
    if file_data["cardTitle"].endswith(" ex") or file_data["cardTitle"].endswith(" break"):
        os.remove(f"metadata/{name}")
        os.remove(f"images/{name[:-5]}.png")
        continue


    with open(f"metadata/{name}", "w") as file:
        json.dump(file_data, file, indent=2)
