"""
Instead of changing code, you can run tests like this from root:
PYTHONPATH=src/python_foundation pytest -v
This makes src/python_foundation the top-level, so imports like from utils import slugify work.
"""
from pathlib import Path
from python_foundation.renamer import FileInfo, make_target_name


def test_make_target_name_num_and_ext(tmp_path):
    p = tmp_path / "My File.JPG"
    p.write_text("x")

    fi = FileInfo(p)
    # Fixed date for deterministic test
    from datetime import datetime
    dt = datetime(2025, 8, 27)

    name = make_target_name(fi, "{stem_slug}_{num:03}{ext}", 5, dt)
    assert name == "my-file_005.JPG"


def test_make_target_name_with_parent_and_date(tmp_path):
    sub = tmp_path / "Photos"
    sub.mkdir()
    file = sub / "Summer 2025.png"
    file.write_text("x")

    fi = FileInfo(file)
    from datetime import datetime
    dt = datetime(2025, 8, 27)

    name = make_target_name(fi, "{parent}_{stem_slug}_{date:%Y%m%d}{ext}", 1, dt)
    assert name == "Photos_summer-2025_20250827.png"
