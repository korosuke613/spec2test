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
                  learn_result_="model_iter_72306")
    yield _


def test_instance_able(testsuite):
    assert isinstance(testsuite, TestSuite)


def test_load_vocabularies(testsuite):
    testsuite.load_vocabularies()
    assert len(testsuite.vocab_i) > 2000


def test_create_csv(testsuite):
    fff = [1, 2, 3]
    testsuite.create_csv("testes", fff)
    assert os.path.isfile(PATH_RESOURCE + "testes.testsuite.csv")


def test_load_imporwords(testsuite):
    testsuite.load_vocabularies()
    testsuite.load_model()
    generater = testsuite.load_imporwords()
    filename, impolist = generater.__next__()
    impolist = [impo[0] for impo in impolist]
    testsuite_list = testsuite.create_testsuite(impolist)
    testsuite.create_csv(filename, testsuite_list)


def generate(testsuite):
    for _ in range(10):
        testsuite.generate("蒲団")
