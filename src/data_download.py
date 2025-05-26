"""
data_download.py
Download a sample Sentinel-2 band from AWS Open Data for demonstration purposes.
"""
import os
import requests

def download_band(url, out_path):
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(out_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded {out_path}")

def main():
    os.makedirs('data', exist_ok=True)
    # Example: Sentinel-2 L1C tile, 2020-06-01, 32TQM, band 04 (red)
    url = "https://sentinel-s2-l1c.s3.amazonaws.com/tiles/32/T/QM/2020/6/1/0/B04.jp2"
    out_path = "data/S2_sample_B04.jp2"
    download_band(url, out_path)

if __name__ == "__main__":
    main() 