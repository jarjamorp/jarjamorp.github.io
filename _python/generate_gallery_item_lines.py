def generate_gallery_items(number_of_items):
    for i in range(number_of_items+1):
        line = f'<div class="gallery__item"><a href="#img{i}"><img src="b_w/{i}-tn.webp" alt="Image {i} - Black & White"></a></div>'
        print(line)

def generate_lightbox_items(number_of_items):
    for i in range(number_of_items+1):
        line = f'''    <div class="lightbox" id="img{i}">
    <a href="#" class="lightbox__close">&times;</a>
    <img src="b_w/{i}.webp" alt="Image{i} - Black & White">
  </div>'''
        print(line)
        
        
# Call the function to generate and print the lines
# generate_gallery_items(98)
generate_lightbox_items(98)