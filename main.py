import json

from tcgdexsdk import TCGdex
import requests
import sys

import util

sdk = TCGdex("en")
set_id = "sv10"

# Get set_data
set_data = requests.get(f"https://api.tcgdex.net/v2/en/sets/{set_id}")

if set_data.status_code != 200:
    print(f"Error: {set_id} not found. Error Message: {set_id.text}")
    sys.exit(1)

set_data = set_data.json()

# save to file
with open(f"set_data/{set_id}.json", "w") as file:
    json.dump(set_data, file, indent=4)

cleaned_set_name = util.clean_str(set_data.get("name", "generic name"))
release_date = set_data.get("releaseDate", "1970-01-01")
total_cards = set_data.get("cardCount").get("official")

# Get Release Obj
release_date = release_date.split("-")
release_obj = {
    "releaseYear": int(release_date[0]),
    "releaseMonth": int(release_date[1]),
    "releaseDay": int(release_date[2])
}

# Create necessary folders
util.create_folders(cleaned_set_name)

# Start getting cards