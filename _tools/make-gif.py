import os
from PIL import Image
import matplotlib.pyplot as plt

def create_gif(image_folder, output_path, duration=500, loop=0, target_width=800):
    # Get all image file paths from the directory
    images = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.endswith(('png', 'jpg', 'jpeg', 'JPG', 'bmp', 'gif'))]
    
    # Sort images by name to maintain order
    images.sort()

    # Open images, resize them, and append to a list
    frames = []
    for image_path in images:
        with Image.open(image_path) as img:
            # Calculate the new height to maintain aspect ratio
            aspect_ratio = img.height / img.width
            new_height = int(target_width * aspect_ratio)
            
            # Resize the image
            img_resized = img.resize((target_width, new_height), Image.ANTIALIAS)
            
            # Append the resized image to the frames list
            frames.append(img_resized)

    # Save as GIF
    if frames:
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=loop
        )
        print(f"GIF saved at {output_path}")
    else:
        print("No images found in the directory.")

    # Save as GIF
    if frames:
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=loop
        )
        print(f"GIF saved at {output_path}")
    else:
        print("No images found in the directory.")

# Parameters
image_folder = 'C:/Users/harra/Downloads/tiles'  
output_path = 'experiments/output-4.gif'  # Output GIF file path
duration = 50  # Duration between frames in milliseconds
loop = 0  # Number of loops (0 for infinite)

create_gif(image_folder, output_path, duration, loop)