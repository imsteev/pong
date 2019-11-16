from dataclasses import dataclass


@dataclass
class Player:
    name: str = ""
    rating: int = 0


DUMMY_PLAYER = Player(name="BYE")
