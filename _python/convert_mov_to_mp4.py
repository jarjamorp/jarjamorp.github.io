import ffmpeg
import os

def convert_all_mov_to_mp4(folder_path):
    # Loop through all files in the specified folder
    for filename in os.listdir(folder_path):
        # Check if the file has a .mov extension
        if filename.lower().endswith(".mov"):
            input_path = os.path.join(folder_path, filename)
            # Create output path with .mp4 extension
            output_path = os.path.splitext(input_path)[0] + ".mp4"
            
            try:
                # Convert the .mov file to .mp4
                ffmpeg.input(input_path).output(output_path).run(overwrite_output=True)
                print(f"Converted: {filename} to {os.path.basename(output_path)}")
            except Exception as e:
                print(f"Error converting {filename}: {e}")

# Specify the path to your folder containing .mov files
folder_path = r"C:\projects\website-content\little films" # Replace with your folder path
convert_all_mov_to_mp4(folder_path)
