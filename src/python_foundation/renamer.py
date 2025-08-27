from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Tuple

from utils import slugify


@dataclass
class FileInfo:
    path: Path

    @property
    def stem(self) -> str:
        return self.path.stem

    @property
    def ext(self) -> str:
        return self.path.suffix

    @property
    def parent_name(self) -> str:
        return self.path.parent.name


def iter_files(root: Path, include_ext: Iterable[str], recursive: bool) -> Iterable[Path]:
    if not root.exists() or not root.is_dir():
        return []

    include_set = {e.lower() for e in include_ext} if include_ext else None

    if recursive:
        iterator = root.rglob("*")
    else:
        iterator = root.glob("*")

    for p in iterator:
        if p.is_file():
            if include_set is None or p.suffix.lower() in include_set:
                yield p


def make_target_name(
    file: FileInfo,
    pattern: str,
    index: int,
    base_date: datetime,
) -> str:
    """
    Supported placeholders:
      - {stem}, {stem_slug}, {ext}, {parent}, {num}, {date:...}
    """
    # First, handle {date:...}
    # We look for occurrences like {date:%Y-%m-%d}
    def date_replacer(match):
        fmt = match.group(1) or "%Y-%m-%d"
        return base_date.strftime(fmt)

    import re

    date_pattern = re.compile(r"{date:(.*?)}")
    out = date_pattern.sub(lambda m: date_replacer(m), pattern)

    # Replace the simple placeholders
    out = out.replace("{stem}", file.stem)
    out = out.replace("{stem_slug}", slugify(file.stem))
    out = out.replace("{ext}", file.ext)
    out = out.replace("{parent}", file.parent_name)

    # Replace {num} with optional format {num:03}, etc.
    # Find {num(:format)?}
    def num_replacer(match):
        fmt = match.group(1)
        if fmt:
            return f"{index:{fmt}}"
        return str(index)

    num_pattern = re.compile(r"{num(?::([^}]+))?}")
    out = num_pattern.sub(lambda m: num_replacer(m), out)

    return out


def plan_and_optionally_apply(
    root: Path,
    include_ext: Iterable[str],
    recursive: bool,
    pattern: str,
    start_num: int,
    apply: bool,
) -> List[Tuple[Path, Path]]:
    base_date = datetime.now()
    files = sorted(iter_files(root, include_ext, recursive))
    plan: List[Tuple[Path, Path]] = []

    idx = start_num
    for p in files:
        fi = FileInfo(p)
        new_name = make_target_name(fi, pattern, idx, base_date)
        new_path = p.with_name(new_name)

        # Avoid collisions: if new_path exists and differs by case or content, bump the counter.
        while new_path.exists() and new_path.resolve() != p.resolve():
            idx += 1
            new_name = make_target_name(fi, pattern, idx, base_date)
            new_path = p.with_name(new_name)

        plan.append((p, new_path))
        idx += 1

    if apply:
        for old, new in plan:
            if old != new:
                old.rename(new)

    return plan
