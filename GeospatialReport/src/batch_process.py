"""
batch_process.py
Batch process all Sentinel-2 tiles in the data/ directory.
For each set of bands (B02, B03, B04, B08, QA60 if available):
- Run cloud masking (QA60 or blue band)
- Calculate NDVI
- Generate vegetation mask
- Export mask as GeoTIFF
Outputs are saved to output/ with tile-specific filenames.
"""
import os
import glob
import numpy as np
import rasterio
from src.preprocessing import calculate_ndvi, basic_cloud_mask, qa60_cloud_mask
from src.utils import export_mask_as_geotiff

def find_band(tile_prefix, band):
    # Looks for files like tileprefix_B02.tif or tileprefix_B02.jp2
    for ext in ('.tif', '.jp2'):
        path = f"data/{tile_prefix}_{band}{ext}"
        if os.path.exists(path):
            return path
    return None

def process_tile(tile_prefix):
    red_path = find_band(tile_prefix, 'B04')
    nir_path = find_band(tile_prefix, 'B08')
    blue_path = find_band(tile_prefix, 'B02')
    qa60_path = find_band(tile_prefix, 'QA60')
    if not (red_path and nir_path and blue_path):
        print(f"Missing bands for {tile_prefix}, skipping.")
        return
    with rasterio.open(red_path) as src:
        red = src.read(1).astype(float)
        profile = src.profile
    with rasterio.open(nir_path) as src:
        nir = src.read(1).astype(float)
    with rasterio.open(blue_path) as src:
        blue = src.read(1).astype(float)
    if qa60_path:
        with rasterio.open(qa60_path) as src:
            qa60 = src.read(1)
        cloud_mask = qa60_cloud_mask(qa60)
    else:
        cloud_mask = basic_cloud_mask(blue)
    ndvi = calculate_ndvi(nir, red)
    ndvi_masked = np.where(cloud_mask, ndvi, np.nan)
    veg_mask = (ndvi_masked > 0.3)
    profile_out = profile.copy()
    profile_out.update(dtype='uint8', count=1)
    out_path = f"output/{tile_prefix}_vegetation_mask.tif"
    export_mask_as_geotiff(veg_mask, profile_out, out_path)
    print(f"Processed {tile_prefix}, output: {out_path}")

def main():
    os.makedirs('output', exist_ok=True)
    # Find all unique tile prefixes in data/
    files = glob.glob('data/*_B04.*')
    prefixes = [os.path.basename(f).split('_B04')[0] for f in files]
    for prefix in prefixes:
        process_tile(prefix)

if __name__ == "__main__":
    main() 