import pytest

"""
Converts int into string
"""
def foo(n: int) -> str:
    return str(n)

def test_fail():
    assert(1 == 2)

def test_test_unit_test():
    test1 = foo(10) # "10"
    assert(test1 == "10")

def test_deck_gen_properly():
    """
    Testing that all 52 cards are being generated correctly
    """
    from utils.deck import Deck

    deck = Deck()

    suites = ["S", "C", "H", "D"]
    faces = [i for i in range(1, 14, 1)]

    assert(len(deck.cards) == 52) #To check that 52 cards were generated

    card_index = 0
    for suite in suites:
        for face in faces:
            curr_card = deck.cards[card_index]
            assert(curr_card.suite == suite and curr_card.face == face)
            card_index += 1

def test_deck_shuffle():
    from utils.deck import Deck

    deck_shuffled = Deck()
    deck_shuffled.shuffle()


    suites = ["S", "C", "H", "D"]
    faces = [i for i in range(1, 14, 1)]

    card_dict = {}
    """
    suite: {
        face: False
    }
    """
    for suite in suites:
        card_dict[suite] = {}
        for face in faces:
            card_dict[suite][face] = False

    assert(len(deck_shuffled.cards) == 52)
    for card in deck_shuffled.cards:
        assert(card.suite in card_dict)
        assert(card.face in card_dict[card.suite])
        assert(not card_dict[card.suite][card.face])
        card_dict[card.suite][card.face] = True

def test_deck_shuffle2():
    from utils.deck import Deck

    deck_unshuffled = Deck()
    deck_shuffled = Deck()

    deck_shuffled.shuffle()

    num_matches = 0

    for i in range(52):
        if deck_unshuffled.cards[i] == deck_shuffled.cards[i]:
            num_matches += 1

    assert(num_matches < 5)

"""
Player Test Cases
"""

def test_add_card():
    from utils.player import Player
    from utils.deck import Deck

    player = Player()
    deck = Deck()

    deck.shuffle()

    for i in range(5):
        curr_card = deck.draw_card()
        player.add_card(curr_card)
        assert(player.hand[-1] == curr_card)

def make_class_of_hand_testcase(hand, common_cards) -> tuple[int, object]:
    from utils.player import Player
    from utils.deck import Card

    player = Player()

    for curr_card in hand:
        player.add_card(curr_card)

    return player.idenitfy_class_of_hand(common_cards)

def test_high_card():
    from utils.deck import Card
    hand = [
        Card("S", 2),
        Card("D", 3)
    ]
    common_cards = [
        Card("C", 1),
        Card("D", 9),
        Card("S", 10),
        Card("H", 8),
        Card("H", 5)
    ]
    class_of_hand, highest_card = make_class_of_hand_testcase(hand, common_cards)

    assert(class_of_hand == 1)
    assert(highest_card == common_cards[0])