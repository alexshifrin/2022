from dataclasses import dataclass, make_dataclass, field, fields
from typing import Any, List
from math import asin, cos, radians, sin, sqrt

@dataclass
class PlayingCard:
    rank: str
    suit: str

    def __str__(self):
        return f'{self.rank}{self.suit}'

ace_of_spades = PlayingCard('A', '♠')

print(ace_of_spades)

PlayingCard2 = make_dataclass('PlayingCard2', ['rank', 'suit'])

ace_of_spades2 = PlayingCard2('Ace', 'Spades')

print(ace_of_spades2)

@dataclass
class Position:
    name: str
    lon: float = field(default=0.0, metadata={'unit': 'degrees'})
    lat: float = field(default=0.0, metadata={'unit': 'degrees'})

    def distance_to(self, other):
        r = 6371  # Earth radius in kilometers
        lam_1, lam_2 = radians(self.lon), radians(other.lon)
        phi_1, phi_2 = radians(self.lat), radians(other.lat)
        h = (sin((phi_2 - phi_1) / 2)**2
             + cos(phi_1) * cos(phi_2) * sin((lam_2 - lam_1) / 2)**2)
        return 2 * r * asin(sqrt(h))

seattle = Position("Seattle", 47.6, 122.3)

print(seattle)

nowhere = Position("Nowhere")

print(nowhere)

print("Distance from Seattle to nowhere" \
        f" is {seattle.distance_to(nowhere)}!")

@dataclass
class Anything:
    thing: Any

blah = Anything(None)
blah2 = Anything("Alex!")

print(blah, blah2)

@dataclass
class Deck:
    cards: List[PlayingCard]

queen_of_hearts = PlayingCard('Q', 'Hearts')
ace_of_spades = PlayingCard('A', 'Spades')
two_cards = Deck([queen_of_hearts, ace_of_spades])

print(two_cards)

RANKS = '2 3 4 5 6 7 8 9 10 J Q K A'.split()
SUITS = '♣ ♢ ♡ ♠'.split()

def make_french_deck():
    return [PlayingCard(r, s) for s in SUITS for r in RANKS]

@dataclass
class Deck:
    cards: List[PlayingCard] = field(default_factory=make_french_deck)

    def __repr__(self):
        cards = ', '.join(f"{c!s}" for c in self.cards)
        return f"{self.__class__.__name__}({cards})"

print(Deck())

# priint metadata from Position object `seattle`
print(fields(seattle)[2].metadata['unit'])

from dataclasses import dataclass, field

RANKS = '2 3 4 5 6 7 8 9 10 J Q K A'.split()
SUITS = '♣ ♢ ♡ ♠'.split()

@dataclass(order=True)
class PlayingCard:
    sort_index: int = field(init=False, repr=False)
    rank: str
    suit: str

    def __post_init__(self):
        self.sort_index = (RANKS.index(self.rank) * len(SUITS)
                           + SUITS.index(self.suit))

    def __str__(self):
        return f'{self.suit}{self.rank}'

queen_of_hearts = PlayingCard('Q', '♡')
ace_of_spades = PlayingCard('A', '♠')
print(ace_of_spades > queen_of_hearts)

from dataclasses import dataclass

@dataclass
class Position:
    name: str
    lon: float
    lat: float

@dataclass
class Capital(Position):
    country: str