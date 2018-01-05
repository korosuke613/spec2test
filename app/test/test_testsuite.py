import os
import shutil
import pytest
from spec2test import WakachiMeishi, Imporwords, Tfidf, Vector, TestSuite

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
                  units_=100,
                  learn_result_="model_iter_u100_e10_341")
    yield _


def test_instance_able(testsuite):
    assert isinstance(testsuite, TestSuite)


def test_load_vocabularies(testsuite):
    testsuite.load_vocabularies()
    assert len(testsuite.vocab_i) > 2000


def test_create_csv(testsuite):
    fff = [1, 2, 3]
    score = [0.1, 0.2, 0.3]
    testsuite.create_csv("testes", fff, score)
    assert os.path.isfile(PATH_RESOURCE + "testes.testsuite.csv")


def test_load_imporwords(testsuite):
    testsuite.load_vocabularies()
    testsuite.load_vector()
    generater = testsuite.load_imporwords()
    for filename, impolist in generater:
        impolist = [impo[0] for impo in impolist]
        testsuite_list, scores = testsuite.create_testsuite(impolist, threshold_=0.1, num_=3)
        testsuite.create_csv(filename, testsuite_list, scores)
        assert isinstance(testsuite_list, list)
        assert isinstance(scores, list)
