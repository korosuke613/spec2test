import os
import pytest
from spec2test import Wakachi

PATH_FILE = "test_file/"
PATH_RESOURSE = "test_resource/wakachi/"


def true_file_list():
    return [path
            for path in os.listdir("./test_file")
            if path[-len(".txt"):] == ".txt"]


@pytest.fixture()
def setup_file():
    if os.path.isfile("./" + PATH_RESOURSE + "ラブクラフト.txt.wakachi"):
        os.remove("./" + PATH_RESOURSE + "ラブクラフト.txt.wakachi")


@pytest.fixture()
def wakachi(setup_file):
    _ = Wakachi()
    _.file_path = PATH_FILE
    _.wakachi_path = PATH_RESOURSE
    yield _


def test_instance_able(wakachi):
    assert isinstance(wakachi, Wakachi)


def test_create_file_list(wakachi):
    file_list = wakachi._Wakachi__create_file_list()
    assert isinstance(file_list, list)
    assert true_file_list() == file_list


def test_generate(wakachi):
    wakachi.generate("ラブクラフト.txt")
    assert os.path.isfile("./" + PATH_RESOURSE + "ラブクラフト.txt.wakachi")