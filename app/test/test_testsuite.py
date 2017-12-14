import os
import shutil
import pytest
from spec2test import WakachiMeishi, Imporwords, Tfidf, Model, TestSuite

PATH_FILE = "test_file/"
PATH_FILE_LEARN = PATH_FILE
PATH_RESOURCE = "test_resource/testsuite/"


@pytest.fixture()
def setup_file():
    if os.path.isdir("./" + PATH_RESOURCE):
        shutil.rmtree("./" + PATH_RESOURCE)
    if not os.path.isdir("./" + PATH_RESOURCE):
        os.mkdir("./" + PATH_RESOURCE)


@pytest.fixture()
def testsuite(setup_file):
    _ = TestSuite(input_path=PATH_FILE_LEARN,
                  output_path=PATH_RESOURCE,
                  units_=10,
                  learn_result_="./test_file/model_iter_72306")
    yield _


def test_instance_able(testsuite):
    assert isinstance(testsuite, TestSuite)


def test_load_vocabularies(testsuite):
    testsuite.load_vocabularies()
    assert len(testsuite.vocab_i) > 2000


def test_generate(testsuite):
    for _ in range(10):
        testsuite.generate("蒲団")
