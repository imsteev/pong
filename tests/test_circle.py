from data_structures.circle import Circle


def test_rotate_empty():
    circle = Circle([])
    circle.rotate([])
    assert len(circle) == 0


def test_rotate_clockwise():
    circle = Circle([1, 2, 3])
    circle.rotate()
    assert len(circle) == 3
    assert circle[0] == 3
    assert circle[1] == 1
    assert circle[2] == 2


def test_rotate_counter_clockwise():
    circle = Circle([1, 2, 3])
    circle.rotate(clockwise=False)
    assert len(circle) == 3
    assert circle[0] == 2
    assert circle[1] == 3
    assert circle[2] == 1
