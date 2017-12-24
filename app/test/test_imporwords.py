import os
import shutil
import pytest
from spec2test import Directory, Imporwords

PATH_FILE = "test_file/"
PATH_TXT = PATH_FILE + "txt/"
PATH_WAKACHI = PATH_FILE + "wakachi/"
PATH_MODEL = PATH_FILE + "model/"
PATH_TFIDF = PATH_FILE + "tfidf/"
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
    wakachi = Directory(path_=PATH_WAKACHI, default_extension_=".meishi.wakachi", is_import_=True)
    tfidf = Directory(path_=PATH_TFIDF, default_extension_=".tfidf", is_import_=True)
    model = Directory(path_=PATH_MODEL, default_extension_=".model", is_import_=True)
    _ = Imporwords(PATH_RESOURCE,
                   wakachi_=wakachi,
                   tfidf_=tfidf,
                   model_=model)
    yield _


def test_instance_able(imporwords):
    assert isinstance(imporwords, Imporwords)


def test_generate_imporwords(imporwords):
    imporwords.generate()
    assert os.path.isfile("./" + PATH_RESOURCE + "あばばばば.imporword.csv")
    assert os.path.isfile("./" + PATH_RESOURCE + "トロッコ.imporword.csv")