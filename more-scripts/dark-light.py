import os
import json

metadata_files = os.listdir("metadata")

for name in metadata_files:
    with open(f"metadata/{name}", "r") as file:
        file_data = json.load(file)

    rename_flag = False

    # Edit the below
    team = ""
    if rename_flag and file_data["mainPokemon"].startswith("dark-"):
        team = "dark"
        rename_flag = True
    elif rename_flag and file_data["mainPokemon"].startswith("light-"):
        team = "light"
        rename_flag = True

    if file_data["mainEnergy"] == "trainer":
        rename_flag = False

    if rename_flag:
        file_data["mainPokemon"] = file_data["mainPokemon"][len(team) :]

    with open(f"metadata/{name}", "w") as file:
        json.dump(file_data, file, indent=2)
