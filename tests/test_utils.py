from python_foundation.utils import slugify

def test_slugify_basic():
    assert slugify("Hello World") == "hello-world"


def test_slugify_collapse_hyphens():
    assert slugify("a---b  c") == "a-b-c"
