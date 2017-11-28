import os
import pytest
import shutil
from spec2test import Wakachi

PATH_FILE = "test_file/"
PATH_RESOURSE = "test_resource/wakachi/"


def true_file_list(is_add_test=False):
    def judgment_remove_test_file(path_, is_add_test_=False):
        """テストケースのファイルを除外するかどうかを判断する関数"""
        if is_add_test_ is True:
            return True
        else:
            return path_[:4] != "test"

    return [path
            for path in os.listdir("./test_file")
            if path[-len(".txt"):] == ".txt"
            and judgment_remove_test_file(path, is_add_test_=is_add_test)]


@pytest.fixture()
def setup_file():
    if os.path.isdir("./" + PATH_RESOURSE):
        shutil.rmtree("./" + PATH_RESOURSE)
    if not os.path.isdir("./" + PATH_RESOURSE):
        os.mkdir("./" + PATH_RESOURSE)


@pytest.fixture()
def wakachi(setup_file):
    _ = Wakachi()
    _.resource_path = PATH_FILE
    _.path = PATH_RESOURSE
    yield _


def test_instance_able(wakachi):
    assert isinstance(wakachi, Wakachi)


def test_create_file_list(wakachi):
    file_list = wakachi._Wakachi__create_file_list()
    assert isinstance(file_list, list)
    assert true_file_list() == file_list


def test_create_file_list_with_test(wakachi):
    file_list = wakachi._Wakachi__create_file_list(is_add_test=True)
    assert isinstance(file_list, list)
    assert true_file_list(is_add_test=True) == file_list


def test_generate(wakachi):
    wakachi.generate("ラブクラフト.txt")
    assert os.path.isfile("./" + PATH_RESOURSE + "ラブクラフト.txt.wakachi")


def test_generate_all(wakachi):
    wakachi.generate_all(is_simple_=False, is_force=True)
    assert os.path.isfile("./" + PATH_RESOURSE + "ラブクラフト.txt.wakachi")
    assert os.path.isfile("./" + PATH_RESOURSE + "test_ラブクラフト.txt.wakachi")


def test_generate_all_is_simple(wakachi):
    wakachi.generate_all(is_simple_=True, is_force=True)
    assert os.path.isfile("./" + PATH_RESOURSE + "ラブクラフト.txt.meishi.wakachi")
    assert os.path.isfile("./" + PATH_RESOURSE + "test_ラブクラフト.txt.meishi.wakachi")
