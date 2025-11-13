import json

from tcgdexsdk import TCGdex
import requests

sdk = TCGdex("en")

if __name__ == "__main__":
    response = requests.get("https://api.tcgdex.net/v2/en/cards/base1-1")

    with open("data.json", "w") as file:
        json.dump(response.json(), file, indent=4)
