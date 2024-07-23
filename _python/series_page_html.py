import os 

def generate_image_divs(title, foldername, number_of_images):
    """Generates image container divs with images for a given range."""
    template = """
      <div class="gallery__item"><a href="#img{num}"><img src="{foldername}/{num}-tn.webp" alt="Image {num} - {title}"></a></div>
    """
    return ''.join([template.format(title=title, foldername=foldername, num=i) for i in range(number_of_images)])  # range(1, number_of_images + 1)

def generate_lightbox_divs(title, foldername, number_of_images):
    """Generates lightbox container divs with images for a given range."""
    template = """
    <div class="lightbox" id="img{num}">
      <a href="#" class="lightbox__close">&times;</a>
      <img src="{foldername}/{num}.webp" alt="Image {num} - {title}">
    </div>
    """
    return ''.join([template.format(title=title, foldername=foldername, num=i) for i in range(number_of_images)])

def generate_header(title):
    """Generates the header section."""
    return f"""
    <header class="header header--series">
      <nav class="nav nav--series">
        <h2><a href="index.html" class="nav__link--series"> <strong>&lt;</strong></a></h2>
      </nav>
      <div>
        <h1>{title}</h1>
      <div>
    </header>
    """

def create_html_content(title, foldername, number_of_images):
    """Generates the entire HTML content."""
    gallery_divs = generate_image_divs(title, foldername, number_of_images)
    lightbox_divs = generate_lightbox_divs(title, foldername, number_of_images)
    header_div = generate_header(title)
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="style.css">

<title>{title}</title>
</head>
<body>

  <section class="gallery">
    <div class="gallery__grid">
      {gallery_divs}
    </div>
  </section>

  {lightbox_divs}

  {header_div}

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
  # base_directory = 'C:\\Users\\harra\\Downloads\\website-test'
  # folder_names = ['autumn', 'dead-of-night']
  # page_titles = ['Autumn', 'Dead of Night']
  file_counts = count_files_in_folders(base_directory, folder_names)
  
  """Main function to write the HTML content to a file."""
  for i in range(len(folder_names)):
    html_content = create_html_content(page_titles[i], folder_names[i], file_counts[i])
    with open(f"{folder_names[i]}.html", "w") as file:
      file.write(html_content)
    print(f"{folder_names[i]} written")
    
if __name__ == "__main__":
  main()

