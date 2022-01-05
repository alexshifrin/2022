from dataclasses import dataclass

@dataclass
class PlayingCard:
    rank: str
    suit: str

ace_of_spades = PlayingCard('Ace', 'Spades')

print(ace_of_spades)