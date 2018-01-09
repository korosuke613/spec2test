import pytest
from spec2test import Directory, EvaluationTestsuite

PATH_RESOURCE_A = "test_file/testsuite/eval_a/"
PATH_RESOURCE_B = "test_file/testsuite/eval_b/"


@pytest.fixture()
def eval_testsuite():
    eval_a = Directory(path_=PATH_RESOURCE_A)
    eval_b = Directory(path_=PATH_RESOURCE_B)
    _ = EvaluationTestsuite(eval_a, eval_b)
    yield _


def test_default_extension(eval_testsuite: EvaluationTestsuite):
    assert eval_testsuite.eval_a.default_extension == ".testsuite"
    assert eval_testsuite.eval_b.default_extension == ".testsuite"
