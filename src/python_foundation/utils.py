import re


def slugify(text: str) -> str:
    """
    Convert text to a filesystem-friendly, lowercase, hyphen-separated slug.
    - Collapse whitespace to single hyphens
    - Remove characters outside [a-z0-9-._]
    - Collapse multiple hyphens
    - Strip leading/trailing hyphens
    """
    t = text.lower()
    t = re.sub(r"[^a-z0-9]+", "-", t)   # replace any non-alphanumeric run with a hyphen
    t = re.sub(r"-{2,}", "-", t)        # collapse multiple hyphens
    return t.strip("-")

