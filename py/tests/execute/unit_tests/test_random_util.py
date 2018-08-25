import pytest
from qaviton.utils.random_util import random_number, random_string
from qaviton.utils import unique_id
from qaviton.utils import condition


@pytest.mark.parametrize('n', [0] * 100, ids=unique_id.id)
def test_random_utils(n):
    n = random_number(1, 100)
    assert 0 < n < 101
    s = "   goGOgoRangers   "
    r = random_string(s, n)
    assert condition.any_in_any(s, r)
