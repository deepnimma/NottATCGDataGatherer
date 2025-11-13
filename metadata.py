import concurrent.futures
import json
import jsonschema
import requests
import os
import re

from constants import (
    IMAGE_DOWNLOADER_WORKERS,
    ACCEPTABLE_SUPERTYPES,
    TRAINER_SUPERTYPES,
)


def _get_cleaned_set_name(card: dict) -> str:
    set_name = card.get("set").get("name")
    set_name = set_name.replace(" ", "-").lower()
    set_name = re.sub(r"[^A-Za-z0-9\- ]", "", set_name)

    return set_name


def _check_dir(set_name: str) -> None:
    if not os.path.exists(f"sets/{set_name}"):
        try:
            os.mkdir(f"sets/{set_name}")
        except FileExistsError:
            pass

    if not os.path.exists(f"sets/{set_name}/metadata"):
        try:
            os.mkdir(f"sets/{set_name}/metadata")
        except FileExistsError:
            pass

    if not os.path.exists(f"sets/{set_name}/images"):
        try:
            os.mkdir(f"sets/{set_name}/images")
        except FileExistsError:
            pass


def parse_list_of_cards(pages: list[dict]) -> bool:
    all_cards = _get_all_cards(pages)

    _check_dir(_get_cleaned_set_name(all_cards[0]))

    # We are going to have to start downloading images as well
    print(f"Starting {IMAGE_DOWNLOADER_WORKERS} worker thread pool")
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=IMAGE_DOWNLOADER_WORKERS
    ) as executor:
        executor.map(_arrange_data, all_cards)

    # # let's ignore the Thread pool while we test stuff
    # for i, card in enumerate(all_cards):
    #     if i > 1:
    #         continue

#         _arrange_data(card)

    return False


def _get_all_cards(pages: list[dict]) -> list[dict]:
    # Build page of "data" field
    all_cards = []

    for i, page in enumerate(pages):
        print(f"Appending data of page {i + 1}")
        page_data = page.get("data", [])

        all_cards.extend(page_data)

    return all_cards


def _arrange_data(card: dict) -> bool:
    tags = []
    print(f"Arranging Card: {card.get("set").get("name")}( {card.get("number")} )")

    card_supertype = card.get("supertype").lower()
    if card_supertype not in ACCEPTABLE_SUPERTYPES:
        print(f"Skipping {card.get("number")}. Supertype: {card_supertype}")
        return False

    card_title = card.get("name").lower()
    main_pokemon = card_title  # Will have to do change this manually for each Pokemon?
    version = 1

    has_reverse_holo = False  # Always False in WOTC Era
    try:
        main_energy = card.get("types")[0].lower()
    except TypeError:
        # Check if card_supertype is energy
        if card_supertype == "energy":
            main_energy = card_title.lower().split(" ")[0]
            if main_energy == "double":
                main_energy = card_title.lower().split(" ")[1]
        else:
            main_energy = "trainer"

    if main_energy == "lightning":
        main_energy = "electric"
    if main_energy == "potion":
        main_energy = "trainer"
    if main_energy == "rainbow":
        main_energy = "trainer"
    if main_energy == "full":
        main_energy = "trainer"

    try:
        secondary_energy = card.get("types")[1]
    except TypeError:
        secondary_energy = None
    except IndexError:
        secondary_energy = None

    # trainerInfo
    trainer_info_dict = {
        "item": True if card_supertype in TRAINER_SUPERTYPES else False,
        "trainerOwned": False,  # WOTC Era Always False
        "soleTrainer": False,
    }

    illustrator = card.get("artist").lower()

    # masterSetData
    set_data = card.get("set")
    set_name = set_data.get("name").lower()
    card_number = card.get("number")

    if len(card_number) == 1:
        card_number = "00" + card_number
    elif len(card_number) == 2:
        card_number = "0" + card_number


    master_set_data = {
        "setName": set_name.replace(" ", "-"),
        "cardNumber": card_number,
    }

    if main_energy == "trainer" or card_supertype == "energy":
        print(
            f"{card_number} is a {card_supertype if card_supertype == "energy" else "trainer"} card."
        )
        trainer_info_dict["trainer"] = card_title

    # release
    release_date = set_data.get("releaseDate")
    release_date_obj = release_date.split("/")
    release_year = int(release_date_obj[0])
    release_month = int(release_date_obj[1])
    release_day = int(release_date_obj[2])

    release = {
        "releaseYear": release_year,
        "releaseMonth": release_month,
        "releaseDay": release_day,
    }

    if "holo" in card.get("rarity", "").lower():
        tags.append("holofoil")
    if card_supertype == "energy":
        tags.append("energy")

    my_dict = {
        "cardTitle": card_title,
        "mainPokemon": main_pokemon,
        "version": version,
        "trainerInfo": trainer_info_dict,
        "hasReverseHolo": has_reverse_holo,
        "mainEnergy": main_energy,
        "illustrator": illustrator,
        "masterSetData": master_set_data,
        "release": release,
        "tags": tags,
    }

    if secondary_energy is not None:
        print(f"{card_number} has a secondary energy.")
        my_dict["secondaryEnergy"] = secondary_energy

    # Validate against schema
    with open("schema.json", "r") as file:
        schema = json.load(file)

    try:
        jsonschema.validate(my_dict, schema)
    except Exception as e:
        print(f"Could not validate {card_number}. Message: {e}")
        return False

    cleaned_set_name = _get_cleaned_set_name(card)
    metadata_file_loc = f"sets/{cleaned_set_name}/metadata/{card_number}.json"
    with open(metadata_file_loc, "w") as file:
        json.dump(my_dict, file, indent=4)

    # Get Image Now
    image_link = card.get("images").get("large")
    image_loc = f"sets/{cleaned_set_name}/images/{card_number}.png"

    if os.path.exists(image_loc):
        print(f"Skipping {card_number} image. Image already exists.")
        return True

    print(f"Getting {card_number} image now.")

    # Get Image
    response = requests.get(image_link)

    with open(image_loc, "wb") as file:
        file.write(response.content)

    return False
