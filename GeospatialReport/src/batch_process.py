"""
batch_process.py
Batch process all Sentinel-2 tiles in the data/ directory (or user-specified directory).
For each set of bands (B02, B03, B04, B08, QA60 if available):
- Run cloud masking (QA60 or blue band)
- Calculate NDVI
- Generate vegetation mask (threshold configurable)
- Export mask as GeoTIFF, GeoJSON, and Shapefile
Outputs are saved to output/ (or user-specified directory) with tile-specific filenames.
Logs errors to batch_process.log (or user-specified log file).
"""
import os
import glob
import numpy as np
import rasterio
import argparse
from src.preprocessing import calculate_ndvi, basic_cloud_mask, qa60_cloud_mask
from src.utils import export_mask_as_geotiff, export_mask_as_geojson, export_mask_as_shapefile

def find_band(tile_prefix, band, data_dir):
    for ext in ('.tif', '.jp2'):
        path = os.path.join(data_dir, f"{tile_prefix}_{band}{ext}")
        if os.path.exists(path):
            return path
    return None

def process_tile(tile_prefix, data_dir, output_dir, ndvi_thresh, logf):
    try:
        red_path = find_band(tile_prefix, 'B04', data_dir)
        nir_path = find_band(tile_prefix, 'B08', data_dir)
        blue_path = find_band(tile_prefix, 'B02', data_dir)
        qa60_path = find_band(tile_prefix, 'QA60', data_dir)
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
        veg_mask = (ndvi_masked > ndvi_thresh)
        profile_out = profile.copy()
        profile_out.update(dtype='uint8', count=1)
        out_path = os.path.join(output_dir, f"{tile_prefix}_vegetation_mask.tif")
        geojson_path = os.path.join(output_dir, f"{tile_prefix}_vegetation_mask.geojson")
        shp_path = os.path.join(output_dir, f"{tile_prefix}_vegetation_mask.shp")
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
    parser = argparse.ArgumentParser(description="Batch process Sentinel-2 tiles for vegetation detection.")
    parser.add_argument('--data_dir', default='data', help='Input data directory (default: data)')
    parser.add_argument('--output_dir', default='output', help='Output directory (default: output)')
    parser.add_argument('--ndvi_thresh', type=float, default=0.3, help='NDVI threshold for vegetation (default: 0.3)')
    parser.add_argument('--log', default='batch_process.log', help='Log file (default: batch_process.log)')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    processed = 0
    failed = 0
    with open(args.log, 'w') as logf:
        files = glob.glob(os.path.join(args.data_dir, '*_B04.*'))
        prefixes = [os.path.basename(f).split('_B04')[0] for f in files]
        for i, prefix in enumerate(prefixes, 1):
            print(f"[{i}/{len(prefixes)}] Processing {prefix}...")
            ok = process_tile(prefix, args.data_dir, args.output_dir, args.ndvi_thresh, logf)
            if ok:
                processed += 1
            else:
                failed += 1
        summary = f"\nBatch processing complete. Success: {processed}, Failed: {failed}. Log: {args.log}"
        print(summary)
        logf.write(summary + '\n')

if __name__ == "__main__":
    main() 