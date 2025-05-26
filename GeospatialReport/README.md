An open-source pipeline for Sentinel-2 geospatial machine learning: from raw satellite imagery to model predictions and interactive maps. Supports batch and notebook workflows, multiple export formats, and both classical ML and deep learning (U-Net, coming soon).

![Project Status](https://img.shields.io/badge/status-active--development-brightgreen)

## Project Status

This project is in active development. Feedback, issues, and contributions are welcome!

# Sentinel-2 Plant Detection using U-Net

## Objective
A reproducible pipeline for detecting plant cover from raw Sentinel-2 satellite imagery using a machine learning model, with results visualized on an interactive map.

## Dataset
This project uses a sample Sentinel-2 tile. Download a sample from the [Copernicus Open Access Hub](https://scihub.copernicus.eu/) or [AWS Open Data Registry](https://registry.opendata.aws/sentinel-2/). See `data/README.txt` for details.

## Method
- Preprocess Sentinel-2 imagery (cloud masking: QA60 band if available, otherwise blue band; band selection, NDVI)
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
2. Cloud masking (QA60 band support if available, fallback to blue band)
3. NDVI calculation and visualization
4. Model training (Random Forest and U-Net options)
5. Inference on new tiles
6. Interactive map visualization (Folium/Geopandas)
7. Export results (GeoTIFF, HTML map)
8. Automated tests for core functions
9. GitHub Actions CI for notebook and code
10. Example outputs and screenshots in README

## Data Download Helper

A script is provided to help you download a sample Sentinel-2 band from AWS Open Data for demonstration purposes. Run:

```bash
python src/data_download.py
```

This will download a sample Red band (B04) as a JP2 file into the `data/` directory. You can modify the script to fetch other bands or tiles as needed.

## Batch Processing

To process all Sentinel-2 tiles in the `data/` directory, use the batch processing script:

```bash
python src/batch_process.py
```

You can customize the input/output directories, NDVI threshold, and log file:

```bash
python src/batch_process.py --data_dir my_data --output_dir my_output --ndvi_thresh 0.4 --log my_batch.log
```

This will automatically find all tiles with the required bands, run the pipeline, and export vegetation masks to the output directory with tile-specific filenames. Errors and progress are logged to the specified log file, and a summary is printed at the end.

## Export Formats

Vegetation masks are exported as GeoTIFF, GeoJSON, and Shapefile. Run the batch processing script to generate all formats for each tile. Contributions to add new export formats are welcome!

## Advanced Models: U-Net Roadmap

We plan to integrate a U-Net deep learning model for semantic segmentation of Sentinel-2 imagery. This will enable more accurate and flexible vegetation and land cover mapping. The U-Net model will be available as an alternative to the Random Forest classifier, and will be integrated into the pipeline for both notebook and batch processing workflows.

Contributions to the U-Net implementation, training scripts, and inference integration are welcome!

## How to Use U-Net (Coming Soon)

Once implemented, you will be able to:
- Train a U-Net model on your own Sentinel-2 data and masks
- Run inference with a trained U-Net model for semantic segmentation
- Use U-Net in both the notebook and batch processing workflows (as an alternative to Random Forest)

Watch this repository for updates as U-Net support is added!

## Automated Testing

Automated tests are provided for core preprocessing functions (NDVI, cloud masking). Additional tests for batch processing, export formats, and model inference are planned. All tests can be run with:

```bash
pytest
```

> **Note:** Automated CI/CD is currently disabled for this repository. Run tests locally before submitting changes.

## Example Output
See [`output/sample_output_map.html`](output/sample_output_map.html) for a sample interactive map. 
See [`output/vegetation_mask_pred.tif`](output/vegetation_mask_pred.tif) for a sample exported vegetation mask GeoTIFF.

## Example Output Gallery

Contribute your screenshots, interactive maps, and exported files here! Visual examples help others quickly understand the pipeline's results and impact. Add images to the `docs/` folder and link them here, or share links to exported GeoTIFF, GeoJSON, or Shapefile outputs.

## Model Training and Inference
The notebook demonstrates how to train a Random Forest classifier using NDVI and the blue band to predict vegetation. The model is saved and can be used for inference on new data. See the notebook section "Train Random Forest Classifier for Vegetation Detection" for details. 

## Testing and Continuous Integration
Automated tests for core functions (NDVI, cloud masking, model inference) and a GitHub Actions workflow to run tests and check notebook execution are planned. See the Pipeline Roadmap for progress. 

## How to Contribute

Contributions are welcome! To get started:
- Fork the repository and create a new branch for your feature or bugfix.
- Add or update code in the appropriate module:
  - `src/preprocessing.py`: Preprocessing functions (NDVI, cloud masking, etc.)
  - `src/train_model.py`: Model training, saving, loading, and inference
  - `src/utils.py`: Utility functions (e.g., exporting GeoTIFFs)
  - `notebooks/sentinel2_pipeline.ipynb`: Main pipeline notebook
  - `tests/`: Automated tests for core functions
- Run `pytest` to ensure all tests pass.
- If you add a new feature, please add a test for it in `tests/`.
- Open a pull request with a clear description of your changes.

> **Note:** Automated CI/CD is currently disabled. Please ensure your code passes all tests locally before submitting a pull request.

## Example Screenshots

Visual examples help users and reviewers quickly understand the results. Please add screenshots of your notebook outputs here:

![Example NDVI Map](docs/example_ndvi_map.png)

If you generate a new output, save a screenshot in the `docs/` folder and update this section. Overlays of vegetation mask on true color composites are especially helpful if you have the required bands.

## Citing This Work

If you use this pipeline in your research or projects, please cite it as:

> Fennar Ralston et al., GeospatialReport: Sentinel-2 Plant Detection Pipeline, https://github.com/fennar01/GeospatialReport

Or use the repository's citation file if available.

## License

This repository is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions, feedback, or collaboration, please open an issue on GitHub or contact Fennar Ralston via the email address listed in the repository profile.

## Changelog

- Batch processing script and CLI options added
- Export formats: GeoTIFF, GeoJSON, Shapefile now supported
- U-Net deep learning model roadmap and scaffolding added
- CI/CD (GitHub Actions) disabled; tests must be run locally
- Documentation and contribution guidelines improved 