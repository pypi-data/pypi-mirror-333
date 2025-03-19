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
