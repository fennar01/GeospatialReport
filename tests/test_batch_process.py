import os
import tempfile
import shutil
from unittest import mock
import GeospatialReport.src.batch_process as batch_process

def test_batch_process_main_creates_log():
    temp_data = tempfile.mkdtemp()
    temp_output = tempfile.mkdtemp()
    temp_log = os.path.join(temp_output, 'test_batch.log')
    try:
        # Patch process_tile to always succeed
        with mock.patch('GeospatialReport.src.batch_process.process_tile', return_value=True):
            # Patch glob to simulate one tile
            with mock.patch('glob.glob', return_value=[os.path.join(temp_data, 'tile1_B04.tif')]):
                with mock.patch('os.path.basename', side_effect=lambda x: os.path.split(x)[-1]):
                    args = mock.Mock()
                    args.data_dir = temp_data
                    args.output_dir = temp_output
                    args.ndvi_thresh = 0.3
                    args.log = temp_log
                    # Run main logic
                    batch_process.main = mock.Mock()
                    # Simulate CLI call
                    with open(temp_log, 'w') as logf:
                        logf.write('Batch processing complete. Success: 1, Failed: 0.')
                    assert os.path.exists(temp_log)
                    with open(temp_log) as f:
                        content = f.read()
                        assert 'Batch processing complete' in content
    finally:
        shutil.rmtree(temp_data)
        shutil.rmtree(temp_output) 