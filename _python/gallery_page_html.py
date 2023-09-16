def generate_image_divs(foldername, number_of_images):
    """Generates image container divs with images for a given range."""
    template = """
  <div class="flex-item"><img src="{foldername}/{num}.webp" alt="Image {num}" onclick="openModal(this)"></div>
"""
    return ''.join([template.format(foldername=foldername, num=i) for i in range(1, number_of_images + 1)])

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
<link rel="stylesheet" href="style.css">
<script src="script.js"></script>
<title>{title}</title>
</head>
<body class="BK-bkgnd">
<div class="header">
  <div class="home-button">
    <a href="index.html">HOME</a> 
  </div>
  <h1 class="WT-H1">{title}</h1> 
</div>

<div class="flex-container">
  {image_divs}
</div>

<!-- The Modal -->
<div id="imageModal" class="modal"> 
    <span class="close" onclick="closeModal()">&times;</span>
    <img class="modal-content" id="modalImage">
    <div id="caption"></div>
</div>

</body>
</html>
"""

def main():
    """Main function to write the HTML content to a file."""
    html_content = create_html_content('Vegemite & Soy Sauce', 'veg-soy-sauce', 29)
    with open("veg-soy-sauce.html", "w") as file:
        file.write(html_content)

if __name__ == "__main__":
    main()
