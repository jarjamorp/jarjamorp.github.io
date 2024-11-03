import os
from PIL import Image

def resize_images_in_folder(folder_path, max_width=2500, max_height=2500):
    # Loop through each file in the specified folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Check if the file is an image
        try:
            with Image.open(file_path) as img:
                width, height = img.size
                
                # Determine if the image needs resizing based on width or height
                if width > max_width or height > max_height:
                    # Calculate new dimensions while preserving the aspect ratio
                    if width > height:
                        # For wide images, limit width to max_width
                        new_width = min(width, max_width)
                        new_height = int((new_width / width) * height)
                    else:
                        # For tall images, limit height to max_height
                        new_height = min(height, max_height)
                        new_width = int((new_height / height) * width)
                    
                    # Resize the image
                    img_resized = img.resize((new_width, new_height), Image.LANCZOS)
                    
                    # Save the resized image, overwriting the original file
                    img_resized.save(file_path)
                    
                    print(f"Resized {filename} to {new_width}x{new_height}")
                else:
                    print(f"{filename} is already within size limits and was not resized.")
        except (IOError, FileNotFoundError) as e:
            # If the file is not an image or cannot be opened, skip it
            print(f"Skipping {filename}: {e}")

# Specify your folder path here
folder_path = r"C:\Users\harra\Downloads\panos-tall"
resize_images_in_folder(folder_path)
