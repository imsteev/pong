from dataclasses import dataclass


@dataclass
class Player:
    name: str = "BYE"
    rating: int = 0


DUMMY_PLAYER = Player()
