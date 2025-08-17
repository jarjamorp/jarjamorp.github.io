import os
from PIL import Image

def process_images(directory):
    for filename in os.listdir(directory):
        file_root, file_extension = os.path.splitext(filename)
        filepath = os.path.join(directory, filename)
        
        # Convert PNG and PNG files to jpg
        if file_extension.lower() == ".png":
            with Image.open(filepath) as img:
                img.convert('RGB').save(os.path.join(directory, file_root + ".jpg"))
                print(f"Converted {filename} to {file_root}.jpg")

        # Rename JPG to jpg
        elif file_extension == ".JPG":
            new_name = os.path.join(directory, file_root + ".jpg")
            os.rename(filepath, new_name)
            print(f"Renamed {filename} to {file_root}.jpg")

if __name__ == "__main__":
    directory_path = input("Enter the path to the directory containing image files: ")
    process_images(directory_path)
