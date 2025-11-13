import json

import metadata
import set
import unicode

CURR_SET = "swsh1"

if __name__ == "__main__":
    data = set.get_set(CURR_SET)

    if data is None:
        exit(1)

    data = unicode.normalize_json_text(data)

    # Parse data
    metadata.parse_list_of_cards(data)
