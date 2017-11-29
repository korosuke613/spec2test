import os
import shutil
import pytest
from spec2test import Imporwords

PATH_FILE = "test_file/"
PATH_RESOURCE = "test_resource/imporwords/"


def true_file_list(extension_):
    def judgment_remove_test_file(path_, is_add_test_=False):
        """テストケースのファイルを除外するかどうかを判断する関数"""
        if is_add_test_ is True:
            return True
        else:
            return path_[:4] != "test"

    return [PATH_FILE + path
            for path in os.listdir("./test_file")
            if path[-len(extension_):] == extension_
            and judgment_remove_test_file(path)]


@pytest.fixture()
def setup_file():
    if os.path.isdir("./" + PATH_RESOURCE):
        shutil.rmtree("./" + PATH_RESOURCE)
    if not os.path.isdir("./" + PATH_RESOURCE):
        os.mkdir("./" + PATH_RESOURCE)


@pytest.fixture()
def imporwords(setup_file):
    _ = Imporwords()
    _._Imporwords__wakachi.path = PATH_FILE
    _._Imporwords__tfidf.path = PATH_FILE
    _._Imporwords__model.path = PATH_FILE
    yield _


def test_instance_able(imporwords):
    assert isinstance(imporwords, Imporwords)
