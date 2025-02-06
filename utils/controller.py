from deck import Card, Deck

class Player:
    def __init__(self):
        self.hand = []
        self.is_big_blind = False
        self.is_small_blind = False
        self.curr_bet = 0
        self.has_raised = False

    def add_card(self, card: Card):
        self.hand.append(card)

    def get_hand(self) -> list[Card]:
        return self.hand
    
    def clear(self):
        self.hand = []
        self.is_big_blind = False
        self.is_small_blind = False

    def set_curr_bet(self, bet: int):
        self.curr_bet = bet

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

class Controller:
    def __init__(self):
        self.players = []
        self.blinds = [0, 1] #First index is the big blind, second index is the small blind
        self.num_players = 0
        self.pot_amount = 0
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
    
    def _get_prev_player_index(self, i: int) -> int:
        prev_index = i - 1
        if prev_index == -1:
            return len(self.players) - 1
        return prev_index

    def init_players(self):
        """
        Sets the blinds per player based on global configuration
        Deals each player their cards
        """
        for i in range(2):
            for curr_player_index, curr_player in enumerate(self.players):
                if i == 0:
                    curr_player.clear()
                    #Set the blinds if applicable
                    if self.blinds[0] == curr_player_index:
                        curr_player.is_big_blind = True
                    elif self.blinds[1] == curr_player_index:
                        curr_player.is_small_blind = True
                drawn_card = self.deck.draw_card()
                curr_player.add_card(drawn_card)

    def move_blinds(self):
        new_big_blind = self._get_next_player_index(self.blinds[0])
        new_small_blind = self._get_next_player_index(self.blinds[1])
        self.blinds = [new_big_blind, new_small_blind]

    def display_hand_for_player(self, player_index: int):
        for curr_card in self.players[player_index].hand:
            print(curr_card)

    def accept_bets(self):
        #This accepts bets from all the players

        """
        for curr_player_index, curr_player in enumerate(self.players):
            self.display_hand_for_player(curr_player_index)
            curr_player_bet = int(input(f"Player {curr_player_index + 1} Bet: "))
            self.pot_amount += curr_player_bet
            curr_player.set_curr_bet(curr_player_bet)
        """

        curr_player_index = 0 #Curr player to ask bet from
        curr_bet_amount = 10 #The max amount that a person has bet
        last_player_to_bet = len(self.players) - 1

        while True:
            self.display_hand_for_player(curr_player_index)
            is_continue = True
            while is_continue:
                is_continue = False
                curr_player_bet = int(input(f"Player {curr_player_index + 1} Bet: "))
                total_bet_amount =  self.players[curr_player_index].curr_bet + curr_player_bet
                if total_bet_amount < curr_bet_amount:
                    #Error: Prompt them again
                    is_continue = True
                elif total_bet_amount == curr_bet_amount:
                    #Check
                    self.players[curr_player_index].curr_bet += curr_player_bet
                    self.pot_amount += curr_player_bet
                else:
                    #Raise
                    if self.players[curr_player_index].has_raised:
                        is_continue = True
                        continue
                    curr_bet_amount = total_bet_amount
                    self.players[curr_player_index].curr_bet += curr_player_bet
                    self.pot_amount += curr_player_bet
                    self.players[curr_player_index].has_raised = True
                    last_player_to_bet = self._get_prev_player_index(curr_player_index)

            if curr_player_index == last_player_to_bet:
                break
            curr_player_index = self._get_next_player_index(curr_player_index)





    def play_game(self):
        #This should start the game

        #Step 0: Ask for num players
        self.get_num_players()
        #Game Loop
        i = 0
        while i < 3:
            #Step 1: Initialize the Deck
            self.init_deck()

            #Step 2: Initialize Players
            self.init_players()

            #Step 3: Accept First Round of Bets
            self.accept_bets()

            """
            for curr_player in self.players:
                print(curr_player)
            """

            print(self.pot_amount)
            for curr_player in self.players:
                print(curr_player.curr_bet)

            #Step n: Move the blinds
            self.move_blinds()

            i += 1

if __name__ == "__main__":
    controller = Controller()

    controller.play_game()