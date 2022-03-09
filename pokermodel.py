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
from pokerview import *

class Blinds(enum.Enum):

    NO = 0
    SMALL = 1
    BIG = 2

class Game:
    def __init__(self):
        self.window = Window()
        self.deck = self.init_Deck()
        self.pot = Pot()
        self.tablecards = self.init_Tablecards()
        self.player1, self.player2 = self.create_new_players()
        self.active_player = self.player1       #default active_player = player1
        self.big_blind_value = 0        #default big_blind_value = 0
        self.small_blind_value = 0      #default small_blind_value = 0
        self.action = ""  #describes what action the player clicked (raise/call/check/fold)
        self.process_step = 1

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
        player1 = Player("Mafabi", 100, 0, self.create_Hand(), False)
        player2 = Player("Fabissimo", 100, 0, self.create_Hand(), False)
        return player1, player2

    def set_active_player(self, player):
        self.active_player.setNotAktive()   #sets previous player notaktive
        player.setActive()      #sets next active player active
        self.active_player = player     #sets player as active_player

    def check_winner(self):
        if(self.player1.money == 0):
            return self.player2

        if(self.player2.money == 0):
            return self.player1
        else:
            return ""

 # gets a string [raise, call, check, fold] it takes different action for every case
    def action(self, action):
        if(action == "raise"):
            return ""
        if(action == "call"):
            print("call")
            return ""
        if(action == "check"):
            self.active_player.check_state = True

            if(self.player1.check_state == True & self.player2.check_state == True): # -> go to round two # würde ich hier nicht direkt aufrufen
                if(self.process_step == 1):
                    card1 = self.draw_card()
                    card2 = self.draw_card()
                    card3 = self.draw_card()
                    self.tablecards.append([card1,card2,card3]) #TODO: list could make an error
            return ""
        if(action == "fold"):
            return ""

        return "ERROR: Wrong action"
    # takes all steps to start the next turn
###################################################################################################################
class Player:

    def __init__(self, name, money, bet, hand, active_state: bool):
        self.name = name
        self.money = money
        self.bet = bet
        self.handCards = hand.cards
        self.handCardItems = CardItemList(self.handCards)
        self.blind = Blinds.NO
        self.active_state = active_state
        self.view = self.initView()

    #def initView(self):
    def initView(self):
        return PlayerView()

    def set_name_in_view(self):
        self.view.name_label.setText(self.name) #change in view

    def increase_money(self, value):
        self.money += value
        self.view.money_label.setText(f"Money: {self.money}") #change in view

    def decrease_money(self, value):
        if self.money - value < 0:
            print("ERROR: Player doesnt have that amount of money")
        else:
            self.money -= value
            self.view.money_label.setText(f"Money: {self.money}") #change in view

    def increase_bet(self, value):
        if value > self.money:
            print("ERROR: Player doesnt have enough money to bet that high")
        else:
            self.bet += value
            self.view.bet_label.setText(f"Bet: {self.bet}")  # change in view

    def change_blind(self, blind: Blinds):
        self.blind = blind
        self.view.blind_label.setText(f"Blind: {self.blind}")  # change in view

    def change_hand(self, hand):
        self.handCards = hand.cards
        self.handCardItems = CardItemList(self.handCards)

    def setActive(self):
        self.active_state = True
        self.handCardItems.openCard(0)
        self.handCardItems.openCard(1)

    def setNotAktive(self):
        self.active_state = False
        self.handCardItems.coverCard(0)
        self.handCardItems.coverCard(1)

class Pot:
    def __init__(self):
        self.value = 0

    def raisePot(self, value):
        self.value += value

    def get_value(self):
        return self.value

    def reset_Pot(self):
        self.value = 0
