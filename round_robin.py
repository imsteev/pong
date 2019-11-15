from collections import defaultdict


def rotate(L, clockwise=True):
    if not L:
        return []
    return [L[-1]] + L[:-1] if clockwise else L[1:] + [L[0]]


def round_robin(n):
    """
    https://en.wikipedia.org/wiki/Round-robin_tournament

    Create a round-robin schedule from players 1 to n, inclusive.
    If n is odd, there will be matchups with BYEs.
    """
    bye_num = None
    if n % 2 == 1:
        n += 1
        bye_num = n

    matchups = []

    # Construct rotatable circle with everyone but first player
    circle = list(range(2, n+1))

    for _ in range(n-1):
        group = []
        circle.insert(0, 1)  # fix the first player in the circle
        for i in range(n // 2):
            p1, p2 = circle[i], circle[n-1-i]
            if p1 == bye_num:
                p1 = "BYE"
            if p2 == bye_num:
                p2 = "BYE"
            group.append((p1, p2))
        circle.pop(0)
        matchups.append(group)
        circle = rotate(circle)

    return matchups
