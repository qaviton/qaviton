from qaviton.utils import condition


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

