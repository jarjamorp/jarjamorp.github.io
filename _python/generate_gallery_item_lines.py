def generate_gallery_items(number_of_items):
    for i in range(number_of_items+1):
        line = f'<div class="gallery__item" id="pop-dynamics"><a href="#img{i}"><img src="pop_dynamics/{i}-tn.gif" alt="Image {i} - The Structure of Demographic Evolutions"></a></div>'
        print(line)

def generate_lightbox_items(number_of_items):
    for i in range(number_of_items+1):
        line = f'''  <div class="lightbox" id="img{i}">
    <a href="#" class="lightbox__close">&times;</a>
    <img src="pop_dynamics/{i}.gif" alt="Image {i} - The Structure of Demographic Evolutions">
  </div>'''
        print(line)
        
# Call the function to generate and print the lines
# generate_gallery_items(226)
generate_lightbox_items(226)