# utils.py
# General utility functions for the pipeline 

def export_mask_as_geotiff(mask, profile, out_path):
    """
    Export a boolean or integer mask as a GeoTIFF using the given rasterio profile.
    """
    import rasterio
    with rasterio.open(out_path, 'w', **profile) as dst:
        dst.write(mask.astype(rasterio.uint8), 1)

def export_mask_as_geojson(mask, profile, out_path):
    """
    Export a boolean or integer mask as a GeoJSON file using rasterio.features and geopandas.
    """
    import geopandas as gpd
    from rasterio import features
    from shapely.geometry import shape
    geoms = [shape(geom) for geom, value in features.shapes(mask.astype('uint8'), mask=mask, transform=profile['transform']) if value == 1]
    if not geoms:
        print(f"No features to export for {out_path}")
        return
    gdf = gpd.GeoDataFrame({'geometry': geoms}, crs=profile['crs'])
    gdf = gdf.to_crs(epsg=4326)
    gdf.to_file(out_path, driver='GeoJSON')
    print(f"Exported GeoJSON: {out_path}") 