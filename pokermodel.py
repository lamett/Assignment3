"""
Assignment 3
author: Annabell Kießler, Davide Alpino
03.03.2022

Game logik, only QObject and pyqtSignal

terms:
game => beginns with even player properties, ends when one player has zero money.
match => beginns with players getting new cards, ends when the pot got won by one player
round => [0-4], beginns with opening tablecards, end when all players checked
"""
from PyQt5.QtCore import *
from cardlib import *


class Player(QObject):
    """
        Class Player: represents a Player with his attributes and methods to change them
    """

    def __init__(self, name, money, bet, hand, active_state: bool):
        """

        @param name: the name of the player
        @param money: the money of the player
        @param bet: the bet he is taking in the actual phase
        @param hand: the hand cards of the player
        @param active_state: true: if the player is active and the cards are shown, false: if the player is not active and the cards are covered
        """
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
        self.money -= value

    def increase_bet(self, value):
        self.bet += value

    def reset_bet(self):
        self.bet = 0

    def change_hand(self, hand):
        """
        changes the hand cards of the player for the next round
        @param hand: the new hand cards
        """
        self.hand = hand
        self.handCards = self.hand.cards


class Game(QObject):
    """
        Class Game: represents the whole game logic of a game
        Attributes: deck: StandardDeck(), pot: Pot(), tableCards: [],
        player1 : Player(), player2: Player(), winner: Player(), match_number: int,
        round_number: int, check_count: int
    """

    # Refresh signals to refresh the views
    refresh_players_view = pyqtSignal()
    refresh_card_view = pyqtSignal()
    refresh_pot_view = pyqtSignal()

    # Signals to show and cover cards
    show_player1_cards = pyqtSignal()
    cover_player1_cards = pyqtSignal()
    show_player2_cards = pyqtSignal()
    cover_player2_cards = pyqtSignal()

    # Signals to show messages
    trigger_tie_message = pyqtSignal()
    trigger_game_winner_message = pyqtSignal()
    trigger_match_winner_message = pyqtSignal()
    trigger_fold_winner_message = pyqtSignal()

    # Signals for error messages
    raise_error_msg = pyqtSignal()
    check_error_msg = pyqtSignal()

    # Signals to show/cover tablecards
    cover_tablecards = pyqtSignal()
    show_first3_cards = pyqtSignal()
    show_fourth_card = pyqtSignal()
    show_fifth_card = pyqtSignal()

    # Signals to enable/disable button for the next round
    enable_next_button = pyqtSignal()
    disable_next_button = pyqtSignal()

    # Signals to enable/disable buttons
    enable_buttons = pyqtSignal()
    disable_buttons = pyqtSignal()

    # Signal to change the cards
    change_cards = pyqtSignal()

    def __init__(self):

        super().__init__()

        self.deck = self.init_deck()
        self.pot = Pot()
        self.tableCards = self.init_tablecards()
        self.player1, self.player2 = self.create_new_players(100, 100)

        self.winner = None

        self.match_number = 0
        self.round_number = 0
        self.check_count = 0

    def init_deck(self):
        """
        Initalizes a new Deck and shuffles it
        @return: the new Deck
        """
        deck = StandardDeck()
        deck.shuffle()
        return deck

    def init_tablecards(self):
        """
        method to init the 5 tablecards for a game round
        @return: the 5 tablecards
        """
        cards = []
        for i in range(5):
            cards.append(self.deck.draw())
        return cards

    def create_hand(self):
        """
        creats a hand from current deck
        @return: Hand() with two PlayingCards
        """
        hand = Hand()
        hand.add_card(self.deck.draw())
        hand.add_card(self.deck.draw())
        return hand

    def create_new_players(self, player_money1, player_money2):
        """
        This method create 2 new players, one active and one passive
        @param player_money1: money of player 1
        @param player_money2: money of player2
        @return: two Player()
        """
        player1 = Player("Player1", player_money1, 0, self.create_hand(), True)
        player2 = Player("Player2", player_money2, 0, self.create_hand(), False)
        return player1, player2

    # gameState
    def reset_match_number(self):
        self.match_number = 0

    def reset_round_number(self):
        self.round_number = 0

    def reset_check_count(self):
        self.check_count = 0

    def increase_check_count(self, value):
        """
        help method to increase the counter, that know how many times a check occured so we can in the
        case of 2 checks go on to the next step of tha actual round
        @param value: value to add to the check_count
        """
        self.check_count += value
        if self.check_count == 2:
            self.reset_check_count()
            self.next_round()

    def next_round(self):
        """
        logic to go on to the next round, depending on what step we are in right now
        different signals will be triggered to show now cards, test if somebody has won and more
        """
        self.round_number += 1

        self.pot.raise_pot(self.player1.bet + self.player2.bet)
        self.player1.decrease_money(self.player1.bet)
        self.player2.decrease_money(self.player2.bet)
        self.player1.reset_bet()
        self.player2.reset_bet()
        self.refresh_players_view.emit()
        self.refresh_pot_view.emit()

        if self.round_number == 1:
            self.show_first3_cards.emit()

        if self.round_number == 2:
            self.show_fourth_card.emit()

        if self.round_number == 3:
            self.show_fifth_card.emit()

        if self.round_number == 4:

            self.show_player1_cards.emit()
            self.show_player2_cards.emit()
            self.refresh_players_view.emit()

            self.winner = self.compare_pokerhands()

            if self.winner != None:
                self.winner.increase_money(self.pot.value)
                self.trigger_match_winner_message.emit()

            if self.winner == None:
                self.player1.increase_money(int(self.pot.value / 2))
                self.player2.increase_money(int(self.pot.value / 2))
                self.trigger_tie_message.emit()

            self.refresh_players_view.emit()
            self.enable_next_button.emit()
            self.disable_buttons.emit()

    def next_match(self):
        """
        starts a new match if the actual round has ended and there isnt a game_winner
        """
        if not self.check_winner():
            self.disable_next_button.emit()
            self.enable_buttons.emit()
            self.match_number += 1
            self.reset_round_number()
            self.reset_check_count()

            self.deck = self.init_deck()

            self.pot.reset_pot()
            self.refresh_pot_view.emit()

            self.tableCards = self.init_tablecards()

            self.player1.change_hand(self.create_hand())
            self.player2.change_hand(self.create_hand())

            self.change_cards.emit()

            self.cover_tablecards.emit()

            self.set_next_player_active()
            self.refresh_card_view.emit()

    # active_player_handling
    def set_next_player_active(self):
        """
        sets the next player active and sends the signal to open and cover the certain cards
        """
        if self.player1.active_state:
            self.player1.active_state = False
            self.player2.active_state = True
            self.show_player2_cards.emit()
            self.cover_player1_cards.emit()
        else:
            self.player1.active_state = True
            self.player2.active_state = False
            self.show_player1_cards.emit()
            self.cover_player2_cards.emit()

        self.refresh_players_view.emit()

    def get_active_player(self):
        if self.player1.active_state:
            return self.player1
        else:
            return self.player2

    def get_not_active_player(self):
        if not self.player1.active_state:
            return self.player1
        return self.player2

    # buttons
    def raise_(self, bet_string):
        """
        logic behind raise button, increases the actual bet if all necessary conditions are met
        @param bet_string: the amount the player wants to bet
        """
        bet = int(bet_string)
        player_active = self.get_active_player()
        player_not_active = self.get_not_active_player()

        if bet <= (player_active.money + player_active.bet):  # check if enough money
            if (player_active.bet + bet) == player_not_active.bet:  # check if raise == call
                self.call_()
            else:
                player_active.increase_bet(bet)
                self.reset_check_count()
                self.set_next_player_active()
                self.refresh_players_view.emit()
        else:
            self.raise_error_msg.emit()

    def call_(self):
        """
        implements the logic of the call button, to accept the bet the other player bets and move on to the next round
        """
        player_active = self.get_active_player()
        player_not_active = self.get_not_active_player()

        if player_active.bet == player_not_active.bet:
            self.check_()
        else:
            player_active.increase_bet(player_not_active.bet - player_active.bet)
            self.increase_check_count(2)
            self.set_next_player_active()
            self.refresh_players_view.emit()

    def check_(self):
        """
        implements the logic of the check button, if both player checked the next round will start
        """
        if self.player1.bet == self.player2.bet:
            self.set_next_player_active()
            self.increase_check_count(1)
        else:
            self.check_error_msg.emit()

    def fold_(self):
        """
        implements the logic of the fold button, adds the pot to the other active player and enable the
        next button to start a new round
        """
        self.pot.raise_pot(self.player1.bet + self.player2.bet)
        self.player1.decrease_money(self.player1.bet)
        self.player2.decrease_money(self.player2.bet)
        self.player1.reset_bet()
        self.player2.reset_bet()

        self.refresh_players_view.emit()
        self.refresh_pot_view.emit()

        self.winner = self.get_not_active_player()
        self.winner.increase_money(self.pot.value)
        self.trigger_fold_winner_message.emit()

        self.refresh_players_view.emit()

        self.enable_next_button.emit()
        self.disable_buttons.emit()

    def compare_pokerhands(self):
        """
        compare the hands of both players combined with the tablecards to see which player has won the round
        @return: the player with the best poker hand
        """
        poker_hand1 = self.player1.hand.best_poker_hand(self.tableCards)
        poker_hand2 = self.player2.hand.best_poker_hand(self.tableCards)

        if poker_hand1 < poker_hand2:
            return self.player2
        if poker_hand2 < poker_hand1:
            return self.player1

        return None

    def get_winner(self):
        return self.winner

    def get_winning_handtype(self):
        return self.winner.hand.best_poker_hand(self.tableCards).handtype.name

    def check_winner(self):
        """
        Checks if there is a winner of the whole game and in that cas emits a winning message
        @return: True if there is a winner and the game is over else false
        """
        if self.player1.money == 0:
            self.winner = self.player2
            self.trigger_game_winner_message.emit()
            return True
        if self.player2.money == 0:
            self.winner = self.player1
            self.trigger_game_winner_message.emit()
            return True

        return False


class Pot:
    """
    class Pot: represents the Pot of the game where the actual bet of both players is stored
    """

    def __init__(self):
        self.value = 0

    def raise_pot(self, value):
        self.value += value

    def get_value(self):
        return self.value

    def reset_pot(self):
        self.value = 0
