from collections import deque
from typing import Iterable


class Circle:
    """
    Circular queue.
    Supports direct indexing and the ability to rotate clockwise or counterclockwise.
    """

    def __init__(self, A: Iterable):
        self.circle = deque(A or [])

    def __len__(self):
        return len(self.circle)

    def __getitem__(self, i):
        """
        Return i-th element of the circle, where 0-th element is at 12 o'clock
        """
        return self.circle[i]

    def rotate(self, clockwise=True):
        if not self.circle:
            return
        if clockwise:
            last = self.circle.pop()
            self.circle.appendleft(last)
        else:
            first = self.circle.popleft()
            self.circle.append(first)

    def insert_head(self, x):
        """
        Inserts item at the head of the queue. In the circle, it is the item at 12 o'clock
        """
        self.circle.appendleft(x)

    def remove_head(self):
        """
        Removes head from the queue.
        """
        return self.circle.popleft() if self.circle else None


def round_robin(n):
    """
    https://en.wikipedia.org/wiki/Round-robin_tournament

    Generator for a round-robin schedule for n players.
    If n is odd, a dummy player will be introduced as player (n+1).
    Each iteration will yield a list of tuple matchups (p1, p2).
    """
    if n < 2:
        print("No round robin exists for schedule with less than two players")
        return

    # normalize to even amount of players
    n = n if n % 2 == 0 else n + 1

    # construct rotatable circle with everyone but first player
    circle = Circle(range(2, n+1))

    for _ in range(n-1):
        round = []

        # fix the first player in the circle
        circle.insert_head(1)

        for i in range(n//2):
            p1, p2 = circle[i], circle[n-1-i]  # play the person "opposite" of you in the circle
            matchup = min(p1, p2), max(p1, p2)
            round.append(matchup)

        yield round

        # rotate everyone else but the first player
        circle.remove_head()
        circle.rotate()


if __name__ == "__main__":
    import pandas as pd
    import random
    from registry import DUMMY_PLAYER, Player

    with open('./players/the_office.csv') as f:
        df = pd.read_csv(f, delimiter=',')

    pool = [Player(**p) for _, p in df.iterrows()]

    # get 5 random players
    random.shuffle(pool)
    players = pool[:5]
    players.sort(key=lambda p: -p.rating)  # sort the players by rating, highest to lowest

    num_players = len(players)
    for i, round in enumerate(round_robin(num_players), 1):
        print("ROUND {}".format(i))
        for (p1, p2) in round:

            # get player 1
            if 0 <= p1 - 1 < num_players:
                player1 = players[p1-1]
                p1_seed = p1
            else:
                player1 = DUMMY_PLAYER
                p1_seed = "-"

            # get player 2
            if 0 <= p2 - 1 < num_players:
                player2 = players[p2-1]
                p2_seed = p2
            else:
                player2 = DUMMY_PLAYER
                p2_seed = "-"

            print("{0} ({1}) v. {2} ({3})".format(player1.name, p1_seed, player2.name, p2_seed))
        print()
