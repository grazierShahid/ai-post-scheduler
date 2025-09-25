from PIL import Image, ImageDraw, ImageFont
import os

def overlay_text_on_image(
    base_image_path: str,
    text: str,
    font_style: str = "Arial",
    font_size: int = 20,
    text_color: str = "#000000", # Hex color code
    position_x: int = 0,
    position_y: int = 0,
    output_path: str = "./temp_customized_image.jpg"
) -> str:
    """Overlays text on an image and saves the result."""
    try:
        img = Image.open(base_image_path).convert("RGBA")
    except FileNotFoundError:
        raise ValueError(f"Base image not found at {base_image_path}")
    except Exception as e:
        raise ValueError(f"Error opening base image: {e}")

    draw = ImageDraw.Draw(img)

    try:
        # Attempt to load a specific font, fallback to default if not found
        font = ImageFont.truetype(font_style + ".ttf", font_size) # Assumes .ttf extension
    except IOError:
        # Fallback to a generic font if the specified one is not found
        font = ImageFont.load_default()
        print(f"Warning: Font '{font_style}.ttf' not found. Using default font.")

    draw.text((position_x, position_y), text, font=font, fill=text_color)

    # Ensure the output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    img.save(output_path)
    return output_path
