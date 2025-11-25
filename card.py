import requests
import os
import unicode
import util
import json

def get_card_data(card_id: str, release_obj: dict):
    print(card_id)

    # Get Card Data
    card_data = requests.get(f"https://api.tcgdex.net/v2/en/cards/{card_id}")

    if card_data.status_code != 200:
        print(f"An error occured while getting card data: {card_data.status_code}. Error: {card_data.text}. Card ID: {card_id}")

    card_data = card_data.json()

    card_data = unicode.normalize_json_text(card_data)

    with open("temp_card_data.json", "w") as file:
        json.dump(card_data, file, indent = 4)

    # Create tags list early
    tags = []

    # Get detailed variants list
    detailed_variants = card_data.get("variants_detailed", [])

    card_title = card_data.get("name").lower()
    main_pokemon = util.clean_str(card_title)
    version = 1

    # Trainer Info
    _card_category = card_data.get("category").lower()
    if _card_category == "energy":
        tags.append("energy")
    _pkmn_flag = _card_category == "pokemon"
    trainer_info = {
        "item": not _pkmn_flag,
        "trainerOwned": False,
        "soleTrainer": False
    }

    if not _pkmn_flag:
        trainer_info["trainer"] = card_title

    has_reverse_holo = _has_reverse_holo(card_data.get("variants_detailed"))
    energy_list = card_data.get("types", ["DOUBLE_CHECK_THIS"])
    main_energy = renamed_types.get(energy_list[0].lower(), energy_list[0].lower())
    if not _pkmn_flag:
        main_energy = "trainer"
    illustrator = card_data.get("illustrator", "unknown").lower()
    _secondary_energy = None

    if len(energy_list) > 1:
        _secondary_energy = energy_list[1].lower()
        _secondary_energy = renamed_types.get(_secondary_energy, _secondary_energy)

    # MasterSetData
    set_name = card_data.get("set").get("name")
    set_name = util.clean_str(set_name)
    card_num = card_data.get("localId")

    if len(card_num) == 1:
        card_num = "00" + card_num
    elif len(card_num) == 2:
        card_num = "0" + card_num

    if set_name == "base-set":
        set_name = "base"

    master_set_data = {
        "setName": set_name,
        "cardNumber": card_num
    }

    # release data
    release = release_obj

    # tags
    if _is_holofoil(detailed_variants):
        tags.append("holofoil")
    tags.extend(get_all_stamps(detailed_variants))

    # Build Object
    card_obj = {
        "cardTitle": card_title,
        "mainPokemon": main_pokemon,
        "version": 1,
        "trainerInfo": trainer_info,
        "hasReverseHolo": has_reverse_holo,
        "mainEnergy": main_energy,
        "illustrator": illustrator,
        "masterSetData": master_set_data,
        "release": release_obj,
        "tags": tags,
    }

    if _secondary_energy is not None:
        card_obj["secondaryEnergy"] = _secondary_energy

    with open(f"sets/{set_name}/metadata/{card_num}.json", "w") as file:
        json.dump(card_obj, file, indent = 2)

    # Get Image
    image_loc = f"sets/{set_name}/images/{card_num}.png"

    if os.path.exists(image_loc):
        return None

    image_link = card_data.get("image") + "/high.png"
    image = requests.get(image_link)

    with open(image_loc, "wb") as file:
        file.write(image.content)

    return None

renamed_types = {
    "colorless": "normal",
    "lightning": "electric",
    "darkness": "dark",
}

def _get_image(image_link: str, card_num: int) -> None:
    return None

def get_all_stamps(variants_detailed: dict) -> list[str]:
    stamps = []
    for variant in variants_detailed:
        for stamp in variant.get("stamp", []):
            stamps.append(stamp)

    return stamps

def _has_reverse_holo(variants_detailed: dict) -> bool:
    return __check_variants_detailed(variants_detailed, "reverse")

def _is_holofoil(variants_detailed: dict) -> bool:
    return __check_variants_detailed(variants_detailed, "holo")

# doing loop just because I like it better (I didn't notice the variant field until after I implemented this)
def __check_variants_detailed(variants_detailed: dict, card_property: str) -> bool:
    cleaned_card_property = util.clean_str(card_property)
    for variant in variants_detailed:
        if util.clean_str(variant.get("type")) == cleaned_card_property:
            return True
    return False