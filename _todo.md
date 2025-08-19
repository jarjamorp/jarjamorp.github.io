
fix index.html being generated as the page name in site/galleries/*/index.html - make it the gallery title

create a html file of the same name as title, in the current page template format 
update the image names in iPhone upload workflow so they're consistent with other galleries
    update the tools/generate_gallery.py to do this
    refactor python files so that tools are in _tools/ and other random things in _projects
    delete old unsed tool python files 
add a reference to the newly created html file and its folder and images 
fix generate_gallery_line_itmes.py -> create a python script that generates a standard gallery page 
    use this standard gallery page to generate a new page when photos uploaded from iPhone 
    update photos.yml accordingly  

LATER

build a simple frontend for creating pages, loading images (converts to webp), writing things, etc. (make it super easy to post stuff)

<!-- DONE

fix photos-staging so that it only activates an action when a new folder is added, not mods to files in this branch 
    simplifed things and now photos-staging is unused - iPhone straight to main 
    
-->