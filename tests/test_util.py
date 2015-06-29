from afthermal.util import in_range, from_range

import pytest


@pytest.mark.parametrize('start,end,step', [
    (1, 10, 1),
    (2, 5, 2),
    (15, 50, 3),
    (2, 10, 1),
])
def test_different_ranges(start, end, step):
    for v in range(start, end, step):
        assert in_range(start, end, step)(v)
    assert not in_range(start, end, step)(end)
    assert not in_range(start, end, step)(start-1)


def test_allows_in_between():
    assert in_range(1, 2)(1.5)


def test_rejects_non_integer_on_step1():
    assert not in_range(1, 2, 1)(1.5)


def test_assertions_work():
    from_range(1, 2)(1.5)

    with pytest.raises(ValueError):
        from_range(1, 2, 1)(1.5)


def test_value_conversion():
    assert from_range(8, 256 * 8, 8)(64) == 7
