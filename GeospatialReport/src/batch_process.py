"""
batch_process.py
Batch process all Sentinel-2 tiles in the data/ directory.
For each set of bands (B02, B03, B04, B08, QA60 if available):
- Run cloud masking (QA60 or blue band)
- Calculate NDVI
- Generate vegetation mask
- Export mask as GeoTIFF, GeoJSON, and Shapefile
Outputs are saved to output/ with tile-specific filenames.
Logs errors to batch_process.log.
"""
import os
import glob
import numpy as np
import rasterio
from src.preprocessing import calculate_ndvi, basic_cloud_mask, qa60_cloud_mask
from src.utils import export_mask_as_geotiff, export_mask_as_geojson, export_mask_as_shapefile

def find_band(tile_prefix, band):
    # Looks for files like tileprefix_B02.tif or tileprefix_B02.jp2
    for ext in ('.tif', '.jp2'):
        path = f"data/{tile_prefix}_{band}{ext}"
        if os.path.exists(path):
            return path
    return None

def process_tile(tile_prefix, logf):
    try:
        red_path = find_band(tile_prefix, 'B04')
        nir_path = find_band(tile_prefix, 'B08')
        blue_path = find_band(tile_prefix, 'B02')
        qa60_path = find_band(tile_prefix, 'QA60')
        if not (red_path and nir_path and blue_path):
            msg = f"Missing bands for {tile_prefix}, skipping."
            print(msg)
            logf.write(msg + '\n')
            return False
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
        geojson_path = f"output/{tile_prefix}_vegetation_mask.geojson"
        shp_path = f"output/{tile_prefix}_vegetation_mask.shp"
        export_mask_as_geotiff(veg_mask, profile_out, out_path)
        export_mask_as_geojson(veg_mask, profile_out, geojson_path)
        export_mask_as_shapefile(veg_mask, profile_out, shp_path)
        msg = f"Processed {tile_prefix}, outputs: {out_path}, {geojson_path}, {shp_path}"
        print(msg)
        logf.write(msg + '\n')
        return True
    except Exception as e:
        msg = f"Error processing {tile_prefix}: {e}"
        print(msg)
        logf.write(msg + '\n')
        return False

def main():
    os.makedirs('output', exist_ok=True)
    log_path = 'batch_process.log'
    processed = 0
    failed = 0
    with open(log_path, 'w') as logf:
        files = glob.glob('data/*_B04.*')
        prefixes = [os.path.basename(f).split('_B04')[0] for f in files]
        for i, prefix in enumerate(prefixes, 1):
            print(f"[{i}/{len(prefixes)}] Processing {prefix}...")
            ok = process_tile(prefix, logf)
            if ok:
                processed += 1
            else:
                failed += 1
        summary = f"\nBatch processing complete. Success: {processed}, Failed: {failed}. Log: {log_path}"
        print(summary)
        logf.write(summary + '\n')

if __name__ == "__main__":
    main() 