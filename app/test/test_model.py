import os
import shutil
import pytest
from spec2test import Model

PATH_FILE = "test_file/"
PATH_RESOURSE = "test_resource/model/"


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
def model(setup_file):
    _ = Model()
    _._Model__wakachi.path = PATH_FILE
    _.path = PATH_RESOURSE
    yield _


def test_instance_able(model):
    assert isinstance(model, Model)


def test_create_file_list(model):
    file_list = model._Model__create_filepath_list()
    assert isinstance(file_list, list)
    true = true_file_list()
    assert true == file_list


def test_create_models_word_vector(model):
    model.create_models_word_vector()
    assert os.path.isfile("./" + PATH_RESOURSE + "ラブクラフト.txt.model")
    assert os.path.isfile("./" + PATH_RESOURSE + "走れメロス.txt.model")
