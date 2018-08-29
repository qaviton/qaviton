import pytest
from qaviton.utils import unique_id
from qaviton.fixtures.dependency import Depend, DependencyException, dependency, dependencies, depend
from qaviton.utils.helpers import funcname


@pytest.fixture
def add_dep_label(dependencies):
    """label options are:
    0 - dependency is ok
    1 - dependency has failed
    2 - dependency has skipped
    """
    dependencies['label-red'] = 0


@pytest.mark.run(order=1)
def test_label1(depend, add_dep_label):
    depend.on('label-red')


@pytest.mark.run(order=2)
def test_label2(dependencies):
    dependencies['label-red'] = 1


@pytest.mark.run(order=3)
def test_label3(depend):
    depend.fail_when_dependency_fails().on('label-red')


@pytest.mark.run(order=1)
def test_dependency_is_added(dependency, dependencies):
    assert dependencies[funcname()] is None


@pytest.mark.run(order=1)
@pytest.mark.skip(reason='check skipped dependency')
def test_dependency_is_skipped(dependency):
    pass


@pytest.mark.run(order=1)
@pytest.mark.xfail(reason='check failed dependency')
def test_dependency_failure(dependency):
    assert 0


@pytest.mark.run(order=2)
def test_dependency_is_true(dependencies, dependency):
    assert dependencies['test_dependency_is_added'] == 0


@pytest.mark.run(order=2)
def test_depend(depend):
    depend.on('test_dependency_is_added')


@pytest.mark.run(order=2)
def test_wrong_depend(depend):
    with pytest.raises(DependencyException):
        depend.on('wrong_depend')


@pytest.mark.run(order=1)
def test_depend_wrong_order(depend):
    with pytest.raises(DependencyException):
        depend.on('test_dependency_is_true')


@pytest.mark.run(order=2)
def test_depend_on_skipped(depend):
    with pytest.raises(DependencyException):
        depend.on('test_dependency_is_skipped')


@pytest.mark.run(order=2)
def test_depend_on_xfail(depend):
    depend.on('test_dependency_failure')


@pytest.mark.run(order=2)
def test_depend_on_xfail2(depend):
    depend.fail_when_dependency_fails().on('test_dependency_failure')


@pytest.mark.run(order=1)
@pytest.mark.parametrize('n', range(3), ids=unique_id.id)
def test_dependency_dummy(dependency, n):
    pass


@pytest.mark.run(order=1)
@pytest.mark.xfail(reason='fail check')
@pytest.mark.parametrize('n', range(3), ids=unique_id.id)
def test_dependency_dummy2(dependency, n):
    if n == 2:
        pytest.fail('fail check')


@pytest.mark.run(order=2)
def test_multi_dep(depend):
    depend.on(*['test_dependency_dummy[{}]'.format(n) for n in range(3)])


@pytest.mark.run(order=2)
def test_multi_dep_multi_pattern(depend):
    depend.on_parameterized('test_dependency_dummy')


@pytest.mark.run(order=2)
def test_multi_dep_pattern(depend):
    depend.on_pattern('test_dependency_dummy')


@pytest.mark.run(order=2)
def test_multi_dep_pattern2(depend):
    with pytest.raises(DependencyException):
        depend.on_pattern('test_dependency')


@pytest.mark.run(order=2)
def test_multi_dep_pattern3(depend):
    depend.on_parameterized('test_dependency_dummy2')


@pytest.mark.run(order=3)
@pytest.mark.parametrize('x', range(3), ids=unique_id.id)
def test_dependency_with_parameters(x, depend):
    depend.on('test_dependency_is_added')


@pytest.mark.run(order=3)
@pytest.mark.parametrize('x', range(3), ids=unique_id.id)
def test_dependency_with_parameters2(x, depend):
    depend.on_parameterized('test_dependency_dummy')


@pytest.mark.run(order=3)
@pytest.mark.parametrize('x', range(3), ids=unique_id.id)
def test_dependency_with_parameters3(x, depend):
    depend.on('test_dependency_is_added', 'test_dependency_is_true', 'test_dependency_dummy2[1]')


@pytest.mark.run(order=3)
@pytest.mark.parametrize('x', range(3), ids=unique_id.id)
def test_dependency_with_parameters4(x, depend):
    depend.on_pattern('test_dependency_dummy')


@pytest.mark.run(order=3)
@pytest.mark.parametrize('x', range(4), ids=unique_id.id)
def test_dependency_with_parameters5(x, depend):
    if x == 0:
        depend.on_pattern('test_dependency_dummy')
    elif x == 1:
        depend.on('test_dependency_is_added', 'test_dependency_is_true', 'test_dependency_dummy2[1]')
    elif x == 2:
        depend.on_parameterized('test_dependency_dummy')
    elif x == 3:
        with pytest.raises(DependencyException):
            depend.on_pattern('test_dependency_is_skipped')
