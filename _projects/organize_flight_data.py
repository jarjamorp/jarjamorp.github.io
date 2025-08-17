# Rewriting the script from scratch to process the .json.gz files, extract specific columns, and remove duplicates

import os
import gzip
import json
import numpy as np
import pandas as pd

# Function to process each .json.gz file and extract desired columns
def process_json_gz(file_path):
    with gzip.open(file_path, 'rt', encoding='UTF-8') as file:
        file_content = json.load(file)
        now_value = file_content['now']
        relevant_data = []
        for aircraft in file_content['aircraft']:
            if 'hex' in aircraft and aircraft.get('alt_baro') == 'ground':
                extracted_data = {
                    'hex': aircraft.get('hex'),
                    'lat': aircraft.get('lat'),
                    'lon': aircraft.get('lon'),
                    'now': now_value
                }
                relevant_data.append(extracted_data)
        return relevant_data

# Function to remove duplicates based on the 'hex' column
def remove_duplicates(data_list):
    df = pd.DataFrame(data_list)
    df_unique = df.drop_duplicates(subset='hex', keep='first')
    return df_unique

# Main function to process all files in a directory
def process_all_files(directory_path):
    all_data = []

    # Loop through each file in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.json.gz'):
            file_path = os.path.join(directory_path, filename)
            try:
                file_data = process_json_gz(file_path)
                all_data.extend(file_data)
            except Exception as e:
                print(f"Error reading {filename}: {e}")

    return all_data

# Directory path
# directory_path = "/mnt/data/"
directory_path = "C:/projects/website-content/flying/"


# Process all files and remove duplicates
processed_data = process_all_files(directory_path)
unique_data = remove_duplicates(processed_data)

# Convert the unique data to a numpy array
np_unique_data = unique_data.to_numpy()

# Save the numpy array as a CSV file
def save_array_as_csv(array_data, file_name):
    df = pd.DataFrame(array_data)
    df.to_csv(file_name, index=False, header=False)  # No header for numpy array conversion
    return f"File saved as {file_name}"

# Save the file
# file_path = "/mnt/data/unique_flight_data.csv"
file_path = "C:/projects/website-content/flying/unique_flight_data.csv"
save_message = save_array_as_csv(np_unique_data, file_path)
save_message, file_path
