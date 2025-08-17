import os

# Configuration
BASE_DIRECTORY = 'C:\\projects\\orph.in'
# BASE_DIRECTORY = 'C:\\Users\\harra\\Downloads\\website-test'
FOLDER_NAMES = [
    'slow'
]
PAGE_TITLES = [
    'Slow'
]

# BASE_DIRECTORY = 'C:\\Users\\harra\\Downloads\\website-personal'
# FOLDER_NAMES = [
#     'autumn', 'beauty', 'blue', 'clouds-wondrous-clouds', 'could-have', 
#     'covid-quarantine', 'dead-of-night', 'figuring', 'graphic-accidents', 
#     'merica', 'not-a-photo', 'patterns-amsterdam', 'patterns-london', 
#     'patterns-taipei', 'plane-crash', 'pointless-shapes', 'rust', 
#     'self-portraits', 'slow', 'slow-light', 'space-rocks', 'spring', 
#     'stream-as-sculptor', 'surf', 'trash-treasure', 'veg-soy-sauce'
# ]
# PAGE_TITLES = [
#     'Autumn', 'Beauty, Beauty Everywhere', 'Blue', 'Clouds, Wondrous Clouds', 
#     'I Could Have Done That', 'Covid Quarantine', 'Dead of Night', 'Figuring', 
#     'Graphic Accidents', 'Merica', 'Not a Photo', 'Patterns: Amsterdam', 
#     'Patterns: London', 'Patterns: Taipei', 'Plane Crash', 'Pointless Shapes', 
#     'Rust', 'Self Portraits', 'Slow', 'Slow Light', 'Space Rocks', 'Spring', 
#     'Stream As Sculptor', 'Surfing', 'Trash/Treasure', 'Vegemite & Soy Sauce'
# ]
    
def generate_image_divs(title, foldername, number_of_images):
    template = '<div class="gallery__item"><a href="#img{num}"><img src="{foldername}/{num}-tn.webp" alt="Image {num} - {title}"></a></div>'
    lines = [template.format(title=title, foldername=foldername, num=i) for i in range(0, number_of_images)]
    formatted_lines = [lines[0]] + ['\t\t\t' + line for line in lines[1:]]  # ensures correct indents
    return '\n'.join(formatted_lines[:-1]) + '\n' + formatted_lines[-1]  # new line (no lin break) for each div
  
def generate_lightbox_divs(title, foldername, number_of_images):
    template = """
  <div class="lightbox" id="img{num}">
    <a href="#" class="lightbox__close">&times;</a>
    <img src="{foldername}/{num}.webp" alt="Image {num} - {title}">
  </div>
    """
    return ''.join([template.format(title=title, foldername=foldername, num=i) for i in range(0, number_of_images)])

def generate_header(title):
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
  {header_div}
  {lightbox_divs}
</body>
</html>
    """

def count_files_in_folders(base_directory, folder_names):
    file_counts = []
    for folder_name in folder_names:
        folder_path = os.path.join(base_directory, folder_name)
        if os.path.isdir(folder_path):
            count = sum(len(files) for _, _, files in os.walk(folder_path)) // 2
        else:
            count = 0
        file_counts.append(count)
    return file_counts
        
def write_html_files():
    file_counts = count_files_in_folders(BASE_DIRECTORY, FOLDER_NAMES)
    for folder_name, title, count in zip(FOLDER_NAMES, PAGE_TITLES, file_counts):
        html_content = create_html_content(title, folder_name, count)
        file_path = os.path.join(BASE_DIRECTORY, f"{folder_name}.html")
        with open(file_path, "w") as file:
            file.write(html_content)
        print(f"{file_path} written")


if __name__ == "__main__":
    write_html_files()
