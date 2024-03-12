





'''

OBESELETE - USE convert_to_webp.py

'''





from PIL import Image
import os

# Define the directory where your images are stored
image_directory = r"C:\Users\harra\Downloads\surf"
thumbnail_directory = r"C:\Users\harra\Downloads\surf"

# Make sure to create the thumbnail directory if it doesn't exist
if not os.path.exists(thumbnail_directory):
    os.makedirs(thumbnail_directory)

# Set the desired thumbnail width
thumbnail_width = 400

# Loop through all files in the directory
for index, filename in enumerate(os.listdir(image_directory)):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        try:
            # Open the image
            with Image.open(os.path.join(image_directory, filename)) as img:
                # Calculate the height to maintain aspect ratio
                aspect_ratio = img.height / img.width
                thumbnail_height = int(thumbnail_width * aspect_ratio)

                # Create the thumbnail
                img.thumbnail((thumbnail_width, thumbnail_height))

                # Build the new filename
                name, extension = os.path.splitext(filename)
                # new_filename = f"{index + 1}-tn{extension}"
                new_filename = f"{name}-tn{extension}"

                # Save the thumbnail to the new directory
                img.save(os.path.join(thumbnail_directory, new_filename))
                
                print(filename, new_filename)
        except Exception as e:
            print(f"Error processing {filename}: {e}")
print("Thumbnail creation complete.")

