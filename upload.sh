#!/bin/bash

# -- CONFIGURATION --
LINK_VARIABLE="uploader.deepnimma.workers.dev"
DONE_DIR="done"
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

# Ensure required directories exist
for dir in images metadata; do
  if [ ! -d "$dir" ]; then
    echo "Error: '$dir' directory was not found."
    exit 1
  fi
done

# Ensure the "done" directory structure exists
mkdir -p "$DONE_DIR/images" "$DONE_DIR/metadata"

# Loop through every .png file in the 'images' directory
for image_file in images/*.png; do
  filename=$(basename "$image_file")
  number="${filename%.png}"
  metadata_file="metadata/${number}.json"

  if [ -f "$metadata_file" ]; then
    echo "-------------------------"
    echo "Processing: ${number}"
    echo "  Image:    ${image_file}"
    echo "  Metadata: ${metadata_file}"
    echo "-------------------------"

    # Perform upload and capture response + status
    response=$(curl -s -w "%{http_code}" -o /tmp/curl_response.txt \
      -X POST \
      -F "image=@${image_file}" \
      -F "metadata=@${metadata_file}" \
      -H "Uploader-Token: ${UPLOADER_TOKEN}" \
      -H "Routing: image" \
      "${LINK_VARIABLE}")

    echo "HTTP status: ${response}"
    echo "Response: $(cat /tmp/curl_response.txt)"
    echo ""

    # If upload succeeded (2xx response)
    if [[ "$response" =~ ^2[0-9]{2}$ ]]; then
      echo "✅ Upload successful for ${number}. Moving files to done/"
      mv "$image_file" "$DONE_DIR/images/"
      mv "$metadata_file" "$DONE_DIR/metadata/"
    else
      echo "❌ Upload failed for ${number}. Keeping files in place."
    fi

    sleep 1
  else
    echo "-------------------------"
    echo "WARNING: Skipping ${image_file}. Could not find matching file: ${metadata_file}"
    echo "-------------------------"
  fi
done

echo "-------------------------"
echo "All uploads complete."
