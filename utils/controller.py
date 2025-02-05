from deck import Card, Deck

class Player:
    def __init__(self):
        self.hand = []
        self.is_big_blind = False
        self.is_small_blind = False

    def add_card(self, card: Card):
        self.hand.append(card)

    def get_hand(self) -> list[Card]:
        return self.hand
    
    def clear_hand(self):
        self.hand = []

class Controller:
    def __init__(self):
        self.players = []
        self.num_players = 0
        self.deck = None

    def get_num_players(self):
        num_players = 0
        while num_players < 3 or num_players > 22:
            num_players = int(input("How many people are playing? "))
        self.num_players = num_players

        self.players = []
        for i in range(self.num_players):
            curr_player = Player()
            self.players.append(curr_player)


    def init_deck(self):
        self.deck = Deck()
        self.deck.shuffle()

    def _get_next_player_index(self, i: int) -> int:
        return (i + 1) % self.num_players

    def init_players(self):
        is_set_small_blind = False
        is_set_big_blind = False
        for i in range(2):
            for curr_player_index, curr_player in enumerate(self.players):
                if i == 0:
                    curr_player.clear_hand()
                    if is_set_small_blind is False and curr_player.is_small_blind:
                        next_player_index = self._get_next_player_index(curr_player_index)
                        self.players[next_player_index].is_small_blind = True
                        curr_player.is_small_blind = False
                        is_set_small_blind = True
                    if is_set_big_blind is False and curr_player.is_big_blind:
                        next_player_index = self._get_next_player_index(curr_player_index)
                        self.players[next_player_index].is_big_blind = True
                        curr_player.is_big_blind = False
                        is_set_big_blind = True
                drawn_card = self.deck.draw_card()
                curr_player.add_card(drawn_card)

    def play_game(self):
        #This should start the game

        #Step 0: Ask for num players
        self.get_num_players()
        #Game Loop
        i = 0
        while i < 2:
            #Step 1: Initialize the Deck
            self.init_deck()

            #Step 2: Initialize Players
            self.init_players()

if __name__ == "__main__":
    controller = Controller()

    controller.play_game()