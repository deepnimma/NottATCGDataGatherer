import json

import metadata
import set
import unicode

CURR_SET = "basep"

if __name__ == "__main__":
    data = set.get_set(CURR_SET)
    data = unicode.normalize_json_text(data)

    # Parse data
    metadata.parse_list_of_cards(data)
