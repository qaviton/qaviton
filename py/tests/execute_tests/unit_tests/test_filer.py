import pytest
from qaviton.utils import filer
from qaviton.utils import condition
from tests.config.file_paths import yaml1
from tests.config.file_paths import yaml2


@pytest.fixture
def parsed_yaml_file():
    yield filer.parse.yaml(yaml1)


def test_yaml1(parsed_yaml_file):
    y = parsed_yaml_file
    assert condition.all_in_all(("a", "b"), y.keys())
    assert y["a"] == 1
    assert isinstance(y["b"], dict)
    assert condition.all_in_all(("c", "d"), y["b"].keys())
    assert y["b"]["c"] == 3
    assert y["b"]["d"] == 4


def test_yaml2(parsed_yaml_file):
    y = parsed_yaml_file
    doc = """a: 1
b:
  c: 3
  d: 4
"""
    filer.dump.yaml(yaml2, y)
    with open(yaml2) as f:
        assert f.read() == doc
