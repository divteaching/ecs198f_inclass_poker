from utils.deck import Deck
from utils.player import Player

class Controller:
    def __init__(self):
        self.players: list[Player] = []
        self.blinds = [1, 0] #First index is the big blind, second index is the small blind
        self.num_players = 0
        self.pot_amount = 0
        self.blind_bets = [10, 5] #First index is the big blind bet amount, second index is the small blind bet amount
        self.opened_cards = []
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

    def resolve_init_value_for_bets(self, round_num: int) -> list[int, int]:
        if round_num == 1:
            big_blind_player = self.players[self.blinds[0]]
            small_blind_player = self.players[self.blinds[1]]
            big_blind_player.curr_bet += self.blind_bets[0] #Make the big blind bet
            small_blind_player.curr_bet += self.blind_bets[1] # Make the small blind bet

            player_index_after_small_blind = self._get_next_player_index(self.blinds[0])
            return [player_index_after_small_blind, self.blind_bets[0]]
        else:
            return [self.blinds[1], 0]

    def accept_bets(self, start_player_index: int, init_curr_bet_amount: int):
        #This accepts bets from all the players

        curr_player_index = start_player_index #Curr player to ask bet from
        curr_bet_amount = init_curr_bet_amount #The max amount that a person has bet
        last_player_to_bet = self._get_prev_player_index(start_player_index) 

        while True:
            is_continue = True
            while is_continue and not self.players[curr_player_index].has_folded:
                is_continue = False
                self.display_hand_for_player(curr_player_index)
                curr_player_bet = int(input(f"Player {curr_player_index + 1} Bet: "))
                total_bet_amount =  self.players[curr_player_index].curr_bet + curr_player_bet
                if total_bet_amount < 0:
                    #Fold
                    self.players[curr_player_index].has_folded = True
                elif total_bet_amount < curr_bet_amount:
                    #Error: Prompt them again
                    is_continue = True
                elif total_bet_amount == curr_bet_amount:
                    #Check
                    self.players[curr_player_index].curr_bet += curr_player_bet
                else:
                    #Raise
                    if self.players[curr_player_index].has_raised:
                        is_continue = True
                        continue
                    curr_bet_amount = total_bet_amount
                    self.players[curr_player_index].curr_bet += curr_player_bet
                    self.players[curr_player_index].has_raised = True
                    last_player_to_bet = self._get_prev_player_index(curr_player_index)

            if curr_player_index == last_player_to_bet:
                break
            curr_player_index = self._get_next_player_index(curr_player_index)

    def clear_bets_per_player(self):
        #Clear the bets that the players have made
        for curr_player in self.players:
            self.pot_amount += curr_player.curr_bet
            curr_player.curr_bet = 0
            curr_player.has_raised = False

    def open_common_cards(self, round_num: int):
        burn_card = self.deck.draw_card()
        num_cards_to_draw = 1
        if round_num == 1:
            #Flop
            num_cards_to_draw = 3

        for i in range(num_cards_to_draw):
            curr_card = self.deck.draw_card()
            self.opened_cards.append(curr_card)
    
    def display_common_cards(self):
        print("COMMON CARDS START")
        for curr_card in self.opened_cards:
            print(curr_card)
        print("COMMON CARDS END")

    def declare_winner(self):
        best = self.players[0].idenitfy_class_of_hand(self.opened_cards)
        best_player = 0
        for i in range(1, len(self.players), 1):
            curr_class = self.players[i].idenitfy_class_of_hand(self.opened_cards)
            if curr_class[0] == 1 and best[0] == 1:
                if curr_class[1].face > curr_class[1].face:
                    best = curr_class
                    best_player = i
                continue
            if curr_class[0] > best[0]:
                best = curr_class
                best_player = i
        
        print(f"Player {best_player + 1} wins ${self.pot_amount}!")
        self.pot_amount = 0

    def play_game(self):
        #This should start the game

        #Step 0: Ask for num players
        self.get_num_players()
        #Game Loop
        while True:
            #Step 1: Initialize the Deck
            self.init_deck()

            #Step 2: Initialize Players
            self.init_players()

            for round_num in range(1, 4, 1):
                #Step 3: Accept Bets
                bet_init_values = self.resolve_init_value_for_bets(round_num)
                self.accept_bets(bet_init_values[0], bet_init_values[1])
            
                #Clear bets
                self.clear_bets_per_player()

                #Step 4: Open common card(s) 
                self.open_common_cards(round_num)

                #Step 5: Display common cards
                self.display_common_cards()

            #Step 6: Declare the winner
            self.declare_winner()

            #Step 7: Move the blinds
            self.move_blinds()