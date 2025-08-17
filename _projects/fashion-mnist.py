# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.decomposition import PCA
# from keras.datasets import fashion_mnist
# from mpl_toolkits.mplot3d import Axes3D

# # Load the Fashion-MNIST dataset
# (X_train, y_train), _ = fashion_mnist.load_data()

# # Select a subset of the data
# n_samples = 500  # Adjust the number of samples as needed
# X = X_train[:n_samples]
# y = y_train[:n_samples]

# # Flatten the images for PCA
# X_flat = X.reshape(n_samples, -1)

# # Perform PCA to reduce to 3 principal components
# pca = PCA(n_components=3)
# X_pca = pca.fit_transform(X_flat)

# # Plot the data in 3D
# fig = plt.figure(figsize=(12, 9))
# ax = fig.add_subplot(111, projection='3d')

# # Scatter plot of the PCA-transformed data
# # scatter = ax.scatter(
# #     X_pca[:, 0],
# #     X_pca[:, 1],
# #     X_pca[:, 2],
# #     c=y,
# #     cmap='tab10',
# #     s=20,
# #     alpha=0.6  # Slight transparency for better visualization
# # )

# # Optionally, plot images for a subset of data points
# for i in range(0, n_samples, 1):  # Plot every 50th image
#     x, y_pca, z = X_pca[i]
#     img = X[i]

#     # Normalize the image
#     img_norm = img / 255.0  # Shape: (28, 28)

#     # Define the size of the image in the plot
#     img_size = 30  # Adjust this to change the image size in the plot

#     # Create a grid for the image
#     xx, yy = np.meshgrid(
#         np.linspace(x - img_size, x + img_size, img.shape[1]),
#         np.linspace(y_pca - img_size, y_pca + img_size, img.shape[0])
#     )
#     zz = np.ones_like(xx) * z  # Set the z coordinate

#     # Map the grayscale image to RGBA
#     facecolors = plt.cm.gray(img_norm)

#     # Plot the image as a surface
#     ax.plot_surface(
#         xx,
#         yy,
#         zz,
#         rstride=1,
#         cstride=1,
#         facecolors=facecolors,
#         shade=False
#     )

# # Set labels and title
# ax.set_xlabel('Principal Component 1')
# ax.set_ylabel('Principal Component 2')
# ax.set_zlabel('Principal Component 3')
# plt.title('PCA of Fashion-MNIST Dataset with Images')

# # Show color legend
# # legend = ax.legend(*scatter.legend_elements(), title="Classes", loc="upper right")
# # ax.add_artist(legend)

# plt.show()



import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from keras.datasets import fashion_mnist
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Load the Fashion-MNIST dataset
(X_train, y_train), _ = fashion_mnist.load_data()

# Select a subset of the data
n_samples = 500  # Adjust the number of samples as needed
X = X_train[:n_samples]
y = y_train[:n_samples]

# Flatten the images for PCA
X_flat = X.reshape(n_samples, -1)

# Perform PCA to reduce to 3 principal components
pca = PCA(n_components=3)
X_pca = pca.fit_transform(X_flat)

# Plot the data in 3D
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

# Function to plot an image in 3D
def plot_image(ax, img, x, y, z, img_size=30):
    img_norm = img / 255.0  # Normalize the image
    img_extent = [-img_size, img_size, -img_size, img_size]
    
    # Create a 3D plane for the image
    xx, yy = np.meshgrid(np.linspace(-img_size, img_size, img.shape[1]),
                         np.linspace(-img_size, img_size, img.shape[0]))
    zz = np.zeros_like(xx)
    
    # Convert grayscale image to RGBA
    facecolors = plt.cm.gray(img_norm)
    facecolors = np.repeat(facecolors[:, :, np.newaxis], 4, axis=2)
    facecolors[:, :, 3] = 1  # Set alpha channel to 1

    # Transform the vertices to the correct 3D position
    verts = [list(zip(xx.flatten() + x, yy.flatten() + y, zz.flatten() + z))]
    img_plane = Poly3DCollection(verts, facecolors=facecolors.reshape(-1, 4), edgecolor='none')
    
    ax.add_collection3d(img_plane)

# Plot images for a subset of data points
for i in range(0, n_samples, 50):  # Adjust step to include more/fewer images
    x, y_pca, z = X_pca[i]
    img = X[i]
    plot_image(ax, img, x, y_pca, z)

# Set labels and title
ax.set_xlabel('Principal Component 1')
ax.set_ylabel('Principal Component 2')
ax.set_zlabel('Principal Component 3')
plt.title('PCA of Fashion-MNIST Dataset with Images')

plt.show()
print(X_pca)