from dataclasses import dataclass, make_dataclass
from typing import Any
from math import asin, cos, radians, sin, sqrt

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
    lon: float = 0.0
    lat: float = 0.0

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