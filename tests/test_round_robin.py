from collections import defaultdict, namedtuple
import round_robin

Player = namedtuple('Player', 'name rating')


def test_round_robin_invalid_players():
    for i in range(-1, 2):
        matchups = list(round_robin.round_robin(i))
        assert matchups == []


def test_even_round_robin_everyone_plays_each_other():
    # Arrange
    num_players = 10
    counts = defaultdict(set)

    # Act
    for round in round_robin.round_robin(num_players):
        for p1, p2 in round:
            counts[p1].add(p2)
            counts[p2].add(p1)

    # Assert
    assert num_players % 2 == 0
    assert len(counts) == num_players
    for p in counts:
        assert len(counts[p]) == num_players - 1
        assert p not in counts[p]  # make sure players don't play themselves


def test_odd_round_robin_everyone_plays_each_other():
    # Arrange
    num_players = 11
    counts = defaultdict(set)

    # Act
    for round in round_robin.round_robin(num_players):
        for p1, p2 in round:
            counts[p1].add(p2)
            counts[p2].add(p1)

    # Assert
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


def test_construct_matchups_returns_seeded_players_by_rating():
    # Arrange
    round = [(1, 2), (3, 4), (5, 6)]
    players = [Player(name='Picolo', rating=600),
               Player(name='Trunks', rating=700),
               Player(name='Vegeta', rating=900),
               Player(name='Goten', rating=500),
               Player(name='Goku', rating=1000),
               Player(name='Gohan', rating=800)]

    # Act
    result = round_robin.construct_matchups(round, players)

    # Assert
    assert len(result) == 3

    (p1, p1_seed), (p2, p2_seed) = result[0]  # 1 vs 2
    assert p1.name == 'Goku'
    assert p2.name == 'Vegeta'
    assert p1_seed == 1
    assert p2_seed == 2
    assert p1.rating >= p2.rating

    (p1, p1_seed), (p2, p2_seed) = result[1]  # 3 vs 4
    assert p1.name == 'Gohan'
    assert p2.name == 'Trunks'
    assert p1_seed == 3
    assert p2_seed == 4
    assert p1.rating >= p2.rating

    (p1, p1_seed), (p2, p2_seed) = result[2]  # 5 vs 6
    assert p1.name == 'Picolo'
    assert p2.name == 'Goten'
    assert p1_seed == 5
    assert p2_seed == 6
    assert p1.rating >= p2.rating
