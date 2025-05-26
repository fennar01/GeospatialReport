# preprocessing.py
# Functions for Sentinel-2 data preprocessing (cloud masking, band selection, NDVI, etc.)

# Example placeholder function
def calculate_ndvi(nir, red):
    return (nir - red) / (nir + red + 1e-6) 