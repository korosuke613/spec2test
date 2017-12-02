import os
from spec2test import Directory


def test_import_files():
    directory = Directory("./", ".py")
    directory.import_files()
    path = directory.get_file_path("test_directory.py")
    assert os.path.isfile(path)
