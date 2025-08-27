# 🚀 Python Foundation – Bulk File Renamer (CLI)

## 🎯 Objective
Show mastery of Python basics (files, paths, CLI arguments, testing) by building a robust **bulk file rename** utility.

## 🛠 Problem Statement
When managing datasets, photos, or exported experiment artifacts, filenames are often messy or inconsistent. This tool **standardizes names** with a predictable pattern (e.g., `image_001.jpg`, `report_2025-08-27_003.pdf`) while offering a **dry-run** mode for safe preview.

## 📦 Tech Stack
- **Language:** Python 3.10+
- **Libs:** Standard library only (`argparse`, `pathlib`, `re`, `datetime`)
- **Testing:** `pytest`

## 📂 Project Structure
python-foundation/
├─ src/python_foundation/ # source code
├─ tests/ # unit tests (pytest)
├─ requirements.txt # deps (pytest only)
├─ Makefile # quick commands (install/test/run)
└─ README.md # this file

## ⚡ How to Run

### 1) Install
```bash
pip install -r requirements.txt
```
2) See help
```python -m python_foundation --help```

3) Dry-run (no changes written)
# Example: rename only .jpg files with a slugified stem and a counter
```
python -m python_foundation \
  --root ./sample_images \
  --include-ext .jpg \
  --pattern "{stem_slug}_{num:03}{ext}" \
  --dry-run
```
4) Apply changes
```python -m python_foundation \
  --root ./sample_images \
  --include-ext .jpg \
  --pattern "photo_{date:%Y-%m-%d}_{num:04}{ext}" \
  --apply
```
5) Mixed extensions
```python -m python_foundation \
  --root ./docs \
  --include-ext .pdf .docx .txt \
  --pattern "{stem_slug}_{num:03}{ext}" \
  --apply
  ```
6) Recursive (subfolders)
```python -m python_foundation \
  --root ./dataset \
  --recursive \
  --pattern "{parent}_{stem_slug}_{num:03}{ext}" \
  --apply
  ```
🧩 Pattern Placeholders

{stem}: original filename without extension

{stem_slug}: slugified filename (lowercase, hyphens)

{ext}: original file extension (with dot)

{parent}: parent directory name

{num}: running counter (supports formatting: {num:03} → 001)

{date:%Y-%m-%d}: today’s date with strftime format codes

### 🧪 Tests

```PYTHONPATH=src/python_foundation pytest -v```

We set PYTHONPATH=src/python_foundation so that Python knows where to look for our modules.

By default, Python only searches the current folder, installed packages, and the standard library.

Our project code (utils.py, renamer.py) lives inside src/python_foundation/, not at the top level.

Inside renamer.py we import utils directly (from utils import slugify), so Python must treat src/python_foundation as the “root” of imports.

Adding PYTHONPATH=src/python_foundation tells Python:
👉 “Whenever you import something, also check in src/python_foundation/.”
This way both:
the tests can import python_foundation.renamer, and
renamer.py can import utils

🔑 Key Takeaways
Clean CLI with argparse

Safe dry-run vs apply

Predictable renaming with templated patterns

Unit tests for utility and core rename planner logic

## Authenticate and push to Github

We will use SSH authentication

First, generate an SSH Key:

```ssh-keygen -t ed25519 -C "your_other_email@example.com" -f ~/.ssh/id_ed25519_elite```


### 📜 License
MIT

