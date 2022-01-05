from dataclasses import dataclass, make_dataclass

@dataclass
class PlayingCard:
    rank: str
    suit: str

ace_of_spades = PlayingCard('Ace', 'Spades')

print(ace_of_spades)

PlayingCard2 = make_dataclass('PlayingCard2', ['rank', 'suit'])

ace_of_spades2 = PlayingCard2('Ace', 'Spades')

print(ace_of_spades2)

@dataclass
class Position:
    name: str
    lat: float = 0.0
    lon: float = 0.0

seattle = Position("Seattle", 47.6, 122.3)

print(seattle)

nowhere = Position("Nowhere")

print(nowhere)