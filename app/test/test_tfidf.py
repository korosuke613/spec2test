import os
import pytest
from spec2test import Tfidf

PATH_FILE = "test_file/"
PATH_RESOURSE = "test_resource/tfidf/"


def true_file_list():
    return [path
            for path in os.listdir("./test_resource")
            if path[-len(".wakachi"):] == ".wakachi"]


@pytest.fixture()
def tfidf():
    _ = Tfidf()
    _._Tfidf__wakachi.wakachi_path = PATH_FILE
    yield _


def test_instance_able(tfidf):
    assert isinstance(tfidf, Tfidf)


def test_create_file_list(tfidf):
    file_list = tfidf._Tfidf__create_wakachi_list()
    assert isinstance(file_list, list)
    assert true_file_list() == file_list
