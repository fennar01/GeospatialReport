import numpy as np
from src.preprocessing import calculate_ndvi, basic_cloud_mask, qa60_cloud_mask

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

def test_qa60_cloud_mask():
    # Bits 10 and 11: 0b0000000000000000 (clear), 0b0000010000000000 (bit 10 set), 0b0000100000000000 (bit 11 set)
    qa60 = np.array([[0, 1024], [2048, 3072]], dtype=np.uint16)
    mask = qa60_cloud_mask(qa60)
    expected = np.array([[True, False], [False, False]])
    assert np.array_equal(mask, expected) 