from collections import defaultdict
import round_robin


def test_rotate_empty():
    circle = round_robin.Circle([])
    circle.rotate([])
    assert len(circle) == 0


def test_rotate_clockwise():
    circle = round_robin.Circle([1, 2, 3])
    circle.rotate()
    assert len(circle) == 3
    assert circle[0] == 3
    assert circle[1] == 1
    assert circle[2] == 2


def test_rotate_counter_clockwise():
    circle = round_robin.Circle([1, 2, 3])
    circle.rotate(clockwise=False)
    assert len(circle) == 3
    assert circle[0] == 2
    assert circle[1] == 3
    assert circle[2] == 1


def test_round_robin_invalid_players():
    for i in range(2):
        matchups = list(round_robin.round_robin(i))
        assert matchups == []


def test_even_round_robin_everyone_plays_each_other():
    num_players = 10
    counts = defaultdict(set)
    for round in round_robin.round_robin(num_players):
        for p1, p2 in round:
            counts[p1].add(p2)
            counts[p2].add(p1)

    assert num_players % 2 == 0
    assert len(counts) == num_players
    for p in counts:
        assert len(counts[p]) == num_players - 1
        assert p not in counts[p]  # make sure players don't play themselves


def test_odd_round_robin_everyone_plays_each_other():
    num_players = 11
    counts = defaultdict(set)
    for round in round_robin.round_robin(num_players):
        for p1, p2 in round:
            counts[p1].add(p2)
            counts[p2].add(p1)

    assert num_players % 2 == 1
    assert len(counts) == num_players + 1  # new "dummy" player introduced
    dummy_player = len(counts)
    for p in counts:
        if p == dummy_player:
            # TODO: should we be able to reason about the number of byes?
            continue
        if dummy_player in counts[p]:
            counts[p].remove(dummy_player)
        assert len(counts[p]) == num_players - 1
        assert p not in counts[p]  # make sure players don't play themselves
