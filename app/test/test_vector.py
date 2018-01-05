import os
import shutil
import pytest
from spec2test import Vector

PATH_FILE = "test_file/wakachi/"
PATH_RESOURSE = "test_resource/vector/"


def true_file_list():
    def judgment_remove_test_file(path_, is_add_test_=False):
        """テストケースのファイルを除外するかどうかを判断する関数"""
        if is_add_test_ is True:
            return True
        else:
            return path_[:4] != "test"

    return ["./" + PATH_FILE + path
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
    _ = Vector(PATH_FILE, PATH_RESOURSE)
    yield _


def test_instance_able(model):
    assert isinstance(model, Vector)


def test_create_models_word_vector(model):
    model.generate()
    assert os.path.isfile("./" + PATH_RESOURSE + "あばばばば.vector")
    assert os.path.isfile("./" + PATH_RESOURSE + "トロッコ.vector")
