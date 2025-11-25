import json

from tcgdexsdk import TCGdex
import requests
import sys
import os

import constants
import concurrent.futures
import util
import card

sdk = TCGdex("en")

# CHANGE THIS
set_id = "gym2"

# Get set_data
set_data = requests.get(f"https://api.tcgdex.net/v2/en/sets/{set_id}")

if set_data.status_code != 200:
    print(f"Error: {set_id} not found. Error Message: {set_id.text}")
    sys.exit(1)

set_data = set_data.json()

if not os.path.exists("set_data"):
    os.mkdir("set_data")

# save to file
with open(f"set_data/{set_id}.json", "w") as file:
    json.dump(set_data, file, indent=4)

cleaned_set_name = util.clean_str(set_data.get("name", "generic name"))
release_date = set_data.get("releaseDate", "1970-01-01")
total_cards = set_data.get("cardCount").get("official")
all_cards = set_data.get("cards")

# Get Release Obj
release_date = release_date.split("-")
release_obj = {
    "releaseYear": int(release_date[0]),
    "releaseMonth": int(release_date[1]),
    "releaseDay": int(release_date[2]),
}

# Create necessary folders
util.create_folders(cleaned_set_name)

params = [(ind_card.get("id"), release_obj) for ind_card in all_cards]
with concurrent.futures.ThreadPoolExecutor(max_workers=constants.IMAGE_DOWNLOADER_WORKERS) as executor:
    results_iterator = executor.map(lambda x: card.get_card_data(x[0], x[1]), params)
    all_results = list(results_iterator)
