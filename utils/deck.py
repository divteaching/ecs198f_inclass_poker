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
        14 --> ACE
        """
        if face < 1 or face > 15:
            raise Exception("Invalid face")

        self.suite = suite
        self.face = face

    def __str__(self):
        return f"{self.suite}:{self.face}"
    
    def __eq__(self, other):
        actual_face1 = self.face
        actual_face2 = other.face
        if actual_face1 == 14:
            actual_face1 = 1
        if actual_face2 == 14:
            actual_face2 = 1

        return (self.suite == other.suite) and (actual_face1 == actual_face2)
        
    
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

    def __str__(self):
        return_str = ""
        for card in self.cards:
            return_str += str(card)
            return_str += "\n"
        return return_str