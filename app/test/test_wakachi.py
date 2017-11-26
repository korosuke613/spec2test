import pytest
from spec2test import Wakachi

@pytest.fixture()
def fixture_db():
    pass


def test_instanse_able():
    wakachi = Wakachi()
    assert isinstance(wakachi, Wakachi)
