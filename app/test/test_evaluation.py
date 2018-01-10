import pytest
from spec2test import Directory, EvaluationTestsuite

PATH_CORRECT = "test_file/testsuite/correct/"
PATH_RESOURCE_A = "test_file/testsuite/eval_a/"
PATH_RESOURCE_B = "test_file/testsuite/eval_b/"


@pytest.fixture()
def eval_testsuite():
    correct = Directory(path_=PATH_CORRECT)
    eval_a = Directory(path_=PATH_RESOURCE_A)
    eval_b = Directory(path_=PATH_RESOURCE_B)
    _ = EvaluationTestsuite(eval_a, eval_b, correct)
    yield _


def test_default_extension(eval_testsuite: EvaluationTestsuite):
    assert eval_testsuite.eval_a.default_extension == ".testsuite.csv"
    assert eval_testsuite.eval_b.default_extension == ".testsuite.csv"


def test_same_files_list(eval_testsuite: EvaluationTestsuite):
    eval_dict = eval_testsuite.same_file_generator()
    file_name, eval_a, eval_b = eval_dict.__next__()
    assert file_name == "あばばばば"
    assert eval_a == "test_file/testsuite/eval_a/あばばばば.testsuite.csv"
    assert eval_b == "test_file/testsuite/eval_b/あばばばば.testsuite.csv"


def test_uniq_word_lists(eval_testsuite: EvaluationTestsuite):
    generator = eval_testsuite.unique_word_lists_generator()
    correct, eval_a, eval_b = generator.__next__()
    assert isinstance(correct, set)
    assert isinstance(eval_a, set)
    assert isinstance(eval_b, set)
