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

class Pot:
    """
    Class Pot: represents the Pot of the game where the actual bet of both players is stored
    """

    def __init__(self):
        self.value = 0

    def raise_pot(self, value):
        self.value += value

    def get_value(self):
        return self.value

    def reset_pot(self):
        self.value = 0

class Player(QObject):
    """
    Class Player: represents a Player with his attributes and methods to change them
    """
    #connect refresh signal
    refresh_player_view = pyqtSignal()

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
        self.handCards = hand.cards  # cards with value and suit
        self.active_state = active_state

    def increase_money(self, value):
        self.money += value

    def decrease_money(self, value):
        self.money -= value

    def increase_bet(self, value):
        self.bet += value

    def reset_bet(self):
        self.bet = 0

class Game(QObject):
    """
    Class Game: represents the whole game logic of a game
    Attributes: deck: StandardDeck(), pot: Pot(), tableCards: [],
    players : List of Player(), winner: Player(), match_number: int,
    round_number: int, check_count: int
    """

    # refresh the table view
    refresh_table_view = pyqtSignal()

    # gives out error and game state messages
    game_state_message = pyqtSignal(str)

    # signals for buttons to enable/disable
    change_button_state = pyqtSignal(str)

    def __init__(self):

        super().__init__()

        self.deck = self.init_deck()
        self.pot = Pot()
        self.tableCards = self.init_tablecards()

        player_name = ["Player1", "Player2"]    # default player names
        self.players = []
        for name in player_name:
            self.players.append(Player(name, 100, 0, self.create_hand(), False))    # player money at the beginning: 100

        self.players[0].active_state = True

        self.winner = None

        self.match_number = 0
        self.round_number = 0
        self.check_count = 0

    #init
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

    #gameState
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

        for player in self.players:
            self.pot.raise_pot(player.bet)
            player.decrease_money(player.bet)
            player.reset_bet()

        for player in self.players: player.refresh_player_view.emit()

        if self.round_number == 1:
            self.refresh_table_view.emit()

        if self.round_number == 2:
            self.refresh_table_view.emit()
            self.game_state_message.emit("Test")

        if self.round_number == 3:
            self.refresh_table_view.emit()

        if self.round_number == 4:
            for player in self.players:
                player.active_state = True

            for player in self.players: player.refresh_player_view.emit()

            self.winner = self.compare_pokerhands()

            if self.winner != None:
                self.winner.increase_money(self.pot.value)
                self.game_state_message.emit("match_winner")

            if self.winner == None:
                for player in self.players:
                    player.increase_money(int(self.pot.value / 2))

                self.game_state_message.emit("tie")

            for player in self.players: player.refresh_player_view.emit()

            self.change_button_state.emit("enable_next_button")


    def next_match(self):
        """
        starts a new match if the actual round has ended and there isnt a game_winner
        """
        if not self.check_winner():
            self.change_button_state.emit("disable_next_button")
            self.match_number += 1
            self.reset_round_number()
            self.reset_check_count()

            self.deck = self.init_deck()

            self.pot.reset_pot()
            self.tableCards = self.init_tablecards()
            self.refresh_table_view.emit()

            for player in self.players:
                player.hand = self.create_hand()
                player.handCards = player.hand.cards

            self.players[0].active_state = True #könnte man noch eleganter lösen aber ist glaube egal
            self.players[1].active_state = False

            for player in self.players: player.refresh_player_view.emit()

    # active_player_handling
    def set_next_player_active(self):
        """
        sets the next player active and sends the signal to open and cover the certain cards
        """
        for index, player in enumerate(self.players):
            if player.active_state:
                player.active_state = False
                if index != len(self.players)-1:
                    self.players[index+1].active_state = True
                else:
                    self.players[0].active_state = True
                break

        for player in self.players: player.refresh_player_view.emit()

    def get_active_player(self):
        """
        returns current active player
        """
        for player in self.players:
            if player.active_state:
                return player

        return None

    def get_not_active_player(self):
        """
        returns player behind current active player
        """
        for index, player in enumerate(self.players):
            if player.active_state:
                if index != len(self.players)-1:
                    return self.players[index+1]
                else:
                    return self.players[0]

        return None

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

        else:
            self.game_state_message.emit("raise_error")

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

    def check_(self):
        """
        implements the logic of the check button, if both player checked the next round will start
        """
        high_bet = 0
        for player in self.players:
            if player.bet > high_bet:
                high_bet = player.bet

        active_player = self.get_active_player()

        if active_player.bet == high_bet:
            self.set_next_player_active()
            self.increase_check_count(1)
        else:
            self.game_state_message.emit("check_error")

    def fold_(self):
        """
        implements the logic of the fold button, adds the pot to the other active player and enable the
        next button to start a new round
        """
        for player in self.players:
            self.pot.raise_pot(player.bet)
            player.decrease_money(player.bet)
            player.reset_bet()

        for player in self.players: player.refresh_player_view.emit()
        self.refresh_table_view.emit()

        self.winner = self.get_not_active_player()
        self.winner.increase_money(self.pot.value)
        self.game_state_message.emit("fold_winner")

        for player in self.players: player.refresh_player_view.emit()

        self.change_button_state.emit("enable_next_button")

    # calculate winner
    def compare_pokerhands(self):
        """
        compare the hands of both players combined with the tablecards to see which player has won the round
        @return: the player with the best poker hand
        """
        pokerhands = dict()

        for player in self.players:
            pokerhands[player] = player.hand.best_poker_hand(self.tableCards)

        pokerhands_sort = sorted(pokerhands.items(), key=lambda item: item[1], reverse=True)

        if pokerhands_sort[0][1] == pokerhands_sort[1][1]:
            return None
        else:
            return pokerhands_sort[0][0]

    def get_winner(self):
        return self.winner

    def get_winning_handtype(self):
        return self.winner.hand.best_poker_hand(self.tableCards).handtype.name

    def check_winner(self):
        """
        Checks if there is a winner of the whole game and in that case emits a winning message
        @return: True if there is a winner and the game is over, else: False
        """
        players_copy = self.players.copy()

        players_copy.sort(key=lambda player: player.money, reverse=True)

        if players_copy[1].money == 0:
            self.winner = players_copy[0]
            return True

        return False
