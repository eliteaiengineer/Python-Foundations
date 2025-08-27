import argparse
from pathlib import Path
from renamer import plan_and_optionally_apply


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python_foundation",
        description="Bulk file renamer with dry-run support and templated patterns.",
    )
    p.add_argument(
        "--root",
        type=Path,
        required=True,
        help="Root directory containing files to rename.",
    )
    p.add_argument(
        "--include-ext",
        nargs="*",
        default=[],
        help="List of file extensions to include (e.g., .jpg .png .pdf). If omitted, include all files.",
    )
    p.add_argument(
        "--recursive",
        action="store_true",
        help="Recurse into subdirectories.",
    )
    p.add_argument(
        "--pattern",
        type=str,
        required=True,
        help=(
            "Rename pattern using placeholders: "
            "{stem} {stem_slug} {ext} {parent} {num} {date:%%Y-%%m-%%d}. "
            "Example: 'photo_{date:%%Y-%%m-%%d}_{num:03}{ext}'"
        ),
    )
    p.add_argument(
        "--start-num",
        type=int,
        default=1,
        help="Starting number for the {num} counter. Default: 1",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview proposed renames without writing changes.",
    )
    p.add_argument(
        "--apply",
        action="store_true",
        help="Actually perform the rename operations.",
    )
    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.dry_run and not args.apply:
        parser.error("Choose either --dry-run (preview) or --apply (perform changes).")

    plan = plan_and_optionally_apply(
        root=args.root,
        include_ext=args.include_ext,
        recursive=args.recursive,
        pattern=args.pattern,
        start_num=args.start_num,
        apply=args.apply,
    )

    # Friendly output
    if not plan:
        print("No matching files found.")
        return 0

    header = "APPLY" if args.apply else "DRY-RUN"
    print(f"[{header}] Proposed operations:")
    for old, new in plan:
        print(f"  {old}  ->  {new}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
