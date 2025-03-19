"""Test the dataset module."""

from pathlib import Path


def test_list_datasets():
    """List available datasets."""
    from .http_storage import list_datasets
    datasets = list_datasets()
    assert len(datasets) > 0
    expected_columns = {'name', 'description', 'download_url', 'license'}
    assert expected_columns.issubset(datasets.columns)


def test_download_dataset():
    """Download a behaverse dataset from a public OneDrive link."""
    # NOTE this commented section is ALT to get one of the available datasets
    # datasets = list_datasets()
    # download_url = datasets.query('name == "P500_9subjects/L1m"')['download_url'].item()
    # print(download_url)

    from .http_storage import download_dataset

    output = download_dataset('P500_9subjects/L1m')

    assert output.exists()
    assert output.is_dir()
    assert len(list(output.iterdir())) > 0
    assert output == (Path.home() / '.behaverse' / 'datasets' / 'P500_9subjects' / 'L1m')


def test_load_full_dataset():
    """Load all records of a dataset."""
    from .dataset import Dataset

    dataset = Dataset.open('P500_9subjects/L1m').load()

    assert dataset.name == 'P500_9subjects/L1m'
    assert len(dataset.subjects) > 0
    assert len(dataset.study_flow) > 0
    assert len(dataset.response_table) > 0


def test_load_dataset_with_condition():
    """Partially load a behaverse dataset."""
    from .dataset import Dataset

    subject_ids = ['001', '002']

    dataset = Dataset.open('P500_9subjects/L1m').where(subject_id=subject_ids).load()

    assert dataset.name == 'P500_9subjects/L1m'
    assert len(dataset.subjects) == len(subject_ids)
    assert len(dataset.study_flow.subject_id.unique()) == len(subject_ids)

    assert len(dataset.response_table['subject_id'].unique()) == len(subject_ids)
