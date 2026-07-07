from pathlib import Path
from zipfile import ZipFile

from tools.create_project_package import create_package


def test_create_project_package_writes_to_project_packages_and_overwrites(tmp_path):
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools" / "x.py").write_text("print('x')", encoding="utf-8")
    (tmp_path / "output").mkdir()
    (tmp_path / "output" / "large.txt").write_text("skip", encoding="utf-8")
    (tmp_path / "rapportzip").mkdir()
    (tmp_path / "rapportzip" / "old.zip").write_text("skip", encoding="utf-8")
    (tmp_path / "archive").mkdir()
    (tmp_path / "archive" / "old.md").write_text("skip", encoding="utf-8")

    first = create_package(tmp_path)
    second = create_package(tmp_path)

    assert first == tmp_path / "project_packages" / "Project_For_ChatGPT.zip"
    assert second == first
    assert first.exists()

    with ZipFile(first) as zf:
        names = set(zf.namelist())

    assert "tools/x.py" in names
    assert "output/large.txt" not in names
    assert "rapportzip/old.zip" not in names
    assert "archive/old.md" not in names
    assert "PROJECT_PACKAGE_MANIFEST.txt" in names


def test_create_project_package_keeps_manifest_outside_zip(tmp_path):
    (tmp_path / "README.md").write_text("hello", encoding="utf-8")
    create_package(tmp_path)

    assert (tmp_path / "project_packages" / "PROJECT_PACKAGE_MANIFEST.txt").exists()
    assert (tmp_path / "project_packages" / "PROJECT_INFO_FOR_CHATGPT.txt").exists()
