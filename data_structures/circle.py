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
