from PIL import Image, ImageDraw, ImageFont
import math
import os
import threading


def get_optimal_font(text, font_path, max_width, max_height):
    """
    Calculates the maximum font size that fits within the given dimensions
    using the specific font provided.
    """
    # clear_font check
    try:
        # Load a base instance to test availability
        ImageFont.truetype(font_path, 10)
    except IOError:
        print(f"ERROR: Could not find font file at: {font_path}")
        print("Please download 'Poppins-SemiBold.ttf' and place it in this folder.")
        print("Falling back to default (This will NOT scale).")
        return ImageFont.load_default()

    # Optimization: We start with a guess based on height
    # We want text height to be roughly 80% of sash height
    target_height = max_height * 0.8

    # Arbitrary starting size to measure aspect ratio
    test_size = 100
    font = ImageFont.truetype(font_path, test_size)

    # Measure
    # textbbox = (left, top, right, bottom)
    dummy_draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    bbox = dummy_draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Calculate scaling factor needed
    width_ratio = (max_width * 0.90) / text_width  # Leave 10% padding on sides
    height_ratio = target_height / text_height

    # We must satisfy the strictest constraint (smallest ratio)
    scale_factor = min(width_ratio, height_ratio)

    final_size = int(test_size * scale_factor)

    return ImageFont.truetype(font_path, final_size)


def add_sash_poppins(input_path, output_path, text="SASH TEXT"):
    # 1. Load Image
    try:
        base_image = Image.open(input_path).convert("RGBA")
    except FileNotFoundError:
        print(f"Error: Input image {input_path} not found.")
        return

    width, height = base_image.size

    # 2. Geometry (Diagonal & Angle)
    diagonal = int(math.sqrt(width ** 2 + height ** 2))
    angle = math.degrees(math.atan2(height, width))

    # 3. Create Overlay Canvas (Square)
    overlay_size = (diagonal, diagonal)
    overlay = Image.new('RGBA', overlay_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # 4. Sash Configuration
    sash_height = int(diagonal * 0.18)  # 18% of diagonal thickness
    sash_color = (44, 44, 44, 175)  # Grey
    text_color = (255, 255, 255, 255)  # White

    # !!! IMPORTANT: Ensure this filename matches your downloaded file !!!
    font_path = "Poppins-SemiBold.ttf"

    # 5. Get Scaled Font
    font = get_optimal_font(text, font_path, diagonal, sash_height)

    # 6. Draw Sash Background
    center_y = diagonal // 2
    rect_top = center_y - (sash_height // 2)
    rect_bottom = center_y + (sash_height // 2)

    draw.rectangle([(0, rect_top), (diagonal, rect_bottom)], fill=sash_color)

    # 7. Draw Text (Centered)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Accurate centering
    text_x = (diagonal - text_w) // 2
    # Adjust y by the bounding box offset to handle descenders (like 'g' or 'y')
    text_y = center_y - (text_h // 2) - bbox[1]

    draw.text((text_x, text_y), text, font=font, fill=text_color)

    # 8. Rotate
    rotated_overlay = overlay.rotate(angle, resample=Image.BICUBIC)

    # 9. Composite
    offset_x = (width - diagonal) // 2
    offset_y = (height - diagonal) // 2

    base_image.alpha_composite(rotated_overlay, dest=(offset_x, offset_y))

    # 10. Save
    base_image.convert("RGB").save(output_path)
    print(f"Saved to {output_path}")


if __name__ == "__main__":
    if not os.path.exists("./input"):
        os.mkdir("./input")
    if not os.path.exists("./images"):
        os.mkdir("./images")

    input_files = os.listdir("./input")
    file_paths = [f"input/{file}" for file in input_files]
    output_paths = [f"images/{file}" for file in input_files]

    threads = []

    for i in range(len(file_paths)):
        threads.append(
            threading.Thread(target=add_sash_poppins, args=(file_paths[i], output_paths[i], "REVERSE FOIL"))
        )

    for t in threads:
        t.start()

    for t in threads:
        t.join()