import pytest
from qaviton.utils.differ import asserts
from qaviton.exceptions import DiffException


def test_differ():
    asserts.elements_are_equal(1, 1, 1, 1, 1)
    asserts.elements_are_equal("1", "1")
    with pytest.raises(DiffException):
        asserts.elements_are_equal("1", "2")
