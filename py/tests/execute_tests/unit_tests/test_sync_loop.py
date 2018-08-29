from qaviton.utils.sync_loop import sync_loop
from qaviton.utils.condition import match


def test_sync_loops():
    a = range(20)
    b = range(6)
    i = 0
    expected_results = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 0),
        (7, 1),
        (8, 2),
        (9, 3),
        (10, 4),
        (11, 5),
        (12, 0),
        (13, 1),
        (14, 2),
        (15, 3),
        (16, 4),
        (17, 5),
        (18, 0),
        (19, 1))
    for i1, i2 in sync_loop(a, b):
        assert match((i1, i2), expected_results[i])
        i += 1
