# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.cm as cm

# def mandelbrot(c, max_iter):
#     z = c
#     for n in range(max_iter):
#         if abs(z) > 2:
#             return n
#         z = z*z + c
#     return max_iter

# def generate_mandelbrot_image(xmin, xmax, ymin, ymax, width, height, max_iter, filename=None):
#     r1 = np.linspace(xmin, xmax, width)
#     r2 = np.linspace(ymin, ymax, height)
#     n3 = np.empty((width, height))
#     for i in range(width):
#         for j in range(height):
#             n3[i, j] = mandelbrot(r1[i] + 1j * r2[j], max_iter)
#     if filename:
#         plt.imshow(n3.T, cmap=cm.viridis, extent=(xmin, xmax, ymin, ymax))
#         plt.axis('off')
#         plt.savefig(filename, bbox_inches='tight', pad_inches=0)
#         plt.close()
#     return n3.T

# # Interactive click handler to capture the click coordinates
# def onclick(event):
#     global center_x, center_y, zoom_ready
#     center_x, center_y = event.xdata, event.ydata
#     print(f"Clicked at: {center_x}, {center_y}")
#     zoom_ready = True
#     plt.close()

# # Initial parameters
# xmin, xmax, ymin, ymax = -2.0, 1.0, -1.5, 1.5
# width, height = 800, 800
# max_iter = 256
# zoom_factor = 2
# iterations = 10

# for i in range(iterations):
#     # Generate and display the Mandelbrot set image
#     fig, ax = plt.subplots()
#     image_data = generate_mandelbrot_image(xmin, xmax, ymin, ymax, width, height, max_iter)
#     ax.imshow(image_data, cmap=cm.viridis, extent=(xmin, xmax, ymin, ymax))
#     ax.axis('off')
    
#     global center_x, center_y, zoom_ready
#     zoom_ready = False
#     cid = fig.canvas.mpl_connect('button_press_event', onclick)
#     plt.show()
    
#     # Wait until the user clicks on the image
#     while not zoom_ready:
#         plt.pause(0.1)
    
#     # Calculate the new bounds based on the click coordinates
#     new_width = (xmax - xmin) / zoom_factor
#     new_height = (ymax - ymin) / zoom_factor
    
#     xmin = center_x - new_width / 2
#     xmax = center_x + new_width / 2
#     ymin = center_y - new_height / 2
#     ymax = center_y + new_height / 2
    
#     print(xmin, xmax, ymin, ymax)
    
#     # Generate the zoomed image and save it
#     generate_mandelbrot_image(xmin, xmax, ymin, ymax, width, height, max_iter, f'mandelbrot_zoomed_{i+1}.png')


# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.cm as cm
# import time

# def mandelbrot(c, max_iter):
#     z = c
#     for n in range(max_iter):
#         if abs(z) > 2:
#             return n
#         z = z*z + c
#     return max_iter

# def generate_mandelbrot_image(xmin, xmax, ymin, ymax, width, height, max_iter, filename=None):
#     r1 = np.linspace(xmin, xmax, width)
#     r2 = np.linspace(ymin, ymax, height)
#     n3 = np.empty((width, height))
#     for i in range(width):
#         for j in range(height):
#             n3[i, j] = mandelbrot(r1[i] + 1j * r2[j], max_iter)
#     plt.imshow(n3.T, cmap=cm.viridis, extent=(xmin, xmax, ymin, ymax))
#     plt.axis('off')
#     if filename:
#         plt.savefig(filename, bbox_inches='tight', pad_inches=0)
#         plt.close()
#     return n3.T

# # Interactive click handler to capture the click coordinates
# def onclick(event):
#     global center_x, center_y, click_ready
#     center_x, center_y = event.xdata, event.ydata
#     print(f"Clicked at: {center_x}, {center_y}")
#     click_ready = True
#     draw_zoom_square(ax, center_x, center_y, zoom_factor)
#     plt.draw()
#     plt.pause(0.1)
#     time.sleep(5)
#     plt.close(fig)

# # Function to draw a square around the selected area
# def draw_zoom_square(ax, center_x, center_y, zoom_factor):
#     new_width = (xmax - xmin) / zoom_factor
#     new_height = (ymax - ymin) / zoom_factor
#     rect = plt.Rectangle((center_x - new_width / 2, center_y - new_height / 2),
#                          new_width, new_height, linewidth=1, edgecolor='r', facecolor='none')
#     ax.add_patch(rect)

# # Initial parameters
# xmin, xmax, ymin, ymax = -2.0, 1.0, -1.5, 1.5
# width, height = 800, 800
# max_iter = 256
# zoom_factor = 2
# iterations = 10

# for i in range(iterations):
#     # Generate and display the Mandelbrot set image
#     fig, ax = plt.subplots()
#     image_data = generate_mandelbrot_image(xmin, xmax, ymin, ymax, width, height, max_iter)
    
#     global center_x, center_y, click_ready
#     click_ready = False
#     cid_click = fig.canvas.mpl_connect('button_press_event', onclick)
#     plt.show()
    
#     # Wait until the user clicks on the image
#     while not click_ready:
#         plt.pause(0.1)
    
#     # Calculate the new bounds based on the click coordinates
#     new_width = (xmax - xmin) / zoom_factor
#     new_height = (ymax - ymin) / zoom_factor
    
#     xmin = center_x - new_width / 2
#     xmax = center_x + new_width / 2
#     ymin = center_y - new_height / 2
#     ymax = center_y + new_height / 2
    
#     # Generate the zoomed image and save it
#     generate_mandelbrot_image(xmin, xmax, ymin, ymax, width, height, max_iter, f'mandelbrot_zoomed_{i+1}.png')





import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time

def mandelbrot(c, max_iter):
    z = c
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

def generate_mandelbrot_image(xmin, xmax, ymin, ymax, width, height, max_iter, filename=None):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((width, height))
    for i in range(width):
        for j in range(height):
            n3[i, j] = mandelbrot(r1[i] + 1j * r2[j], max_iter)
    plt.imshow(n3.T, cmap=cm.viridis, extent=(xmin, xmax, ymin, ymax))
    plt.axis('off')  # Always ensure the axis is turned off when displaying the image
    if filename:  # Save the image if a filename is provided
        plt.savefig(filename, bbox_inches='tight', pad_inches=0)
        plt.close()
    return n3.T

def onclick(event):
    global center_x, center_y, click_ready
    center_x, center_y = event.xdata, event.ydata
    print(f"Clicked at: {center_x}, {center_y}")
    click_ready = True
    draw_zoom_square(ax, center_x, center_y, zoom_factor)
    plt.draw()  # Update the plot with the drawn rectangle
    plt.pause(0.1)  # Briefly pause to ensure the plot updates
    time.sleep(5)  # Wait 5 seconds to allow the user to see the rectangle
    plt.close(fig)  # Close the figure after the delay

def draw_zoom_square(ax, center_x, center_y, zoom_factor):
    new_width = (xmax - xmin) / zoom_factor
    new_height = (ymax - ymin) / zoom_factor
    rect = plt.Rectangle((center_x - new_width / 2, center_y - new_height / 2),
                         new_width, new_height, linewidth=1, edgecolor='r', facecolor='none')
    ax.add_patch(rect)

xmin, xmax, ymin, ymax = -2.0, 1.0, -1.5, 1.5
width, height = 800, 800
max_iter = 256
zoom_factor = 2
iterations = 10

for i in range(iterations):
    fig, ax = plt.subplots()  # Create a new figure and axis for each iteration
    image_data = generate_mandelbrot_image(xmin, xmax, ymin, ymax, width, height, max_iter)
    
    global center_x, center_y, click_ready
    click_ready = False
    cid_click = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()  # Show the plot and wait for user interaction
    
    while not click_ready:
        plt.pause(0.1)  # Briefly pause to allow interaction events to be processed
    
    new_width = (xmax - xmin) / zoom_factor
    new_height = (ymax - ymin) / zoom_factor
    
    xmin = center_x - new_width / 2
    xmax = center_x + new_width / 2
    ymin = center_y - new_height / 2
    ymax = center_y + new_height / 2
    
    generate_mandelbrot_image(xmin, xmax, ymin, ymax, width, height, max_iter, f'mandelbrot_zoomed_{i+1}.png')
