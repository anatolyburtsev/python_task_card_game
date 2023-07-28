from typing import List, Tuple, Dict
from enum import Enum
from dataclasses import dataclass
from random import shuffle
from lenses import lens

# Initial Rules:
#
# The game consists of 30 cards, where each card has a Value which is a number between 0-9 and a Color which is
# Red, Green, or Blue (RGB)
# Each player gets 3 cards
# Each game consists of some number of players, and winners are determined by who has the best Combo:
#     Color Combo (3 cards same color)
#     Value Combo (3 cards same value)
#     Pair Combo (2 cards with same value, and 1 random card)
#     etc. (emphasizing there are many possibilities and it's not important to know all of them)
# Write the library required to play this game. Don't worry about UI or getters/setters/constructors,
# or implementing every method, just draw out what you need and who will call what, and we will dive deeper
# into the interesting areas.


class Value:
    MIN_VALUE = 0
    MAX_VALUE = 9

    def __init__(self, value):
        if not isinstance(value, int):
            raise ValueError()
        if not (self.MIN_VALUE <= value <= self.MAX_VALUE):
            raise ValueError()
        self.value = value

    def __int__(self):
        return self.value

    @staticmethod
    def range():
        return range(Value.MIN_VALUE, Value.MAX_VALUE)

    def __repr__(self):
        return str(self.value)

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.value == other.value


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


@dataclass()
class Card:
    value: Value
    color: Color

    @staticmethod
    def of(val: int, color: str):
        return Card(Value(val), Color[color.upper()])

    def __hash__(self):
        return hash(str(self.value) + self.color.name)

    def __eq__(self, other):
        return self.value == other.value and self.color == other.color


class Deck:
    def __init__(self):
        self.cards = [
            Card(Value(value), color) for value in Value.range() for color in Color
        ]
        shuffle(self.cards)


@dataclass()
class Player:
    hand: List[Card]


def dealer(users_count: int, deck: Deck) -> List[Player]:
    NUMBER_OF_CARDS_IN_HAND = 3
    return [
        Player(deck.cards[i : i + NUMBER_OF_CARDS_IN_HAND]) for i in range(users_count)
    ]


class Game:
    def __init__(self, users_count, players=None):
        if players is None:
            players = dealer(users_count, Deck())
        self.players = players

    COMBOS = {
        "Color_Combo": lambda player: len(set(map(lens.color.get(), player.hand))) == 1,
        "Value_Combo": lambda player: len(set(map(lens.value.get(), player.hand))) == 1,
        "Pair_Combo": lambda player: len(set(map(lens.value.get(), player.hand)))
        == len(player.hand) - 1,
    }

    def find_winners(self):
        for combo_name, combo_predicate in self.COMBOS.items():
            winners = list(filter(combo_predicate, self.players))
            if winners:
                return winners

        return None


if __name__ == "__main__":
    d = Deck()
    print(d.cards)
    print(dealer(3))
