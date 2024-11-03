import os
from PIL import Image

def find_and_save_long_aspect_ratio_images(main_folder_path, output_folder_path):
    # Ensure the output folder exists
    os.makedirs(output_folder_path, exist_ok=True)

    # Index for naming files in the output folder
    index = 0
    
    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}

    # Walk through each subfolder and file in the main folder
    for root, _, files in os.walk(main_folder_path):
        for filename in files:
            # Check if the file has a valid image extension
            if os.path.splitext(filename)[1].lower() in valid_extensions:
                file_path = os.path.join(root, filename)  
                              
                # Check if the file is an image
                try:
                    with Image.open(file_path) as img:
                        width, height = img.size
                        
                        # Determine the longest and shortest dimensions
                        longest = max(width, height)
                        shortest = min(width, height)
                        
                        # Check the condition
                        if longest > 2.3 * shortest:
                            print(file_path, filename)
                            # Construct the new filename based on the incrementing index
                            new_filename = f"{index}{os.path.splitext(filename)[1]}"
                            new_file_path = os.path.join(output_folder_path, new_filename)
                            
                            # Save the image to the output folder
                            img.save(new_file_path)
                            print(new_file_path)
                            
                            # Increment the index for the next file
                            index += 1
                except (IOError, FileNotFoundError):
                    # If the file is not an image or cannot be opened, skip it
                    continue

# Specify your main folder path and output folder path here
# main_folder_path = r"C:\Users\harra\OneDrive\Pictures\iPhone Photos 02023-09-20"
main_folder_path = r"E:\Photos"
# output_folder_path = r"C:\projects\website-content\panos"
output_folder_path = r"C:\Users\harra\Downloads\panos"
result = find_and_save_long_aspect_ratio_images(main_folder_path, output_folder_path)
