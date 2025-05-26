import numpy as np
from src.preprocessing import calculate_ndvi, basic_cloud_mask

def test_calculate_ndvi():
    nir = np.array([[0.8, 0.6], [0.4, 0.2]])
    red = np.array([[0.2, 0.2], [0.2, 0.2]])
    ndvi = calculate_ndvi(nir, red)
    expected = (nir - red) / (nir + red + 1e-6)
    assert np.allclose(ndvi, expected)

def test_basic_cloud_mask():
    blue = np.array([[0.1, 0.3], [0.2, 0.05]])
    mask = basic_cloud_mask(blue, threshold=0.2)
    expected = np.array([[True, False], [True, True]])
    assert np.array_equal(mask, expected) 