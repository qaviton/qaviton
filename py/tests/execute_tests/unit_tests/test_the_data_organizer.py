import pytest
from qaviton.utils import organize


def test_lists():
    data = []
    r = organize.lists(data)
    assert len(r) == 1

    data = [(123, '5555'), (1, 2, 3, 0, 0), (1, 2), (1, 2, 3, 4)]
    r = organize.lists(data)
    assert len(r) == 80

    data = [(), (1, 2, 3), (1, 2), (1, 2, 3, 4)]
    with pytest.raises(ZeroDivisionError):
        organize.lists(data)


def test_dicts():
    data = {}
    r = organize.dicts(data)
    assert len(r) == 1

    data = dict(a=(123, '5555'), b=(1, 2, 3, 0, 0), c=(1, 2), d=(1, 2, 3, 4))
    r = organize.dicts(data)
    assert len(r) == 80

    data = dict(a=(), b=(1, 2, 3), c=(1, 2), d=(1, 2, 3, 4))
    with pytest.raises(ZeroDivisionError):
        organize.dicts(data)


def test_add():
    item = {"c": (3,)}
    data = [{"a": (1,), "b": (1, 1)}, {"a": (1,), "b": (1, 2)}]

    r = organize.add(data, item)
    assert len(r) == 2

    item = {"c": (3, 4)}
    data = [{"a": (1,), "b": (1, 1)}, {"a": (1,), "b": (1, 2)}]

    r = organize.add(data, item)
    assert len(r) == 4


def test_adds():
    items = [{"c": (3, 4)}, {"d": (5,)}]
    data = [{"a": (1,), "b": (1, 1)}, {"a": (1,), "b": (1, 2)}]

    r = organize.adds(data, items)
    assert len(r) == 4

    items = [{"c": (3, 4)}, {"d": (5, 6)}]
    data = [{"a": (1,), "b": (1, 1)}, {"a": (1,), "b": (1, 2)}]

    r = organize.adds(data, items)
    assert len(r) == 8
