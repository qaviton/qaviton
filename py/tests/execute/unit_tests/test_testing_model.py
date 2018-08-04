import pytest
from qaviton import test_model


def test_organize():
    data_lists = []
    test_model.organize(data_lists)

    data_lists = [(123, '5555'), (1, 2, 3, 0, 0), (1, 2), (1, 2, 3, 4)]
    test_model.organize(data_lists)

    data_lists = [(), (1, 2, 3), (1, 2), (1, 2, 3, 4)]
    with pytest.raises(Exception):
        test_model.organize(data_lists)