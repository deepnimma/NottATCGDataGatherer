#!/bin/bash

# -- CONFIGURATION --
LINK_VARIABLE="uploader.deepnimma.workers.dev"
# -- CONFIGURATION --

# -- READ ENV --
if [ -f "../../.env" ]; then
  source "../../.env"
else
  echo ".env file not found."
  exit 1
fi
# -- DONE ENV --

echo "Starting upload script.."

# Check if the images directory exists
if [ ! -d "images" ]; then
  echo "Error: 'images' directory was not found."
  exit 1
fi

# Check if the metadata directory exists
if [ ! -d "metadata" ]; then
  echo "Error: 'metadata' directory was not found."
  exit 1
fi

# Loop through every .png file in the 'images' directory
for image_file in images/*.png
do
  filename=$(basename "$image_file")
  number="${filename%.png}"
  metadata_file="metadata/${number}.json"

  if [ -f "$metadata_file" ]; then
    echo "-------------------------"
    echo "Processing: ${number}"
    echo "  Image:    ${image_file}"
    echo "  Metadata: ${metadata_file}"
    echo "-------------------------"

    curl -X POST \
      -F "image=@${image_file}" \
      -F "metadata=@${metadata_file}" \
      -H "Uploader-Token: ${UPLOADER_TOKEN}" \
      -H "Routing: image" \
      "${LINK_VARIABLE}"

    echo ""
  else
    echo "-------------------------"
    echo "WARNING: Skipping ${image_file}. Could not find matching file: ${metadata_file}"
    echo "-------------------------"
  fi
done

echo "-------------------------"
echo "All uploads complete."