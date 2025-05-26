# utils.py
# General utility functions for the pipeline 

def export_mask_as_geotiff(mask, profile, out_path):
    """
    Export a boolean or integer mask as a GeoTIFF using the given rasterio profile.
    """
    import rasterio
    with rasterio.open(out_path, 'w', **profile) as dst:
        dst.write(mask.astype(rasterio.uint8), 1) 