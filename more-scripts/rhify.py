import os
import json

metadata_files = os.listdir("metadata")

for name in metadata_files:
    with open(f"metadata/{name}", "r") as file:
        file_data = json.load(file)

    # Edit the below
    file_data["isReverseHolo"] = True

    if not file_data["masterSetData"]["cardNumber"].endswith("-RH"):
        file_data["masterSetData"]["cardNumber"] = (
            file_data["masterSetData"]["cardNumber"] + "-RH"
        )
        try:
            file_data["tags"].remove("holofoil")
        except Exception as e:
            pass

        file_data.append("reverse-holofoil")

        # Edit the image file name
        image_name = f"images/{name[:-4]}png"
        image_new_name = f"images/{name[:-5]}-RH.png"

        os.rename(image_name, image_new_name)

    with open(f"metadata/{name[:-5]}-RH.json", "w") as file:
        json.dump(file_data, file, indent=2)

    os.remove(f"metadata/{name}")
