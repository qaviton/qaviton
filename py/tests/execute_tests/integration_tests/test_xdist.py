import pytest


# pytest.main()


import pytest
from qaviton.utils import unique_id

"""
expectation:
tests total: 40
tests passed: 35
tests ignored: 3
tests failed: 2
"""


@pytest.mark.run(order=1)
def test_xdist_set_and_get():
    pass


@pytest.mark.run(order=2)
def test_xdist_is_added():
    pass


@pytest.mark.run(order=2)
@pytest.mark.skip(reason='check skipped xdist')
def test_xdist_is_skipped():
    """skip test"""
    pass


@pytest.mark.run(order=2)
@pytest.mark.xfail(reason='check failed xdist')
@pytest.mark.flaky(reruns=5)  # this is a retry mechanism, it will not work with xfail marker
def test_xdist_failure():
    """xfail (expect to fail) test"""
    assert 0


@pytest.mark.run(order=1)
def test_xdist_failure2():
    """this test will fail and be marked as fail (unexpected)"""
    assert 0


@pytest.mark.run(order=3)
def test_xdist_is_true():
    pass


@pytest.mark.run(order=3)
def test_xdist2():
    pass


@pytest.mark.run(order=3)
def test_wrong_xdist2():
    pass


@pytest.mark.run(order=2)
def test_xdist2_wrong_order():
    pass


@pytest.mark.run(order=3)
def test_xdist2_on_skipped():
    pass


@pytest.mark.run(order=2)
def test_xdist2_on_xfail():
    """skip test"""
    pass


@pytest.mark.run(order=3)
def test_xdist2_on_fail():
    """fail test"""
    pass


@pytest.mark.run(order=3)
def test_skip_when_xdist2_on_fail():
    """skip test"""
    pass


@pytest.mark.run(order=2)
@pytest.mark.parametrize('n', range(3), ids=unique_id.id)
def test_xdist_dummy(n):
    pass


@pytest.mark.run(order=2)
@pytest.mark.xfail(reason='fail check')
@pytest.mark.parametrize('n', range(3), ids=unique_id.id)
def test_xdist_dummy2(n):
    """fail test in case n == 2"""
    if n == 2:
        pytest.fail('fail check')


@pytest.mark.run(order=3)
def test_multi_xdist3():
    pass


@pytest.mark.run(order=3)
def test_multi_xdist3_multi_pattern():
    pass


@pytest.mark.run(order=3)
def test_multi_xdist3_pattern():
    """skip test"""
    pass


@pytest.mark.run(order=3)
def test_multi_xdist3_pattern2():
    """skip test"""
    pass


@pytest.mark.run(order=3)
def test_multi_xdist3_pattern3():
    """skip test"""
    pass


@pytest.mark.run(order=4)
@pytest.mark.parametrize('x', range(3), ids=unique_id.id)
def test_xdist_with_parameters(x):
    pass


@pytest.mark.run(order=4)
@pytest.mark.parametrize('x', range(3), ids=unique_id.id)
def test_xdist_with_parameters2(x):
    pass


@pytest.mark.run(order=4)
@pytest.mark.parametrize('x', range(3), ids=unique_id.id)
def test_xdist_with_parameters3(x):
    pass


@pytest.mark.run(order=4)
@pytest.mark.parametrize('x', range(3), ids=unique_id.id)
def test_xdist_with_parameters4(x):
    """expect to skip"""
    pass


@pytest.mark.run(order=4)
@pytest.mark.parametrize('x', range(4), ids=unique_id.id)
def test_xdist_with_parameters5(x):
    """skip on case x == 0"""
    if x == 0:
        assert 0
