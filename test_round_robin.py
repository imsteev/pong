import round_robin


def test_rotate_empty():
    res = round_robin.rotate([])
    assert res == []


def test_rotate_clockwise():
    A = [1, 2, 3]
    res = round_robin.rotate(A)
    assert res == [3, 1, 2]


def test_rotate_counter_clockwise():
    A = [1, 2, 3]
    res = round_robin.rotate(A, clockwise=False)
    assert res == [2, 3, 1]