# preprocessing.py
# Functions for Sentinel-2 data preprocessing (cloud masking, band selection, NDVI, etc.)

def calculate_ndvi(nir, red):
    """Calculate NDVI from NIR and Red bands."""
    return (nir - red) / (nir + red + 1e-6)

def basic_cloud_mask(blue_band, threshold=0.2):
    """
    Basic cloud mask using the blue band (B02).
    Pixels with blue reflectance > threshold (scaled 0-1) are masked as clouds.
    Returns a boolean mask: True = clear, False = cloud.
    """
    blue_scaled = blue_band / blue_band.max()
    return blue_scaled <= threshold

def qa60_cloud_mask(qa60_band):
    """
    Generate a cloud mask from Sentinel-2 QA60 band.
    Bits 10 or 11 set = cloud. Returns boolean mask: True = clear, False = cloud.
    """
    # Bits 10 and 11: opaque/cloud, cirrus/cloud
    cloud_bits = (1 << 10) | (1 << 11)
    return (qa60_band & cloud_bits) == 0

def cloud_mask_stub(band):
    """Stub for cloud masking. Returns a mask of all True (no clouds)."""
    import numpy as np
    return np.ones_like(band, dtype=bool) 