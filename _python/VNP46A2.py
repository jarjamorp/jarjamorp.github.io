import h5py
import matplotlib.pyplot as plt
import numpy as np

# Path to the HDF5 file
file_path = './VNP46A2/VNP46A2.A2012019.h00v01.001.2020038165154.h5'

    
# Function to recursively print the structure of the HDF5 file
def print_structure(name, obj):
    if isinstance(obj, h5py.Group):
        print(f"Group: {name}")
    elif isinstance(obj, h5py.Dataset):
        print(f"Dataset: {name} - Shape: {obj.shape}, Datatype: {obj.dtype}")

# Open the HDF5 file
with h5py.File(file_path, 'r') as data:
    print("HDF5 File Structure:")
    data.visititems(print_structure)

# Open the HDF5 file
with h5py.File(file_path, 'r') as data:
    # Navigate to the BRDF-corrected nighttime lights data
    # brdf_corrected_ntl_data = data['HDFEOS']['GRIDS']['VNP_Grid_DNB']['Data Fields']['DNB_BRDF-Corrected_NTL'][:]
    brdf_corrected_ntl_data = data['HDFEOS']['GRIDS']['VNP_Grid_DNB']['Data Fields']['DNB_Lunar_Irradiance'][:]
    
    # Apply the scale factor
    scale_factor = 0.1
    brdf_corrected_ntl_data = brdf_corrected_ntl_data * scale_factor
    
    # Plot the data
    plt.figure(figsize=(10, 10))
    plt.imshow(brdf_corrected_ntl_data, cmap='gray', vmin=0, vmax=10)  # Grayscale with intensity range 0-10
    plt.colorbar(label='Nighttime Light Intensity (nW·cm⁻²·sr⁻¹)')
    plt.title('Daily Lunar BRDF-Adjusted Nighttime Lights (VNP46A2)')
    plt.xlabel('Pixel Column')
    plt.ylabel('Pixel Row')
    plt.show()


# import h5py
# import matplotlib.pyplot as plt
# import numpy as np
# import gdal
# import os

# # Paths
# input_file_path = r'C:\projects\orph.in\jarjamorp.github.io\VNP46A2\VNP46A2.A2012019.h00v01.001.2020038165154.h5'  # Update this with your file path
# output_folder = r'C:\projects\orph.in\jarjamorp.github.io\VNP46A2\output'  # Folder to save the output GeoTIFF

# # Load and visualize HDF5 file
# with h5py.File(input_file_path, 'r') as data:
#     # Extract the BRDF-corrected nighttime lights data
#     brdf_corrected_ntl_data = data['HDFEOS']['GRIDS']['VNP_Grid_DNB']['Data Fields']['DNB_BRDF-Corrected_NTL'][:]
    
#     # Plot the data
#     plt.figure(figsize=(10, 10))
#     plt.imshow(brdf_corrected_ntl_data, cmap='gray', vmin=0, vmax=10)  # Adjust intensity and color scale
#     plt.colorbar(label='Nighttime Light Intensity (nW·cm⁻²·sr⁻¹)')
#     plt.title('Daily Lunar BRDF-Adjusted Nighttime Lights (VNP46A2)')
#     plt.xlabel('Pixel Column')
#     plt.ylabel('Pixel Row')
#     plt.show()

# # Convert HDF5 layer to GeoTIFF
# # Open the HDF file with GDAL
# hdflayer = gdal.Open(input_file_path, gdal.GA_ReadOnly)
# subhdflayer = hdflayer.GetSubDatasets()[0][0]  # Access the first sub-dataset
# rlayer = gdal.Open(subhdflayer, gdal.GA_ReadOnly)

# # Create output filename
# output_name = rlayer.GetMetadata_Dict().get('long_name', 'Nighttime_Lights').strip().replace(" ", "_").replace("/", "_")
# output_raster = os.path.join(output_folder, f"{output_name}_BBOX.tif")

# # Calculate bounding box coordinates
# horizontal_tile_number = int(rlayer.GetMetadata_Dict()["HorizontalTileNumber"])
# vertical_tile_number = int(rlayer.GetMetadata_Dict()["VerticalTileNumber"])

# west_bound_coord = (10 * horizontal_tile_number) - 180
# north_bound_coord = 90 - (10 * vertical_tile_number)
# east_bound_coord = west_bound_coord + 10
# south_bound_coord = north_bound_coord - 10

# # Set EPSG to WGS84 and define translation options
# epsg = "-a_srs EPSG:4326"  # WGS84
# translate_option_text = f"{epsg} -a_ullr {west_bound_coord} {north_bound_coord} {east_bound_coord} {south_bound_coord}"
# translate_options = gdal.TranslateOptions(gdal.ParseCommandLine(translate_option_text))

# # Convert to GeoTIFF
# gdal.Translate(output_raster, rlayer, options=translate_options)
# print(f"GeoTIFF saved at: {output_raster}")
