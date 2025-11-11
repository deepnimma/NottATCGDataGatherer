import json

import metadata
import set
import unicode

CURR_SET = "base2"
url = "https://api.pokemontcg.io/v2/cards?q=set.id:base1"

if __name__ == "__main__":
    data = set.get_set(CURR_SET)
    data = unicode.normalize_json_text(data)

    # Parse data
    metadata.parse_list_of_cards(data)
