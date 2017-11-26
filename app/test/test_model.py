import os
import pytest
from spec2test import Model

PATH_FILE = "test_file/"
PATH_RESOURSE = "test_resource/model/"


def true_file_list():
    return [path
            for path in os.listdir("./test_resource")
            if path[-len(".wakachi"):] == ".wakachi"]


@pytest.fixture()
def model():
    _ = Model()
    _._Model__wakachi.wakachi_path = PATH_FILE
    yield _


def test_instance_able(model):
    assert isinstance(model, Model)


def test_create_file_list(model):
    file_list = model._Model__create_filepath_list()
    assert isinstance(file_list, list)
    assert true_file_list() == file_list
