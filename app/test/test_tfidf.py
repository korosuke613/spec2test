import os
import shutil
import pytest
from spec2test import Tfidf

PATH_FILE = "test_file/"
PATH_RESOURSE = "test_resource/tfidf/"


def true_file_list():
    def judgment_remove_test_file(path_, is_add_test_=False):
        """テストケースのファイルを除外するかどうかを判断する関数"""
        if is_add_test_ is True:
            return True
        else:
            return path_[:4] != "test"

    return [PATH_FILE + path
            for path in os.listdir("./test_file")
            if path[-len(".meishi.wakachi"):] == ".meishi.wakachi"
            and judgment_remove_test_file(path)]


@pytest.fixture()
def setup_file():
    if os.path.isdir("./" + PATH_RESOURSE):
        shutil.rmtree("./" + PATH_RESOURSE)
    if not os.path.isdir("./" + PATH_RESOURSE):
        os.mkdir("./" + PATH_RESOURSE)


@pytest.fixture()
def tfidf(setup_file):
    _ = Tfidf()
    _._Tfidf__wakachi.path = PATH_FILE
    _.path = PATH_RESOURSE
    yield _


def test_instance_able(tfidf):
    assert isinstance(tfidf, Tfidf)


def test_create_file_list(tfidf):
    file_list = tfidf._Tfidf__create_wakachi_list()
    assert isinstance(file_list, list)
    assert true_file_list() == file_list


def test_generate_tfidf(tfidf):
    tfidf.generate_tfidf()
    assert os.path.isfile("./" + PATH_RESOURSE + "ラブクラフト.txt.tfidf")
    assert os.path.isfile("./" + PATH_RESOURSE + "走れメロス.txt.tfidf")
