import os
import shutil
import pytest
from spec2test import WakachiMeishi, Imporwords, Tfidf, Model

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
    wakachi = WakachiMeishi(input_path=PATH_FILE, output_path=PATH_FILE)
    tfidf = Tfidf(input_path=PATH_FILE, output_path=PATH_FILE)
    model = Model(input_path=PATH_FILE, output_path=PATH_FILE)
    _ = Imporwords(PATH_RESOURCE,
                   wakachi_=wakachi,
                   tfidf_=tfidf,
                   model_=model)
    yield _


def test_instance_able(imporwords):
    assert isinstance(imporwords, Imporwords)


def test_generate_imporwords(imporwords):
    imporwords.generate()
    assert os.path.isfile("./" + PATH_RESOURCE + "ラブクラフト.imporword.csv")
    assert os.path.isfile("./" + PATH_RESOURCE + "走れメロス.imporword.csv")
    pass
