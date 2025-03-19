from functools import partial
from pathlib import Path
from typing import Callable
from mlflow_ibmcos.model_registry import COSModelRegistry
import pytest
import os
from pytest_mock import MockerFixture

FIXTURES_PATH = Path(__file__).parent / "fixtures"


@pytest.fixture
def bucket_name():
    return os.getenv("COS_BUCKET_NAME")


@pytest.fixture
def mock_hash(mocker: MockerFixture):
    """
    Creates a test fixture that mocks the COSModelRegistry.write_hash method.

    This fixture allows tests to capture the generated fingerprint hash during model registration
    by copying it to a specified temporary path. This is useful for verifying that fingerprinting
    is correctly performed in tests without having to recalculate hashes.

    Args:
        mocker (MockerFixture): The pytest-mock fixture that provides patching functionality.

    Returns:
        callable: A wrapper function that accepts a tmp_path parameter and returns the mock patch.
            The returned function signature is:
                wrapper(tmp_path: Path) -> MagicMock
    """
    original_write_hash = COSModelRegistry.write_hash

    def mocked_write_hash(directory: str, tmp_path: Path):
        original_write_hash(directory)
        with open(os.path.join(directory, "fingerprint")) as f:
            hash_ = f.read()
        with open(os.path.join(tmp_path, "fingerprint"), "w") as f:
            f.write(hash_)
        return

    def wrapper(tmp_path: Path):
        return mocker.patch.object(
            target=COSModelRegistry,
            attribute="write_hash",
            new=partial(mocked_write_hash, tmp_path=tmp_path),
        )

    return wrapper


def test_model_registration_process(
    bucket_name: str, mock_hash: Callable, tmp_path: Path
):
    """
    Test the end-to-end model registration process using COSModelRegistry.

    This test verifies the full workflow of:
    1. Logging a PyFunc model with code and artifacts to the registry
    2. Verifying the model fingerprint
    3. Downloading the model artifacts
    4. Checking the structure of downloaded artifacts
    5. Loading the model
    6. Making predictions with the loaded model

    Parameters
    ----------
    bucket_name : str
        Name of the COS bucket to use for the model registry.
        You can set this up using the environment variable COS_BUCKET_NAME.
    mock_hash : Callable
        Mock function for generating fingerprints
    tmp_path : Path
        Temporary path provided by pytest fixture for artifact storage

    Notes
    -----
    This test requires fixture files: modelcode.py and model.pkl
    """
    mock_hash(tmp_path)

    registry = COSModelRegistry(
        bucket=bucket_name,
        model_name="test",
        model_version="latest",
    )
    registry.log_pyfunc_model_as_code(
        model_code_path=FIXTURES_PATH / "modelcode.py",
        artifacts={"model": FIXTURES_PATH / "model.pkl"},
    )
    registry.artifact_uri
    remote_fingerprint = registry._get_remote_fingerprint()
    assert tmp_path.joinpath("fingerprint").read_text() == remote_fingerprint

    # Now download the model
    path = registry.download_artifacts(dst_path=tmp_path)
    model_files = set(Path(path).glob("**/*"))
    expected_files = {
        tmp_path.joinpath("test/latest/modelcode.py"),
        tmp_path.joinpath("test/latest/python_env.yaml"),
        tmp_path.joinpath("test/latest/conda.yaml"),
        tmp_path.joinpath("test/latest/requirements.txt"),
        tmp_path.joinpath("test/latest/artifacts/model.pkl"),
        tmp_path.joinpath("test/latest/MLmodel"),
        tmp_path.joinpath("test/latest/fingerprint"),
        tmp_path.joinpath("test/latest/artifacts"),
    }
    assert model_files == expected_files

    model = registry.load_model(model_local_path=path)

    prediction = model.predict(
        [
            {"text": "Hello"},
            {"text": "World"},
        ]
    )
    assert prediction == ["5", "5"]
