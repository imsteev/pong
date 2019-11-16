from dataclasses import dataclass


@dataclass
class Player:
    name: str = ""
    rating: int = 0


BYE = Player(name="BYE")
