from pathlib import Path

import runtime_lab


def test_runtime_lab_package_imports() -> None:
    assert runtime_lab.__version__ == "0.1.0"


def test_expected_project_scaffold_exists() -> None:
    root = Path(__file__).resolve().parents[1]

    assert (root / "README.md").is_file()
    assert (root / "pyproject.toml").is_file()
    assert (root / "chapters" / "CHAPTER_TEMPLATE.md").is_file()
    assert (root / "src" / "runtime_lab").is_dir()
    assert (root / "tests").is_dir()
    assert (root / "scripts").is_dir()
