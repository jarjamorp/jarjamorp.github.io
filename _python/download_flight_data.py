import requests
from bs4 import BeautifulSoup
import os
import re

# Set up the initial parameters for the download
base_url = "https://samples.adsbexchange.com/readsb-hist/2023/10/01/"
local_save_path = "C:/projects/website-content/flying/"  # Replace with your actual path

# Make sure the local directory exists
os.makedirs(local_save_path, exist_ok=True)

# Function to download a single file
def download_file(url, local_filename):
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded {local_filename}")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
    except Exception as e:
        print(f"Error: {e}")

# Function to list all .json.gz files on the webpage
def list_files(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return [node.get('href') for node in soup.find_all('a') if node.get('href').endswith('.json.gz')]

# Get a list of all .json.gz files
file_list = list_files(base_url)

# Download each file
for filename in file_list:
    file_url = base_url + filename
    local_filename = os.path.join(local_save_path, filename)
    download_file(file_url, local_filename)

