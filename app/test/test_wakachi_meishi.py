import os
import pytest
import shutil
from spec2test import WakachiMeishi

PATH_FILE = "test_file/txt/"
PATH_RESOURSE = "test_resource/wakachi/"


@pytest.fixture()
def setup_file():
    if os.path.isdir("./" + PATH_RESOURSE):
        shutil.rmtree("./" + PATH_RESOURSE)
    if not os.path.isdir("./" + PATH_RESOURSE):
        os.mkdir("./" + PATH_RESOURSE)


@pytest.fixture()
def wakachi_meishi(setup_file):
    _ = WakachiMeishi(input_path=PATH_FILE, output_path=PATH_RESOURSE)
    _.input_dir_path = PATH_FILE
    _.output_dir_path = PATH_RESOURSE
    yield _


def test_generate_all(wakachi_meishi):
    wakachi_meishi.generate_all(is_force=True)
    assert os.path.isfile("./" + PATH_RESOURSE + "あばばばば.meishi.wakachi")
    assert os.path.isfile("./" + PATH_RESOURSE + "test_ラブクラフト.meishi.wakachi")