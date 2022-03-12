"""
Assignment 2
author: Annabell Kießler, Davide Alpino
03.03.2022

Game logik, only QObject and pyqtSignal

game => beginns with even player properties, ends when one player has zero money.
match => [0-00], beginns with players getting new cards, ends when the pot was won by one player
round => [0-4], beginns with opening tablecards, end when all players checked
"""
from PyQt5.QtCore import *
from cardlib import *

class Player(QObject):

    def __init__(self, name, money, bet, hand, active_state: bool):
        super().__init__()
        self.name = name
        self.money = money
        self.bet = bet
        self.hand = hand
        self.handCards = self.hand.cards  # cards with value and suit
        self.active_state = active_state

    def increase_money(self, value):
        self.money += value

    def decrease_money(self, value):
        if self.money - value < 0:
            print("ERROR: Player doesnt have that amount of money")
        else:
            self.money -= value

    def increase_bet(self, value):
        if value > self.money:
            print("ERROR: Player doesnt have enough money to bet that high")
        else:
            self.bet += value

    def reset_bet(self):
        self.bet = 0

    def change_hand(self, hand):
        self.hand = hand
        self.handCards = self.hand.cards

class Game(QObject):
    # signals
    refresh_players_view_signal = pyqtSignal()
    refresh_card_view_signal = pyqtSignal()
    refresh_pot_view_signal = pyqtSignal()

    show_player1_cards_signal = pyqtSignal()
    cover_player1_cards_signal = pyqtSignal()
    show_player2_cards_signal = pyqtSignal()
    cover_player2_cards_signal = pyqtSignal()

    trigger_tie_message = pyqtSignal()
    trigger_game_winner_message_signal = pyqtSignal()
    trigger_match_winner_message_signal = pyqtSignal()
    trigger_fold_winner_message_signal = pyqtSignal()

    raise_error_msg_signal = pyqtSignal()
    check_error_msg_signal = pyqtSignal()

    cover_tablecards_signal = pyqtSignal()
    show_first3_cards_signal = pyqtSignal()
    show_fourth_card_signal = pyqtSignal()
    show_fifth_card_signal = pyqtSignal()

    enable_next_button_signal = pyqtSignal()
    disable_next_button_signal = pyqtSignal()

    enable_buttons_signal = pyqtSignal()
    disable_buttons_signal = pyqtSignal()

    change_cards_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.deck = self.init_Deck()
        self.pot = Pot()
        self.tableCards = self.init_Tablecards()
        self.player1, self.player2 = self.create_new_players(100, 100)

        self.winner = None

        self.match_number = 0
        self.round_number = 0
        self.check_count = 0

    #initialize Game
    def init_Deck(self):
        deck = StandardDeck()
        deck.shuffle()
        return deck

    def init_Tablecards(self):
        cards = []
        for i in range(5):
            cards.append(self.deck.draw())
        return cards

    def create_Hand(self):
        hand = Hand()
        hand.add_card(self.deck.draw())
        hand.add_card(self.deck.draw())
        return hand

    def create_new_players(self, player_money1, player_money2):
        player1 = Player("Player1", player_money1, 0, self.create_Hand(), True)
        player2 = Player("Player2", player_money2, 0, self.create_Hand(), False)
        return player1, player2

    #gameState
    def reset_match_number(self):
        self.match_number = 0

    def reset_round_number(self):
        self.round_number = 0

    def reset_check_count(self):
        self.check_count = 0

    def increase_check_count(self, value):
        self.check_count += value
        if self.check_count == 2:
            self.reset_check_count()
            self.next_round()

    def next_round(self):
        self.round_number += 1
        if self.round_number <= 3:
            self.pot.raisePot(self.player1.bet + self.player2.bet)
            self.player1.decrease_money(self.player1.bet)
            self.player2.decrease_money(self.player2.bet)
            self.player1.reset_bet()
            self.player2.reset_bet()
            self.refresh_players_view_signal.emit()
            self.refresh_pot_view_signal.emit()

            if self.round_number == 1:
                self.show_first3_cards_signal.emit()
            if self.round_number == 2:
                self.show_fourth_card_signal.emit()
            if self.round_number == 3:
                self.show_fifth_card_signal.emit()

        if self.round_number == 4:

            self.show_player1_cards_signal.emit()
            self.show_player2_cards_signal.emit()
            self.refresh_players_view_signal.emit()

            self.winner = self.compare_PokerHands()

            if self.winner != None:
                self.winner.increase_money(self.pot.value)
                self.trigger_match_winner_message_signal.emit()   #change to match-winner-msg

            if self.winner == None:
                self.player1.increase_money(int(self.pot.value/2))
                self.player2.increase_money(int(self.pot.value/2))
                self.trigger_tie_message.emit()

            self.refresh_players_view_signal.emit()
            self.enable_next_button_signal.emit()
            self.disable_buttons_signal.emit()

    def next_match(self):
        if not self.check_winner():
            self.disable_next_button_signal.emit()
            self.enable_buttons_signal.emit()
            self.match_number += 1
            self.reset_round_number()
            self.reset_check_count()

            self.deck = self.init_Deck()

            self.pot.reset_Pot()
            self.refresh_pot_view_signal.emit()

            self.tableCards = self.init_Tablecards()

            self.player1.change_hand(self.create_Hand())
            self.player2.change_hand(self.create_Hand())

            self.change_cards_signal.emit()

            self.cover_tablecards_signal.emit()

            self.set_next_player_active()
            self.refresh_card_view_signal.emit()


    #active_player_handling
    def set_next_player_active(self):
        if (self.player1.active_state):
            self.player1.active_state = False
            self.player2.active_state = True
            self.show_player2_cards_signal.emit()
            self.cover_player1_cards_signal.emit()
        else:
            self.player1.active_state = True
            self.player2.active_state = False
            self.show_player1_cards_signal.emit()
            self.cover_player2_cards_signal.emit()

        self.refresh_players_view_signal.emit()

    def get_active_player(self):
        if self.player1.active_state:
            return self.player1
        else:
            return self.player2

    def get_not_active_player(self):
        if not self.player1.active_state:
            return self.player1
        return self.player2

    #buttons
    def raise_(self, bet_string):

        bet = int(bet_string)
        player_active = self.get_active_player()
        player_not_active = self.get_not_active_player()

        if bet <= (player_active.money + player_active.bet): #check if enough money
            if (player_active.bet + bet) == player_not_active.bet:  #check if raise == call
                self.call_()
            else:
                player_active.increase_bet(bet)
                self.reset_check_count()
                self.set_next_player_active()
                self.refresh_players_view_signal.emit()
        else:
            self.raise_error_msg_signal.emit()

    def call_(self):
        player_active = self.get_active_player()
        player_not_active = self.get_not_active_player()

        if player_active.bet == player_not_active.bet:
            self.check_()
        else:
            player_active.increase_bet(player_not_active.bet - player_active.bet)
            self.increase_check_count(2)
            self.set_next_player_active()
            self.refresh_players_view_signal.emit()

    def check_(self):
        if self.player1.bet == self.player2.bet:
            self.set_next_player_active()
            self.increase_check_count(1)
        else:
            self.check_error_msg_signal.emit()

    def fold_(self):
        self.winner = self.get_not_active_player()
        self.winner.increase_money(self.pot.value)
        self.trigger_fold_winner_message_signal.emit()
        self.refresh_players_view_signal.emit()

        self.enable_next_button_signal.emit()
        self.disable_buttons_signal.emit()

    def compare_PokerHands(self):
        pokerHand1 = self.player1.hand.best_poker_hand(self.tableCards)
        pokerHand2 = self.player2.hand.best_poker_hand(self.tableCards)

        if pokerHand1 < pokerHand2:
            return self.player2
        if pokerHand2 < pokerHand1:
            return self.player1

        return None

    def get_winner(self):
        return self.winner

    def get_winning_handtype(self):
        return self.winner.hand.best_poker_hand(self.tableCards).handtype.name

    def check_winner(self):
        if (self.player1.money == 0):
            self.winner = self.player2
            self.trigger_game_winner_message_signal.emit()
            return True
        if (self.player2.money == 0):
            self.winner = self.player1
            self.trigger_game_winner_message_signal.emit()
            return True

        return False

class Pot:
    def __init__(self):
        self.value = 0

    def raisePot(self, value):
        self.value += value

    def get_value(self):
        return self.value

    def reset_Pot(self):
        self.value = 0
