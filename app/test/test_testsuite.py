import os
import shutil
import pytest
from spec2test import WakachiMeishi, Imporwords, Tfidf, Model, TestSuite

PATH_FILE = "test_file"
PATH_RESOURCE = "test_resource/imporwords/"


@pytest.fixture()
def setup_file():
    if os.path.isdir("./" + PATH_RESOURCE):
        shutil.rmtree("./" + PATH_RESOURCE)
    if not os.path.isdir("./" + PATH_RESOURCE):
        os.mkdir("./" + PATH_RESOURCE)


@pytest.fixture()
def testsuite(setup_file):
    wakachi = WakachiMeishi(input_path=PATH_FILE, output_path=PATH_FILE)
    model = Model(input_path=PATH_FILE, output_path=PATH_FILE)
    tfidf = Tfidf(input_path=PATH_FILE, output_path=PATH_FILE)
    imporwords = Imporwords(output_path=PATH_FILE, wakachi_=wakachi, model_=model, tfidf_=tfidf)
    _ = TestSuite(PATH_RESOURCE,
                  model_=model,
                  tfidf_=tfidf,
                  imporwords_=imporwords)
    yield _


def test_instance_able(testsuite):
    assert isinstance(testsuite, TestSuite)
