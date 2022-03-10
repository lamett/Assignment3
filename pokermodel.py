"""
Assignment 2
author: Annabell Kießler, Davide Alpino
03.03.2022

Game logik, only QObject and pyqtSignal
"""
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from cardlib import *

class Blinds(enum.Enum):

    NO = 0
    SMALL = 1
    BIG = 2

class Player(QObject):

    def __init__(self, name, money, bet, hand, active_state: bool):
        super().__init__()
        self.name = name
        self.money = money
        self.bet = bet
        self.handCards = hand.cards  #cards with value and suit
        self.blind = Blinds.NO
        self.active_state = active_state

        # self.handCardItems = CardItemList(self.handCards)

    #def set_name_in_view(self):
     #   self.view.name_label.setText(self.name) #change in view

    def increase_money(self, value):
        self.money += value

        #self.view.money_label.setText(f"Money: {self.money}") #change in view

    def decrease_money(self, value):
        if self.money - value < 0:
            print("ERROR: Player doesnt have that amount of money")
        else:
            self.money -= value
            #self.view.money_label.setText(f"Money: {self.money}") #change in view

    def increase_bet(self, value):
        if value > self.money:
            print("ERROR: Player doesnt have enough money to bet that high")
        else:
            self.bet += value
            #self.view.bet_label.setText(f"Bet: {self.bet}")  # change in view

    def reset_bet(self):
        self.bet = 0

    def change_blind(self, blind: Blinds):
        self.blind = blind
        #self.view.blind_label.setText(f"Blind: {self.blind}")  # change in view

    def change_hand(self, hand):
        self.handCards = hand.list_cardItems
        #self.handCardItems = CardItemList(self.handCards)

    def setActive(self):
        self.active_state = True
        #self.handCardItems.openCard(0)
        #self.handCardItems.openCard(1)

    def setNotAktive(self):
        self.active_state = False
        #self.handCardItems.coverCard(0)
        #self.handCardItems.coverCard(1)

class Game(QObject):

    # signals
    refresh_players_view_signal = pyqtSignal()
    #show_player1_cards_signal = pyqtSignal()
    #show_player2_cards_signal = pyqtSignal()
    #show_tablecards_signal = pyqtSignal()
    #refresh_card_view_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.deck = self.init_Deck()
        self.pot = Pot()
        self.tablecards = self.init_Tablecards()
        self.player1, self.player2 = self.create_new_players()
        #self.active_player = self.player1       #mit function: get_active_player() aufrufen
        self.big_blind_value = 0        #default big_blind_value = 0
        self.small_blind_value = 0      #default small_blind_value = 0
        self.action = ""  #describes what action the player clicked (raise/call/check/fold)
        self.process_step = 1

        #self.set_active_player(self.player2)

    def init_Deck(self):
        deck = StandardDeck()
        deck.shuffle()
        return deck

    def init_Tablecards(self):
        tableCards = []
        for i in range(5):
            tableCards.append(self.deck.draw())
        return tableCards

    def create_Hand(self):
        hand = Hand()
        hand.add_card(self.deck.draw())
        hand.add_card(self.deck.draw())
        return hand

    def create_new_players(self):
        player1 = Player("Mafabi", 100, 0, self.create_Hand(), True)
        player2 = Player("Fabissimo", 100, 0, self.create_Hand(), False)
        return player1, player2

    def get_active_player(self):
        if self.player1.active_state:
            return self.player1
        return self.player2

    def get_not_active_player(self):
        if not self.player1.active_state:
            return self.player1
        return self.player2

    def set_next_player_active(self):
        previous_active_player = self.get_active_player()
        previous_not_active_player = self.get_not_active_player()

        previous_active_player.setNotAktive()
        previous_not_active_player.setActive()

        #if self.get_active_player() == self.player1:
            #self.show_player1_cards_signal.emit()
            #self.refresh_card_view_signal.emit()
        #else:
            #self.show_player2_cards_signal.emit()
            #self.refresh_card_view_signal.emit()

    def check_winner(self):
        if(self.player1.money == 0):
            return self.player2

        if(self.player2.money == 0):
            return self.player1
        else:
            return ""

    def raise_(self):
        player = self.get_active_player()
        player.increase_bet(1)
        self.set_next_player_active()
        self.refresh_players_view_signal.emit()

    def call_(self):
        player = self.get_active_player()
        highest_bet = self.get_highest_bet()
        player.increase_bet(highest_bet - player.bet)
        self.set_next_player_active()
        self.refresh_players_view_signal.emit()

    def check_(self):
        if self.get_active_player().bet == self.get_not_active_player().bet:
            self.set_next_player_active()
            self.refresh_players_view_signal.emit()

    def fold_(self):
        print(f"{self.get_not_active_player().name} wins round") # --> next round

    def get_highest_bet(self):
        if self.player1.bet >= self.player2.bet:
            return self.player1.bet
        return self.player2.bet

class Pot:
    def __init__(self):
        self.value = 0

    def raisePot(self, value):
        self.value += value

    def get_value(self):
        return self.value

    def reset_Pot(self):
        self.value = 0
