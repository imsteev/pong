from collections import defaultdict, namedtuple
import round_robin

Player = namedtuple('Player', 'name rating')


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


def test_get_matchups_returns_seeded_players_by_rating():
    players = [
        Player(name='Picolo', rating=600),
        Player(name='Trunks', rating=700),
        Player(name='Vegeta', rating=900),
        Player(name='Goten', rating=500),
        Player(name='Goku', rating=1000),
        Player(name='Gohan', rating=800),
    ]
    round = [(1, 2), (3, 4), (5, 6)]

    matchups = round_robin.get_matchups(round, players)

    assert len(matchups) == 3

    matchup1 = matchups[0]  # 1 vs 2
    assert matchup1[0][1] == 1
    assert matchup1[1][1] == 2
    assert matchup1[0][0].name == 'Goku'
    assert matchup1[1][0].name == 'Vegeta'

    matchup2 = matchups[1]  # 3 vs 4
    assert matchup2[0][1] == 3
    assert matchup2[1][1] == 4
    assert matchup2[0][0].name == 'Gohan'
    assert matchup2[1][0].name == 'Trunks'

    matchup3 = matchups[2]  # 5 vs 6
    assert matchup3[0][1] == 5
    assert matchup3[1][1] == 6
    assert matchup3[0][0].name == 'Picolo'
    assert matchup3[1][0].name == 'Goten'
