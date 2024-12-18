import os
from PIL import Image

# Constants
THUMBNAIL_WIDTH = 1500  # 150 
THUMBNAIL_HEIGHT = 750  # 150 
SET_WIDTH = True  # Set to False to use height instead
BASE_DIRECTORY = r"C:\Users\harra\Downloads"
# BASE_DIRECTORY = r"C:\projects\website-content"
# BASE_DIRECTORY = 'C:\\Users\\harra\\Downloads\\test'
FOLDER_NAMES = [
    'panos-long'
]
# FOLDER_NAMES = [
#     'autumn', 'beauty', 'blue', 'clouds-wondrous-clouds', 'could-have', 
#     'covid-quarantine', 'dead-of-night', 'figuring', 'graphic-accidents', 
#     'merica', 'not-a-photo', 'patterns-amsterdam', 'patterns-london', 
#     'patterns-taipei', 'plane-crash', 'pointless-shapes', 'rust', 
#     'self-portraits', 'slow-light', 'space-rocks', 'spring', 
#     'stream-as-sculptor', 'surf', 'trash-treasure', 'veg-soy-sauce'
# ]

def convert_to_webp(directory):
    counter = 0  # Initialize counter for prefixing filenames
    lst = os.listdir(directory)
    # lst.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))  # Sort ascending
    
    # Check if the directory has any .webp files
    has_webp_files = any(filename.lower().endswith(".webp") for filename in lst)

    if has_webp_files:
        # Remove files that do not contain "-tn"
        lst = [filename for filename in lst if "-tn" in filename]
        for filename in lst:
            try:
                file_root, file_extension = os.path.splitext(filename)
                filepath = os.path.join(directory, filename)

                # Check for the required extensions (both lowercase and uppercase)
                if file_extension.lower() == ".webp":
                    with Image.open(filepath) as img:
                        # Resize the image maintaining the aspect ratio
                        if SET_WIDTH:
                            aspect_ratio = img.height / img.width
                            new_height = int(THUMBNAIL_WIDTH * aspect_ratio)
                            thumbnail_img = img.resize((THUMBNAIL_WIDTH, new_height))
                        else:
                            aspect_ratio = img.width / img.height
                            new_width = int(THUMBNAIL_HEIGHT * aspect_ratio)
                            thumbnail_img = img.resize((new_width, THUMBNAIL_HEIGHT))
                        
                        print("filepath", filepath)
                        
                        # Save the thumbnail in .webp format with numbered prefix
                        thumbnail_webp_path = os.path.join(directory, f"{counter}-tn.webp")
                        thumbnail_img.save(thumbnail_webp_path, "WEBP")
                        print(f"Created thumbnail {thumbnail_webp_path[-10:]}")
                        counter += 1  # Increment counter for the next filename
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    else:
        for filename in lst:
            try:
                file_root, file_extension = os.path.splitext(filename)
                filepath = os.path.join(directory, filename)

                # Check for the required extensions (both lowercase and uppercase)
                if file_extension in [".jpg", ".jpeg", ".JPG", ".PNG", ".png"]:
                    with Image.open(filepath) as img:
                        # Resize the image maintaining the aspect ratio
                        if SET_WIDTH:
                            aspect_ratio = img.height / img.width
                            new_height = int(THUMBNAIL_WIDTH * aspect_ratio)
                            thumbnail_img = img.resize((THUMBNAIL_WIDTH, new_height))
                        else:
                            aspect_ratio = img.width / img.height
                            new_width = int(THUMBNAIL_HEIGHT * aspect_ratio)
                            thumbnail_img = img.resize((new_width, THUMBNAIL_HEIGHT))
                        
                        print("filepath", filepath)
                        
                        # Save the image and thumbnail in .webp format with numbered prefix     
                        large_webp_path = os.path.join(directory, f"{counter}.webp")
                        thumbnail_webp_path = os.path.join(directory, f"{counter}-tn.webp")
                        img.save(large_webp_path, "WEBP")
                        thumbnail_img.save(thumbnail_webp_path, "WEBP")
                        print(f"Converted {large_webp_path[-10:]} and {thumbnail_webp_path[-10:]}")
                        counter += 1  # Increment counter for the next filename
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    for folder_name in FOLDER_NAMES:
        directory_path = os.path.join(BASE_DIRECTORY, folder_name)
        print(f"Processing directory: {directory_path}")
        convert_to_webp(directory_path)
