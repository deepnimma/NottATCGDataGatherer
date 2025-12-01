import os
import json

metadata_files = os.listdir("metadata")

for name in metadata_files:
    with open(f"metadata/{name}", "r") as file:
        file_data = json.load(file)

    # Edit the below
    if not file_data["hasReverseHolo"]:
        print(f"Removing {name} | {file_data["hasReverseHolo"]}")
        os.remove(f"metadata/{name}")
        os.remove(f"images/{name[:-5]}.png")
