from utils.deck import Card
from functools import cmp_to_key

class Player:
    def __init__(self):
        self.hand = []
        self.is_big_blind = False
        self.is_small_blind = False
        self.curr_bet = 0
        self.has_raised = False
        self.has_folded = False

    def add_card(self, card: Card):
        self.hand.append(card)

    def get_hand(self) -> list[Card]:
        return self.hand
    
    def clear(self):
        self.hand = []
        self.is_big_blind = False
        self.is_small_blind = False
        self.has_raised = False
        self.has_folded = False

    def set_curr_bet(self, bet: int):
        self.curr_bet = bet

    def _group_card_by_face(self, all_cards: list[Card]) -> list[list[Card]]:
        grouping = []
        faces = [i for i in range(1, 14, 1)]
        for face in faces:
            grouping.append([])

        for curr_card in all_cards:
            grouping[curr_card.face - 1].append(curr_card)

        return grouping
    
    def _check_num_cards_of_same_face(self, all_cards: list[Card], num_cards) -> list[list[Card]]:
        groupings = self._group_card_by_face(all_cards)

        all_groupings = []
        if len(groupings[0]) >= num_cards:
            all_groupings.apend(groupings[0])

        for i in range(12, 0, -1): # 12 to 1 decrement by 1
            if len(groupings[i]) >= num_cards:
                all_groupings.append(groupings[i])
        
        return all_groupings

    def is_royal_flush(self, common_cards: list[Card]) -> tuple[bool, list[Card]]:
        cards_indexed_by_suite = {}
        track_impt_cards_by_suite = {}
        suites = ["S", "C", "H", "D"]
        card_ranks = [1, 10, 11, 12, 13]
        for curr_suite in suites:
            cards_indexed_by_suite[curr_suite] = []
            track_impt_cards_by_suite[curr_suite] = []
            for curr_rank in card_ranks:
                cards_indexed_by_suite[curr_suite].append(curr_rank)

        all_cards = self.hand + common_cards
        for curr_card in all_cards:
            if curr_card.face in card_ranks:
                cards_indexed_by_suite[curr_card.suite].remove(curr_card.face)
                track_impt_cards_by_suite[curr_card.suite].append(curr_card)

        for curr_value in track_impt_cards_by_suite.values():
            if len(curr_value) == 5:
                return True, curr_value
            
        return False, []
    
    def is_straight_flush(self, common_cards: list[Card]) -> tuple[bool, list[Card]]:
        is_flush, flush_cards = self.is_flush(common_cards) 
        is_straight, straight_cards = self.is_straight(common_cards)

        if is_flush and is_straight:
            #You might have a straight flush
            cards_in_straight_flush = []
            for curr_straight_choices in straight_cards:
                is_choice_card = False
                for curr_straight_choice in curr_straight_choices:
                    if curr_straight_choice in flush_cards:
                        is_choice_card = True
                        cards_in_straight_flush.append(curr_straight_choice)
                        break
                if not is_choice_card:
                    if len(cards_in_straight_flush) >= 5:
                        break
                    cards_in_straight_flush = []
            
            if len(cards_in_straight_flush) >= 5:
                return True, cards_in_straight_flush

        return False, []
    
    def is_four_of_a_kind(self, common_cards: list[Card]) -> tuple[bool, list[Card]]:
        all_cards = self.hand + common_cards
        all_groupings = self._check_num_cards_of_same_face(all_cards, 4)
        if len(all_groupings) >= 1:
            return True, all_groupings[0]
        return False, []

    def is_full_house(self, common_cards: list[Card]) -> tuple[bool, list[Card]]:
        all_cards = self.hand + common_cards
        all_pair_groupings = self._check_num_cards_of_same_face(all_cards, 2)
        all_three_groupings = self._check_num_cards_of_same_face(all_cards, 3)
        if len(all_pair_groupings) >= 1 and len(all_three_groupings) >= 1:
            all_pairs_rank = [cards[0].face for cards in all_pair_groupings]
            all_three_rank = [cards[0].face for cards in all_three_groupings]
            for three_index, three_rank in enumerate(all_three_rank):
                for pair_index, pair_rank in enumerate(all_pairs_rank):
                    if three_rank != pair_rank:
                        return_cards = all_three_groupings[three_index] + all_pair_groupings[pair_index]
                        return True, return_cards
        return False, []

    def is_flush(self, common_cards: list[Card]) -> tuple[bool, list[Card]]:
        cards_indexed_by_suite = {}
        suites = ["S", "C", "H", "D"]
        for curr_suite in suites:
            cards_indexed_by_suite[curr_suite] = []

        all_cards = self.hand + common_cards
        for curr_card in all_cards:
            if curr_card not in cards_indexed_by_suite[curr_card.suite]:
                cards_indexed_by_suite[curr_card.suite].append(curr_card)

        for curr_value in cards_indexed_by_suite.values():
            if len(curr_value) >= 5:
                return True, curr_value
        return False, []
    
    def is_straight(self, common_cards: list[Card]) -> tuple[bool, list[list[Card]]]:
        all_cards = self.hand + common_cards
        new_all_cards = []

        for curr_card in all_cards:
            new_all_cards.append(curr_card)
            if curr_card.face == 1:
                #Ace Duplicate it
                new_ace_card = Card(curr_card.suite, 14)
                new_all_cards.append(new_ace_card)

        def card_compare(card1: Card, card2: Card):
            return card1.face - card2.face
        
        new_all_cards = sorted(new_all_cards, key=cmp_to_key(card_compare))

        sequence_cards = [[new_all_cards[0]]]

        for i in range(1, len(new_all_cards), 1):
            if new_all_cards[i].face - new_all_cards[i - 1].face == 1:
                sequence_cards.append([new_all_cards[i]])
            elif new_all_cards[i].face - new_all_cards[i - 1].face == 0:
                sequence_cards[-1].append(new_all_cards[i])
            else:
                if len(sequence_cards) >= 5:
                    break
                sequence_cards = [[new_all_cards[i]]]
        
        if len(sequence_cards) >= 5:
            return True, sequence_cards #Return last 5 cards
        
        return False, []
    
    def is_three_of_a_kind(self, common_cards: list[Card]) -> tuple[bool, list[Card]]:
        all_cards = self.hand + common_cards
        all_groupings = self._check_num_cards_of_same_face(all_cards, 3)
        if len(all_groupings) >= 1:
            return True, all_groupings[0]
        return False, []
    
    def is_two_pairs(self, common_cards: list[Card]) -> tuple[bool, list[list[Card]]]:
        all_cards = self.hand + common_cards
        all_groupings = self._check_num_cards_of_same_face(all_cards, 2)
        if len(all_groupings) >= 2:
            return True, [all_groupings[0], all_groupings[1]]
        return False, []

    def is_two_of_a_kind(self, common_cards: list[Card]) -> tuple[bool, list[Card]]:
        all_cards = self.hand + common_cards
        all_groupings = self._check_num_cards_of_same_face(all_cards, 2)
        if len(all_groupings) >= 1:
            return True, all_groupings[0]
        return False, []
    
    def idenitfy_class_of_hand(self, common_cards: list[Card]) -> tuple[int, Card]:
        is_royal_flush, cards = self.is_royal_flush(common_cards)
        is_straight_flush, cards = self.is_straight_flush(common_cards)
        is_four_of_kind, cards = self.is_four_of_a_kind(common_cards)
        is_full_house, cards = self.is_full_house(common_cards)
        is_flush, cards = self.is_flush(common_cards)
        is_straight, cards = self.is_straight(common_cards)
        is_three_of_kind, cards = self.is_three_of_a_kind(common_cards)
        is_two_pair, cards = self.is_two_pairs(common_cards)
        is_pair, cards = self.is_two_of_a_kind(common_cards)
        if is_royal_flush:
            return 10, None
        if is_straight_flush:
            return 9, None
        if is_four_of_kind:
            return 8, None
        if is_full_house:
            return 7, None
        if is_flush:
            return 6, None
        if is_straight:
            return 5, None
        if is_three_of_kind:
            return 4, None
        if is_two_pair:
            return 3, None
        if is_pair:
            return 2, None
        #High Card
        def card_compare(card1: Card, card2: Card):
            return card1.face - card2.face
        all_cards = self.hand + common_cards
        all_cards = sorted(all_cards, key=cmp_to_key(card_compare))
        #Check Ace
        if all_cards[-1].face == 1:
            return 1, all_cards[-1]
        return 1, all_cards[0]

    def __str__(self):
        return_str = ""
        if self.is_big_blind:
            return_str += "Big Blind\n"
        elif self.is_small_blind:
            return_str += "Small Blind\n"
        return_str += "Deck:\n"
        for curr_card in self.hand:
            return_str += str(curr_card) + "\n"
        return return_str
