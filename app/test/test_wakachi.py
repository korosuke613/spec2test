import os
import pytest
import shutil
from spec2test import Wakachi
from spec2test import File

PATH_FILE = "test_file/txt/"
PATH_RESOURSE = "test_resource/wakachi/"


@pytest.fixture()
def setup_file():
    if os.path.isdir("./" + PATH_RESOURSE):
        shutil.rmtree("./" + PATH_RESOURSE)
    if not os.path.isdir("./" + PATH_RESOURSE):
        os.mkdir("./" + PATH_RESOURSE)


@pytest.fixture()
def wakachi(setup_file):
    _ = Wakachi(input_path=PATH_FILE, output_path=PATH_RESOURSE)
    _.input_dir_path = PATH_FILE
    _.output_dir_path = PATH_RESOURSE
    yield _


def test_instance_able(wakachi):
    assert isinstance(wakachi, Wakachi)


def test_generate(wakachi):
    file = File("あばばばば.txt", ".txt")
    wakachi.generate(file)
    assert os.path.isfile("./" + PATH_RESOURSE + "あばばばば.wakachi")


def test_generate_all(wakachi):
    wakachi.generate_all(is_force=True)
    assert os.path.isfile("./" + PATH_RESOURSE + "あばばばば.wakachi")
    assert os.path.isfile("./" + PATH_RESOURSE + "test_ラブクラフト.wakachi")
