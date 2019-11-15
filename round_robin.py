from collections import deque


class Circle:
    """
    Circular queue.
    Supports direct indexing and the ability to rotate clockwise or counterclockwise.
    """

    def __init__(self, L):
        self.circle = deque(L or [])

    def __len__(self):
        return len(self.circle)

    def __getitem__(self, i):
        """
        Return i-th element of the circle, where 0-th element is at 12 o'clock
        """
        # TODO: safety checks
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

    def insert_beginning(self, x):
        self.circle.appendleft(x)

    def remove_beginning(self):
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
    circle = Circle(list(range(2, n+1)))

    for _ in range(n-1):
        round = []

        # fix the first player in the circle
        circle.insert_beginning(1)

        for i in range(n//2):
            p1, p2 = circle[i], circle[n-1-i]  # play the person "opposite" of you in the circle
            matchup = min(p1, p2), max(p1, p2)
            round.append(matchup)

        yield round

        # rotate everyone else but the first player
        circle.remove_beginning()
        circle.rotate()


if __name__ == "__main__":
    NUM_PLAYERS = 7  # adjust this accordingly
    DUMMY_PLAYER = {"rank": '-', 'name': "BYE"}

    players = [{"rank": 1, "name": "Michael Gary Scott"},
               {"rank": 2, "name": "Jim Halpert"},
               {"rank": 3, "name": "Pam Beasley"},
               {"rank": 4, "name": "Kevin Malone"},
               {"rank": 5, "name": "Phyllis Vance"},
               {"rank": 6, "name": "Dwight Schrute"},
               {"rank": 7, "name": "Robert California"},
               {"rank": 8, "name": "Kelly Kapoor"}]

    players.sort(key=lambda info: info['rank'])

    for i, round in enumerate(round_robin(NUM_PLAYERS), 1):
        print("ROUND {}".format(i))
        for (p1, p2) in round:
            # players are ranked starting from 1
            if 0 <= p1 - 1 < NUM_PLAYERS:
                player1 = players[p1-1]
            else:
                player1 = DUMMY_PLAYER
            if 0 <= p2 - 1 < NUM_PLAYERS:
                player2 = players[p2-1]
            else:
                player2 = DUMMY_PLAYER
            print("{0} ({1}) v. {2} ({3})".format(player1['name'], player1['rank'], player2['name'], player2['rank']))
        print()
