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