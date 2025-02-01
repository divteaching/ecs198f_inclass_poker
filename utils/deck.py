#Standard Library Imports
import random

from typing import Literal

class Card:
    def __init__(self, suite: Literal["S", "C", "H", "D"], face: int):
        """
        1 --> ACE
        2 - 10 --> Number Cards
        11 --> Jack
        12 --> Queen
        13 --> King
        """
        if face < 1 or face > 14:
            raise Exception("Invalid face")

        self.suite = suite
        self.face = face

    def __str__(self):
        return f"{self.suite}:{self.face}"
    
class Deck:
    def __init__(self):
        self.create_cards()

    def create_cards(self):
        self.cards = []
        suites = ["S", "C", "H", "D"]
        faces = [i for i in range(1, 14, 1)]

        for suite in suites:
            for face in faces:
                self.cards.append(Card(suite, face))

    def shuffle(self):
        #Shuffle the deck
        random.shuffle(self.cards)

    def draw_card(self) -> Card:
        if len(self.cards) <= 0:
            raise Exception("Deck is empty")
        return self.cards.pop(0)