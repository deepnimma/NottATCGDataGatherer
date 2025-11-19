import re
import os


def clean_str(unclean: str) -> str:
    unclean = unclean.strip()
    unclean = unclean.split(" ")
    new_words = []

    for word in unclean:
        new_words.append(re.sub(r"[^a-zA-Z0-9\-]", "", word).lower())

    return "-".join(new_words)


def create_folders(set_name: str) -> None:
    clean_name = clean_str(set_name)

    if not os.path.isdir("sets"):
        os.mkdir("sets")
    if not os.path.isdir(f"sets/{clean_name}"):
        os.mkdir(f"sets/{clean_name}")

    _create_image_folder(clean_name)
    _create_metadata_folder(clean_name)


def _create_image_folder(set_name: str) -> None:
    print(f"Creating image folder for {set_name}")

    if not os.path.isdir(f"sets/{set_name}/images"):
        os.mkdir(f"sets/{set_name}/images")


def _create_metadata_folder(set_name: str) -> None:
    print(f"Creating metadata folder for {set_name}")

    if not os.path.isdir(f"sets/{set_name}/metadata"):
        os.mkdir(f"sets/{set_name}/metadata")
