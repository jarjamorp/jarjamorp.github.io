from PIL import Image
import os

def convert_image_to_webp(input_path, output_path=None):
    # Set default output path if not provided
    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + ".webp"

    try:
        # Open the image
        with Image.open(input_path) as img:
            # Convert and save as WebP
            img.save(output_path, "WEBP")
            print(f"Image converted and saved to {output_path}")
    except (IOError, FileNotFoundError) as e:
        print(f"Error converting image: {e}")

# Specify the path to your image
input_image_path = r"C:\projects\orph.in\jarjamorp.github.io\blue\32-tn.jpg"  # Replace with your image path
convert_image_to_webp(input_image_path)
