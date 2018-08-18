from qaviton.utils import condition
import pytest


def test_condition_any_in_any1():
    a = "123456789"
    b = "098765"
    assert condition.any_in_any(a, b)


def test_condition_any_in_any2():
    a = ""
    b = "098765"
    assert not condition.any_in_any(a, b)


def test_condition_any_in_any3():
    a = "123456789".split()
    b = "098765"
    assert not condition.any_in_any(a, b)


def test_condition_any_in_any4():
    a = list("123456789")
    b = "098765"
    assert condition.any_in_any(a, b)


def test_condition_any_in_any5():
    a = list("123456789")
    b = list("098765")
    assert condition.any_in_any(a, b)


def test_condition_all_in_any1():
    a = list("123")
    b = list("1234")
    assert condition.all_in_any(a, b)


def test_condition_all_in_any2():
    a = list("12345")
    b = list("1234")
    assert not condition.all_in_any(a, b)


def test_condition_all_in_all1():
    a = list("1234")
    b = list("1234")
    assert condition.all_in_all(a, b)


def test_condition_all_in_all2():
    a = list("1234")
    b = list("12345")
    assert not condition.all_in_all(a, b)


def test_condition_all_in_all3():
    a = list("1234")
    b = list("123")
    assert not condition.all_in_all(a, b)


def test_condition_value_in_many_any():
    class M:
        e1 = 'e1'
        e2 = 'e2'
        e3 = 'e3'

    class V:
        a1 = 'a1'
        a2 = 'a2'
        a3 = 'a3'

    assert condition.value_in_many_any('a1', (vars(M).values(), vars(V).values()))
    assert condition.value_in_many_any('a2', (vars(M).values(), vars(V).values()))
    assert condition.value_in_many_any('a3', (vars(M).values(), vars(V).values()))
    assert condition.value_in_many_any('e1', (vars(M).values(), vars(V).values()))
    assert condition.value_in_many_any('e2', (vars(M).values(), vars(V).values()))
    assert condition.value_in_many_any('e3', (vars(M).values(), vars(V).values()))
    assert not condition.value_in_many_any('e4', (vars(M).values(), vars(V).values()))


def test_condition_any_in_many_any():
    class M:
        e1 = 'e1'
        e2 = 'e2'
        e3 = 'e3'

    class V:
        a1 = 'a1'
        a2 = 'a2'
        a3 = 'a3'

    assert condition.any_in_many_any(('a1','e2'), (vars(M).values(), vars(V).values()))
    assert condition.any_in_many_any(('a2', 'e3'), (vars(M).values(), vars(V).values()))
    assert condition.any_in_many_any(('a3', 'e1'), (vars(M).values(), vars(V).values()))
    assert condition.any_in_many_any(('a1',), (vars(M).values(), vars(V).values()))
    assert condition.any_in_many_any(('e2',), (vars(M).values(), vars(V).values()))
    assert condition.any_in_many_any(('e2', 'r3'), (vars(M).values(), vars(V).values()))
    assert condition.any_in_many_any(('r3', 'e2'), (vars(M).values(), vars(V).values()))
    assert not condition.any_in_many_any(('e4',), (vars(M).values(), vars(V).values()))
    assert not condition.any_in_many_any(('e4',), (vars(M).values(), vars(V).values()))
