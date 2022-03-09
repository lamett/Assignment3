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

class Game:

    def __init__(self):
        self.tablecards = self.init_Tablecards
        self.pot = self.init_Pot()
        self.deck = self.init_Deck()
        self.player1, self.player2 = self.create_new_players()
        self.active_player = self.player1
        self.big_blind_value = 0
        self.small_blind_value = 0
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

    def init_Pot(self):
        return Pot()

    def create_Hand(self):

        hand = Hand()
        hand1.add_card(self.deck.draw())
        hand1.add_card(self.deck.draw())
        return hand

    def create_new_players(self):
        player1 = Player("Mafabi", 100, 0, self.create_Hand(), Blinds.NO, False)
        player2 = Player("Fabissimo", 100, 0, self.create_Hand(), Blinds.NO, False)
        return player1, player2

    def set_active_player(self, player):
        self.active_player = player

    def check_winner(self):
        if(self.player1.money == 0):
            return self.player2

        elif(self.player2.money == 0):
            return self.player1
        else:
            return ""

 # gets a string [raise, call, check, fold] it takes different action for every case
    def action(self, action):
        if(action == "raise"):
            return ""
        elif(action == "call"):
            print("call")
            return ""
        elif(action == "check"):
            self.active_player.check_state = True

            if(self.player1.check_state == True & self.player2.check_state == True):
                if(self.process_step == 1):
                    card1 = self.draw_card()
                    card2 = self.draw_card()
                    card3 = self.draw_card()
                    self.tablecards.append([card1,card2,card3]) #TODO: list could make an error
            return ""
        elif(action == "fold"):
            return ""
        else:
            return "ERROR: Wrong action"
    # takes all steps to start the next turn

class Player():

    def __init__(self, name, money, bet, hand, blind, active_state: bool):
        self.name = name
        self.money = money
        self.bet = bet
        self.handCards = hand.cards
        self.handCardItems = CardItemList(self.handCards)
        self.blind = none
        self.active_state = active_state
        self.view = self.initView()

    #def initView(self):

    def increase_money(self, value):
        self.money += value

    def decrease_money(self, value):
        if(self.money - value < 0):
            print("ERROR: Player doesnt have that amount of money")
        else:
            self.money -= value

    def change_hand(self, hand):
        self.handCards = hand.cards
        self.handCardItems = CardItemList(self.handCards)

    def change_Blind(self, blind: Blinds):
        self.blind = blind

class Pot():
    def __init__(self):
        self.value = 0

    def raisePot(self, value):
        self.value += value

    def get_value(self):
        return self.value

    def reset_Pot(self):
        self.value = 0

class Blinds(enum.Enum):

    NO = 0
    SMALL = 1
    BIG = 2
