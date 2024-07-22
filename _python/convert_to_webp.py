
import os
from PIL import Image

def convert_to_webp(directory):
    counter = 0  # Initialize counter for prefixing filenames
    lst = os.listdir(directory)
    lst.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))  # Sort ascending
    
    # Check if the directory has any .webp files
    has_webp_files = any(filename.lower().endswith(".webp") for filename in lst)

    if has_webp_files:
        # Remove files that do not contain "-tn"
        lst = [filename for filename in lst if "-tn" in filename]
        for filename in lst:
            file_root, file_extension = os.path.splitext(filename)
            filepath = os.path.join(directory, filename)

            # Check for the required extensions (both lowercase and uppercase)
            if file_extension.lower() == ".webp":
                with Image.open(filepath) as img:
                    # Resize the image maintaining the aspect ratio
                    aspect_ratio = img.height / img.width
                    new_height = int(150 * aspect_ratio)
                    thumbnail_img = img.resize((150, new_height))
                    
                    print("filepath", filepath)
                    
                    # Save the thumbnail in .webp format with numbered prefix
                    thumbnail_webp_path = os.path.join(directory, f"{counter}-tn.webp")
                    thumbnail_img.save(thumbnail_webp_path, "WEBP")
                    print(f"Created thumbnail {thumbnail_webp_path}")
                    counter += 1  # Increment counter for the next filename
    else:
        for filename in lst:
            file_root, file_extension = os.path.splitext(filename)
            filepath = os.path.join(directory, filename)

            # Check for the required extensions (both lowercase and uppercase)
            if file_extension.lower() in [".jpg", ".jpeg", ".png"]:
                with Image.open(filepath) as img:
                    # Resize the image maintaining the aspect ratio
                    aspect_ratio = img.height / img.width
                    new_height = int(150 * aspect_ratio)
                    thumbnail_img = img.resize((150, new_height))
                    
                    print("filepath", filepath)
                    
                    # Save the image and thumbnail in .webp format with numbered prefix
                    large_webp_path = os.path.join(directory, f"{counter}.webp")
                    thumbnail_webp_path = os.path.join(directory, f"{counter}-tn.webp")
                    img.save(large_webp_path, "WEBP")
                    thumbnail_img.save(thumbnail_webp_path, "WEBP")
                    print(f"Converted {large_webp_path} and {thumbnail_webp_path}")
                    counter += 1  # Increment counter for the next filename

if __name__ == "__main__":
    directory_path = input("Enter the path to the directory containing image files: ")
    convert_to_webp(directory_path)
