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

## Pipeline Roadmap
This repository is public and aims to provide a full, reproducible geospatial ML pipeline. Planned and in-progress features:

1. Data download helper script (fetch Sentinel-2 samples)
2. Cloud masking (basic and advanced options)
3. NDVI calculation and visualization
4. Model training (Random Forest and U-Net options)
5. Inference on new tiles
6. Interactive map visualization (Folium/Geopandas)
7. Export results (GeoTIFF, HTML map)
8. Automated tests for core functions
9. GitHub Actions CI for notebook and code
10. Example outputs and screenshots in README

## Example Output
See [`output/sample_output_map.html`](output/sample_output_map.html) for a sample interactive map. 
See [`output/vegetation_mask_pred.tif`](output/vegetation_mask_pred.tif) for a sample exported vegetation mask GeoTIFF.

## Model Training and Inference
The notebook demonstrates how to train a Random Forest classifier using NDVI and the blue band to predict vegetation. The model is saved and can be used for inference on new data. See the notebook section "Train Random Forest Classifier for Vegetation Detection" for details. 

## Testing and Continuous Integration
Automated tests for core functions (NDVI, cloud masking, model inference) and a GitHub Actions workflow to run tests and check notebook execution are planned. See the Pipeline Roadmap for progress. 