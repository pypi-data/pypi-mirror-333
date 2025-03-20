import pytest
from pathlib import Path
from lxd_io.dataset import Dataset

@pytest.fixture
def wrong_dataset_dir():
    return Path("test/data/dummy_dataset")

def test_dataset_initialization(wrong_dataset_dir):
    dataset = Dataset(wrong_dataset_dir)
    assert dataset.id is not None
    assert dataset.version is not None

def test_dataset_invalid_directory():
    with pytest.raises(FileNotFoundError):
        Dataset(Path("/path/to/invalid/dataset"))

def test_dataset_read_dataset_info_from_folder_name(wrong_dataset_dir):
    dataset = Dataset(wrong_dataset_dir)
    assert dataset.id == "dummy"
    assert dataset.version == "1.0"

def test_dataset_load_background_image_scale_factor(wrong_dataset_dir):
    dataset = Dataset(wrong_dataset_dir)
    assert dataset._background_image_scale_factor == 1.0

def test_dataset_explore_data_dir(wrong_dataset_dir):
    dataset = Dataset(wrong_dataset_dir)
    assert len(dataset.recording_ids) > 0
    assert len(dataset.location_ids) > 0

def test_dataset_explore_maps_dir(wrong_dataset_dir):
    dataset = Dataset(wrong_dataset_dir)
    assert len(dataset._lanelet2_map_files_per_location) > 0
    assert len(dataset._opendrive_map_files_per_location) > 0

def test_dataset_get_recording(wrong_dataset_dir):
    dataset = Dataset(wrong_dataset_dir)
    recording_id = dataset.recording_ids[0]
    recording = dataset.get_recording(recording_id)
    assert recording is not None

def test_dataset_get_track_batches(wrong_dataset_dir):
    dataset = Dataset(wrong_dataset_dir)
    track_batches = dataset.get_track_batches(10)
    assert len(track_batches) > 0
