import pytest
from spec2test import File


def test_raise_true():
    File("test_file.py", ".py")


def test_raise_false():
    with pytest.raises(ValueError):
        File("test_file.py", ".pyc")
