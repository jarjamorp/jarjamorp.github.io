def generate_gallery_items(number_of_items, filename):
    for i in range(number_of_items+1):
        line = f'<div class="gallery__item"><a href="#img{i}"><img src="{filename}/{i}-tn.webp" alt="{filename.capitalize()}: {i}"></a></div>'
        print(line)

def generate_lightbox_items(number_of_items, filename):
    for i in range(number_of_items+1):
        line = f'''    <div class="lightbox" id="img{i}">
    <a href="#" class="lightbox__close">&times;</a>
    <img src="{filename}/{i}.webp" alt="{filename.capitalize()}: {i}">
  </div>'''
        print(line)
        
        
# Call the function to generate and print the lines
number_of_items = 38
filename = 'experiments'
# generate_gallery_items(number_of_items, filename)
generate_lightbox_items(number_of_items, filename)