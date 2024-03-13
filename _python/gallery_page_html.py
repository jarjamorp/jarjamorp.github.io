import os 

def generate_image_divs(foldername, number_of_images):
    """Generates image container divs with images for a given range."""
    template = """
  <div><div class="brick"><img src="{foldername}/{num}-tn.webp" alt="Image {num}" onclick="openModal(this)"></div></div>
"""
    return ''.join([template.format(foldername=foldername, num=i) for i in range(number_of_images)])  # range(1, number_of_images + 1)

def create_html_content(title, foldername, number_of_images):
    """Generates the entire HTML content."""
    image_divs = generate_image_divs(foldername, number_of_images)
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400..800;1,400..800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<link rel="stylesheet" href="style-flexmasonry.css">
<script src="script.js"></script>

<title>{title}</title>
</head>
<body>
  <div class="gallery-container">
    <div class="gallery-sidebar">
      <a class="home-btn" href="index.html"><</a>
      <h1>{title}</h1>
    </div>
    <div class="gallery-content">
      <div class="grid">
        {image_divs}
      </div>
    </div>
  </div>

  <div id="imageModal" class="modal"> 
      <span class="close-btn" onclick="closeModal()">&times;</span>
      <img class="modal-content" id="modalImage">
      <div id="caption"></div>
  </div>
  
  <script>
      FlexMasonry.init('.grid');
  </script>

</body>
</html>
"""

def count_files_in_folders(base_directory, folder_names):
  file_counts = []
  for folder_name in folder_names:
    folder_path = os.path.join(base_directory, folder_name)
    if os.path.isdir(folder_path):
      count = sum([len(files) for r, d, files in os.walk(folder_path)])/2
    else:
      count = 0
    file_counts.append(int(count))
  return file_counts

def main():
  base_directory = 'C:\\projects\\website-personal'
  folder_names = ['autumn', 'beauty', 'blue','clouds-wondrous-clouds', 'could-have', 'covid-quarantine',
                  'dead-of-night', 'figuring', 'graphic-accidents','merica', 'not-a-photo', 
                  'patterns-amsterdam','patterns-london', 'patterns-taipei', 'plane-crash','pointless-shapes',
                  'rust', 'self-portraits', 'slow-light', 'space-rocks', 'spring', 'stream-as-sculptor',
                  'surf', 'trash-treasure', 'veg-soy-sauce']
  page_titles = ['Autumn', 'Beauty, Beauty Everywhere', 'Blue', 'Clouds, Wondrous Clouds', 'I Could Have Done That',
                 'Covid Quarantine', 'Dead of Night', 'Figuring', 'Graphic Accidents', 'Merica', 'Not a Photo',
                 'Patterns: Amsterdam', 'Patterns: London', 'Patterns: Taipei', 'Plane Crash', 'Pointless Shapes',
                 'Rust', 'Self Portraits', 'Slow Light', 'Space Rocks', 'Spring', 'Stream As Sculpture',
                 'Surfing = Fun', 'Trash/Treasure', 'Vegemite & Soy Sauce']
  file_counts = count_files_in_folders(base_directory, folder_names)
  
  """Main function to write the HTML content to a file."""
  for i in range(len(folder_names)):
    html_content = create_html_content(page_titles[i], folder_names[i], file_counts[i])
    with open(f"{folder_names[i]}.html", "w") as file:
      file.write(html_content)
    print(f"{folder_names[i]} written")
    
  # html_content = create_html_content(page_titles[1], folder_names[1], file_counts[1])
  # with open(f"{folder_names[1]}.html", "w") as file:
  #   file.write(html_content)
  # print(f"{folder_names[1]} written")

if __name__ == "__main__":
  main()

