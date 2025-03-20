from pathlib import Path

import pytest


@pytest.fixture
def package_dir(tmp_path_factory) -> Path:
    package_dir = tmp_path_factory.mktemp("package-", numbered=True)
    return package_dir


@pytest.fixture
def init_package_pyproject(package_dir):
    def pyproject_writer(toml_str) -> Path:
        pyproject_toml = package_dir / "pyproject.toml"
        with open(pyproject_toml, "w") as f:
            f.write(toml_str)
        return pyproject_toml

    return pyproject_writer
