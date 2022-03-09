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



class Game:

    def __init__(self):
        self.tablecards = []
        self.action = ""  #describes what action the player clicked (raise/call/check/fold)
        self.process_step = 1



    def set_active_player(self,player):
        self.active_player = player

    def create_new_players(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def set_blinds(self,small_blind, big_blind):
        self.small_blind = small_blind
        self.big_blind = big_blind

    def set_pot(self, value):
        self.pot = value

    def add_card_to_tablecards(self, card):
        self.tablecards.append(card)

    def check_winner(self):
        if(self.player1.money == 0):
            return self.player2

        elif(self.player2.money == 0):
            return self.player1
        else:
            return ""

    def init_deck(self):
        self.deck = StandardDeck()
        self.deck.shuffle()

    def init_player_hands(self):


        hand1 = Hand()
        hand2 = Hand()

        hand1.add_card(self.deck.draw())
        hand2.add_card(self.deck.draw())
        hand1.add_card(self.deck.draw())
        hand2.add_card(self.deck.draw())

        return hand1, hand2

    def set_players(self, player1, player2):
        self.player1 = player1
        self.player2 = player2


    def draw_card(self):
       return self.deck.draw()

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

    def __init__(self,money):
        self.money = money

    def increase_money(self, value):
        self.money += value

    def decrease_money(self,value):
        if(self.money - value < 0):
            print("ERROR: Player doesnt have that amount of money")
        else:
            self.money -= value

    def add_pokerhand(self, pokerhand):
        self.pokerhand = pokerhand
"""
class Pot():
    def __init__(self, value):
        self.value =value

    def raisePot(self,value):
        self.value += value

    def getPot(self):
        return self.value
"""
