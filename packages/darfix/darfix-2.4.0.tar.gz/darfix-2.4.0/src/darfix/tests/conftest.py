import pytest

from . import utils


@pytest.fixture(scope="session")
def resource_files():
    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files

    return files


@pytest.fixture
def in_memory_dataset(tmpdir):
    return utils.create_3motors_dataset(
        dir=tmpdir,
        in_memory=True,
        backend="edf",
    )


@pytest.fixture
def on_disk_dataset(tmpdir):
    return utils.create_3motors_dataset(
        dir=tmpdir,
        in_memory=False,
        backend="edf",
    )
