import os
import shutil
import pytest
from spec2test import Imporwords

PATH_FILE = "test_file/"
PATH_RESOURCE = "test_resource/imporwords/"
EXTENSION_WAKACHI = ".meishi.wakachi"
EXTENSION_TFIDF = ".tfidf"
EXTENSION_MODEL = ".model"


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
    _ = Imporwords(PATH_RESOURCE,
                   work_dir_path__="./",
                   txt_dir_path=PATH_FILE,
                   wakachi_dir_path=PATH_FILE,
                   tfidf_dir_path=PATH_FILE,
                   model_dir_path=PATH_FILE)
    yield _


def test_instance_able(imporwords):
    assert isinstance(imporwords, Imporwords)


def test_create_file_list_wakachi(imporwords):
    file_list = imporwords._Imporwords__create_filepath_list(PATH_FILE, EXTENSION_WAKACHI)
    assert isinstance(file_list, list)
    assert file_list == true_file_list(EXTENSION_WAKACHI)


def test_create_file_list_tfidf(imporwords):
    file_list = imporwords._Imporwords__create_filepath_list(PATH_FILE, EXTENSION_TFIDF)
    assert isinstance(file_list, list)
    assert file_list == true_file_list(EXTENSION_TFIDF)


def test_create_file_list_model(imporwords):
    file_list = imporwords._Imporwords__create_filepath_list(PATH_FILE, EXTENSION_MODEL)
    assert isinstance(file_list, list)
    assert file_list == true_file_list(EXTENSION_MODEL)


def test_generate_imporwords(imporwords):
    imporwords.generate_imporwords()
    assert os.path.isfile("./" + PATH_RESOURCE + "ラブクラフト.txt.imporword.csv")
    assert os.path.isfile("./" + PATH_RESOURCE + "走れメロス.txt.imporword.csv")
    pass
