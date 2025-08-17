def generate_gallery_items(number_of_items, filename, seriesname):
    for i in range(number_of_items+1):
        line = f'<div class="gallery__item"><a href="#img{i}"><img src="{filename}/{i}-tn.webp" alt="{seriesname}: {i}"></a></div>'
        print(line)

def generate_lightbox_items(number_of_items, filename, seriesname):
    for i in range(number_of_items+1):
        line = f'''  <div class="lightbox" id="img{i}">
    <a href="#" class="lightbox__close">&times;</a>
    <img src="{filename}/{i}.webp" alt="{seriesname}: {i}">
  </div>'''
        print(line)
        
        
# Call the function to generate and print the lines
number_of_items = 66
filename = 'panos'
seriesname = 'Long & Tall'
# generate_gallery_items(number_of_items-1, filename, seriesname)
generate_lightbox_items(number_of_items-1, filename, seriesname)