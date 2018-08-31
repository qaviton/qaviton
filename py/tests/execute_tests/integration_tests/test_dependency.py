import pytest
from qaviton.utils import unique_id
from qaviton.fixtures.dependency import DependencyException
from qaviton.utils.helpers import funcname


"""
expectation:
tests passed: 26
tests ignored: 12
tests failed: 2
"""


@pytest.mark.run(order=1)
def test_dependency_set_and_get(dependency):
    assert dependency.get() in dependency.dependencies.get_all()
    assert dependency.get() == 'test_dependency_set_and_get'

    assert dependency.set('label-red').get() == 'label-red'
    assert dependency.get() == 'label-red'
    assert dependency.get() in dependency.dependencies.get_all()
    assert 'test_dependency_set_and_get' not in dependency.dependencies.get_all()


@pytest.mark.run(order=2)
def test_dependency_is_added(dependency, dependencies):
    dependency.depend.on('label-red')
    assert dependencies.get(funcname()) == dependencies.running


@pytest.mark.run(order=2)
@pytest.mark.skip(reason='check skipped dependency')
def test_dependency_is_skipped(dependency):
    """skip test"""
    pass


@pytest.mark.run(order=2)
@pytest.mark.xfail(reason='check failed dependency')
@pytest.mark.flaky(reruns=5)  # this is a retry mechanism, it will not work with xfail marker
def test_dependency_failure(dependency):
    """xfail (expect to fail) test"""
    assert 0


@pytest.mark.run(order=1)
def test_dependency_failure2(dependency):
    """this test will fail and be marked as fail (unexpected)"""
    assert 0


@pytest.mark.run(order=3)
def test_dependency_is_true(dependency):
    assert dependency.dependencies.get('test_dependency_is_added') == dependency.dependencies.passed


@pytest.mark.run(order=3)
def test_depend(depend):
    depend.on('test_dependency_is_added')


@pytest.mark.run(order=3)
def test_wrong_depend(depend):
    with pytest.raises(DependencyException):
        depend.on('wrong_depend')


@pytest.mark.run(order=2)
def test_depend_wrong_order(depend):
    with pytest.raises(DependencyException):
        depend.on('test_dependency_is_true')


@pytest.mark.run(order=3)
def test_depend_on_skipped(depend):
    with pytest.raises(DependencyException):
        depend.on('test_dependency_is_skipped')


@pytest.mark.run(order=2)
def test_depend_on_xfail(depend):
    """skip test"""
    depend.on('test_dependency_failure')


@pytest.mark.run(order=3)
def test_depend_on_fail(depend):
    """fail test"""
    depend.fail_when_dependency_fails().on('test_dependency_failure2')


@pytest.mark.run(order=3)
def test_skip_when_depend_on_fail(depend):
    """skip test"""
    depend.on('test_dependency_failure2')

@pytest.mark.run(order=2)
@pytest.mark.parametrize('n', range(3), ids=unique_id.id)
def test_dependency_dummy(dependency, n):
    pass


@pytest.mark.run(order=2)
@pytest.mark.xfail(reason='fail check')
@pytest.mark.parametrize('n', range(3), ids=unique_id.id)
def test_dependency_dummy2(dependency, n):
    """fail test in case n == 2"""
    if n == 2:
        pytest.fail('fail check')


@pytest.mark.run(order=3)
def test_multi_dep(depend):
    depend.on(*['test_dependency_dummy[{}]'.format(n) for n in range(3)])


@pytest.mark.run(order=3)
def test_multi_dep_multi_pattern(depend):
    depend.on_parameterized('test_dependency_dummy')


@pytest.mark.run(order=3)
def test_multi_dep_pattern(depend):
    """skip test"""
    depend.on_pattern('test_dependency_dummy')


@pytest.mark.run(order=3)
def test_multi_dep_pattern2(depend):
    """skip test"""
    with pytest.raises(DependencyException):
        depend.on_pattern('test_dependency')


@pytest.mark.run(order=3)
def test_multi_dep_pattern3(depend):
    """skip test"""
    depend.on_parameterized('test_dependency_dummy2')


@pytest.mark.run(order=4)
@pytest.mark.parametrize('x', range(3), ids=unique_id.id)
def test_dependency_with_parameters(x, depend):
    depend.on('test_dependency_is_added')


@pytest.mark.run(order=4)
@pytest.mark.parametrize('x', range(3), ids=unique_id.id)
def test_dependency_with_parameters2(x, depend):
    depend.on_parameterized('test_dependency_dummy')


@pytest.mark.run(order=4)
@pytest.mark.parametrize('x', range(3), ids=unique_id.id)
def test_dependency_with_parameters3(x, depend):
    depend.on('test_dependency_is_added', 'test_dependency_is_true', 'test_dependency_dummy2[1]')


@pytest.mark.run(order=4)
@pytest.mark.parametrize('x', range(3), ids=unique_id.id)
def test_dependency_with_parameters4(x, depend):
    """expect to skip"""
    depend.on_pattern('test_dependency_dummy')


@pytest.mark.run(order=4)
@pytest.mark.parametrize('x', range(4), ids=unique_id.id)
def test_dependency_with_parameters5(x, depend):
    """skip on case x == 0"""
    if x == 0:
        depend.on_pattern('test_dependency_dummy')
    elif x == 1:
        depend.on('test_dependency_is_added', 'test_dependency_is_true', 'test_dependency_dummy2[1]')
    elif x == 2:
        depend.on_parameterized('test_dependency_dummy')
    elif x == 3:
        with pytest.raises(DependencyException):
            depend.on_pattern('test_dependency_is_skipped')
