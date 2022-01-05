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