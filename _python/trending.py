import os
from openai import OpenAI
import logging
import requests
import subprocess
import re
from datetime import datetime
from PIL import Image
import io
from pytrends.request import TrendReq
from PIL import Image, ImageDraw, ImageFont

# Configure logging
logging.basicConfig(filename='script.log', level=logging.INFO)

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define absolute paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
TRENDING_PATH = os.path.join(REPO_PATH, 'trending')
INDEX_HTML_PATH = os.path.join(REPO_PATH, 'trending.html')


def get_top_trending_search_term():
    pytrends = TrendReq()
    trending_searches_df = pytrends.trending_searches(pn='united_states')
    top_search_term = trending_searches_df.iloc[0][0]
    print("Search term: ", top_search_term)
    return top_search_term

def generate_image(prompt, filename):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response.data[0].url

    # Generate a timestamp
    timestamp = datetime.now().strftime("0%Y%m%d_%H%M%S")
    
    # Prepare filenames
    filename_parts = os.path.splitext(filename)
    large_filename = f"{filename_parts[0]}_{timestamp}.webp"
    thumb_filename = f"{filename_parts[0]}_{timestamp}-tn.webp"
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Download the image
    img_data = requests.get(image_url).content
    img = Image.open(io.BytesIO(img_data))

    # Save large image
    large_path = os.path.join(TRENDING_PATH, large_filename)
    img.save(large_path, 'WEBP', quality=95)

    # Create and save thumbnail
    thumb = img.copy()
    thumb.thumbnail((150, 150))
    # thumb_path = os.path.join(os.path.dirname(filename), thumb_filename)
    thumb_path = os.path.join(TRENDING_PATH, thumb_filename)
    thumb.save(thumb_path, 'WEBP', quality=95)
    
    print("image generated", large_filename)

    return large_filename, thumb_filename, 

def update_index_html(large_filename, thumb_filename, index_html_path, prompt, search_term):
    with open(INDEX_HTML_PATH, 'r') as file:
        content = file.read()

    # Extract the image name without extension and without the path
    image_name = os.path.splitext(os.path.basename(large_filename))[0]

    # Create new gallery item
    new_gallery_item = f'        <div class="gallery__item"><a href="#{image_name}"><img src="trending/{os.path.basename(thumb_filename)}" alt="{prompt}"></a></div>\n'

    # Create new lightbox div
    new_lightbox_div = f'''
  
   <div class="lightbox" id="{image_name}">
    <a href="#" class="lightbox__close">&times;</a>
    <img src="trending/{os.path.basename(large_filename)}" alt="{prompt}">
    <div class="lightbox__text">"{search_term}" on {datetime.now().strftime("%A %d %B %Y")}</div>
  </div>'''

    # Insert new gallery item at the beginning of the gallery__grid
    gallery_start = content.index('<div class="gallery__grid">')
    insert_position = content.index('\n', gallery_start) + 1
    content = content[:insert_position] + new_gallery_item + content[insert_position:]

    # Insert new lightbox div after the closing header tag
    header_end = content.index('</header>') + len('</header>')
    content = content[:header_end] + new_lightbox_div + content[header_end:]

    # Write the updated content back to the file
    with open(INDEX_HTML_PATH, 'w') as file:
        file.write(content)

    print(f"Updated {INDEX_HTML_PATH}")

def is_content_allowed(text):
    response = client.moderations.create(input=text)
    output = response["results"][0]
    return not output["flagged"]

def git_commit_and_push(repo_path, commit_message):
    try:
        # Add changes
        subprocess.run(["git", "-C", repo_path, "add", "."], check=True)
        
        # Commit changes
        commit_result = subprocess.run(["git", "-C", repo_path, "commit", "-m", commit_message], 
                                       capture_output=True, text=True, check=True)
        logging.info(f"Git commit output: {commit_result.stdout}")
        
        # Push changes
        push_result = subprocess.run(["git", "-C", repo_path, "push"], 
                                     capture_output=True, text=True, check=True)
        logging.info(f"Git push output: {push_result.stdout}")
        
    except subprocess.CalledProcessError as e:
        logging.error(f"Git operation failed: {e}")
        logging.error(f"Command output: {e.output}")
        if e.stderr:
            logging.error(f"Error output: {e.stderr}")

def main():
    search_term = get_top_trending_search_term()
    
    prompt = f"Generate an image of {search_term}"
    image_filename = "img.png"
    index_html_path = "trending.html"
       
    # Generate the image and get the timestamped filenames
    large_filename, thumb_filename = generate_image(prompt, os.path.join(TRENDING_PATH, image_filename))
    # large_filename = "img_020240923_195518.webp"
    # thumb_filename = "img_020240923_195518-tn.webp"

    # Update the HTML file with both images
    update_index_html(large_filename, thumb_filename, index_html_path, prompt, search_term)
    git_commit_and_push(REPO_PATH,f"{os.path.basename(large_filename)} generated")

if __name__ == "__main__":
    main()
