import os
import json

# MUST BE MOVED TO THE SAME FOLDER AS METADATA AND IMAGES
# ...
# | - ./images
# | - ./metadata
# | - prune.py

metadata_files = os.listdir("./metadata")
print(len(metadata_files))

data: list[dict] = []
for file in metadata_files:
    with open(f"./metadata/{file}", "r") as file:
        data.append(json.load(file))


def handle_lt_surge(data: dict) -> dict:
    lt_owner = "lt-surge"
    lt_trainer_name = "lt. surge"
    lt_owner_len = len(lt_owner) + 2
    lt_cameo_pokemon = ["lt-surge", "lt. surge", "lt surge", "lt.-surge"]

    data["mainPokemon"] = d["mainPokemon"][lt_owner_len::]
    data["trainerInfo"]["trainerOwned"] = True
    data["trainerInfo"]["trainer"] = lt_trainer_name
    data["cameoPokemon"] = lt_cameo_pokemon

    return data


new_data: list[dict] = []
for d in data:
    if d["trainerInfo"]["item"]:
        new_data.append(d)
    elif d.get("mainPokemon").startswith("lt-surges-"):
        new_data.append(handle_lt_surge(d))
    else:
        owner = d.get("cardTitle").split(" ")[0]
        # remove 's
        owner = owner[:-2]
        owner_len = len(owner) + 2
        d["mainPokemon"] = d["mainPokemon"][owner_len::]
        d["trainerInfo"]["trainerOwned"] = True
        d["trainerInfo"]["trainer"] = owner.lower()
        d["cameoPokemon"] = [owner.lower()]
        new_data.append(d)

for i, file_name in enumerate(metadata_files):
    with open(f"./metadata/{file_name}", "w") as file:
        json.dump(new_data[i], file, indent=2)
