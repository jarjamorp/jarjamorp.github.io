import os
from PIL import Image

def convert_to_webp(directory):
    counter = 1  # Initialize counter for prefixing filenames
    
    for filename in os.listdir(directory):
        file_root, file_extension = os.path.splitext(filename)
        filepath = os.path.join(directory, filename)

        # Check for the required extensions (both lowercase and uppercase)
        if file_extension.lower() in [".jpg", ".jpeg", ".png"]:
            with Image.open(filepath) as img:
                # Resize the image maintaining the aspect ratio with a width of 1280 pixels
                aspect_ratio = img.height / img.width
                new_height = int(480 * aspect_ratio)  # 1280
                img = img.resize((480, new_height))
                
                # Save the image in .webp format with numbered prefix
                webp_path = os.path.join(directory, f"{counter}.webp")
                img.save(webp_path, "WEBP")
                print(f"Converted {filename} to {counter}.webp")
                counter += 1  # Increment counter for the next filename

if __name__ == "__main__":
    directory_path = input("Enter the path to the directory containing image files: ")
    convert_to_webp(directory_path)
