import os
import json

metadata_files = os.listdir("metadata")

for file in metadata_files:
    with open(f"metadata/{file}", "r") as f:
        file_data = json.load(f)

    # Edit file_data
    # First see if it is team aqua or team magma
    if file_data["mainPokemon"].startswith("team-aquas-"):
        team = "team-aqua"
    elif file_data["mainPokemon"].startswith("team-magmas-"):
        team = "team-magma"
    else:
        team = None

    if team is not None:
        file_data["mainPokemon"] = file_data["mainPokemon"][len(team) + 2:]
        file_data["trainerInfo"]["trainerOwned"] = True
        file_data["trainerInfo"]["trainer"] = "team aqua" if team == "team-aqua" else "team magma"

    with open(f"metadata/{file}", "w") as f:
        json.dump(file_data, f, indent=2)