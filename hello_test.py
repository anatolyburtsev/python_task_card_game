import pytest
from hypothesis import given
from lenses import lens

from main import Value, Game, Player, Card, Color
import hypothesis.strategies as st


@given(st.integers(Value.MIN_VALUE, Value.MAX_VALUE))
def test_positive_scenarios(value):
    valueInst = Value(value)

    assert valueInst.value == value
    assert int(valueInst) == value


@given(st.integers().filter(lambda x: x < Value.MIN_VALUE or x > Value.MAX_VALUE))
def test_invalid_input_outside_range(value):
    with pytest.raises(ValueError):
        Value(value)


@given(st.text())
def test_invalid_input_string_type(value):
    with pytest.raises(ValueError):
        Value(value)


def test_simple_game():
    player = Player([Card(Value(5), Color.RED), Card(Value(6), Color.RED)])
    game = Game(0, players=[player])
    winners = game.find_winners()
    assert winners == [player]


value_gen = st.integers(Value.MIN_VALUE, Value.MAX_VALUE).map(Value)
unique_value_gen = st.lists(value_gen, unique=True)
color_gen = st.sampled_from(Color)
unique_colors_gen = st.lists(color_gen, min_size=2, max_size=len(Color), unique=True)
card_fixed_color_gen = lambda color: value_gen.map(lambda value: Card(value, color))
card_gen = color_gen.flatmap(card_fixed_color_gen)

player_one_color = color_gen.flatmap(
    lambda color: st.lists(card_fixed_color_gen(color), min_size=1, unique=True).map(
        Player
    )
)

player_one_value_gen = value_gen.flatmap(
    lambda value: unique_colors_gen.map(
        lambda colors: Player([Card(value, color) for color in colors])
    )
)


@st.composite
def unique_cards(draw):
    color_value_tuples = draw(st.lists(st.tuples(color_gen, value_gen), unique=True))
    cards = [Card(value, color) for color, value in color_value_tuples]
    return cards


cards_gen = st.lists(
    color_gen.flatmap(lambda color: value_gen.map(lambda value: Card(value, color))),
    min_size=1,
    unique=True,
)

player_one_pair_gen = cards_gen.filter(
    lambda cards: len(cards) - 1 == len(set(map(lens.value.get(), cards)))
).map(Player)

# TODO: implement player looser generator
# player_loser = st.lists(
#     colo
# )

# print(player_one_pair_gen.example())


@given(st.tuples(player_one_color, player_one_color))
def test_two_winners(input_data):
    player1, player2 = input_data
    game = Game(0, players=[player1, player2])
    winners = game.find_winners()
    assert winners == [player1, player2]


@given(st.tuples(player_one_color, player_one_value_gen))
def test_two_strategies_one_winner(input_data):
    player1, player2 = input_data
    game = Game(0, players=[player1, player2])
    winners = game.find_winners()
    assert winners == [player1]


@given(player_one_pair_gen)
def test_one_pair_winner(player):
    game = Game(0, players=[player])
    winners = game.find_winners()
    assert winners == [player]


### TODO: add test with no matches
