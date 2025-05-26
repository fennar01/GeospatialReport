# Sentinel-2 Plant Detection using U-Net

## Objective
A reproducible pipeline for detecting plant cover from raw Sentinel-2 satellite imagery using a machine learning model, with results visualized on an interactive map.

## Dataset
This project uses a sample Sentinel-2 tile. Download a sample from the [Copernicus Open Access Hub](https://scihub.copernicus.eu/) or [AWS Open Data Registry](https://registry.opendata.aws/sentinel-2/). See `data/README.txt` for details.

## Method
- Preprocess Sentinel-2 imagery (cloud masking, band selection, NDVI)
- Train or load a U-Net (or Random Forest) model for segmentation
- Apply the model to the image
- Visualize results on a map (Folium)

## Quickstart
```bash
git clone https://github.com/yourusername/GeospatialReport.git
cd GeospatialReport
pip install -r requirements.txt
jupyter notebook notebooks/sentinel2_pipeline.ipynb
```

## Example Output
See [`output/sample_output_map.html`](output/sample_output_map.html) for a sample interactive map. 