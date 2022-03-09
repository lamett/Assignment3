"""
Assignment 2
author: Annabell Kießler, Davide Alpino
03.03.2022

GUI elements
"""

from PyQt5.QtSvg import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import cardlib

################################################################

class Window(QMainWindow):
    """ Sets hole window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Texas Holdem")
        #self.setStyleSheet("background-image:url(cards/table.png);")

        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)

        self.layout = QGridLayout()
        self.mainWidget.setLayout(self.layout)

    def addView(self, widget, column, row):
        self.layout.addWidget(widget, column, row)

class ButtonsView:

    def __init__(self, game):
        self.mainWidget = QWidget()
        self.layout = QHBoxLayout()
        self.game = game
                
        self.raiseButton = QPushButton("RAISE")
        self.callButton = QPushButton("CALL")
        self.checkButton = QPushButton("CHECK")
        self.foldButton = QPushButton("FOLD")

        #self.raiseButton.setAutoFillBackground(True)
        #self.raiseButton.setStyleSheet("background-color : rgb(101, 252, 129); border = none")

        self.layout.addWidget(self.raiseButton)
        self.layout.addWidget(self.callButton)
        self.layout.addWidget(self.checkButton)
        self.layout.addWidget(self.foldButton)

        self.mainWidget.setLayout(self.layout)

    def setActive(self, button):
        QPushButton.setDisabled(button, False)

    def setDisabled(self, button):
        QPushButton.setDisabled(button, True)

class Pot:
    def __init__(self, money):
        self.money = money

class PotView:
    def __init__(self, pot):
        self.mainWidget = QWidget()
        self.layout = QHBoxLayout()

        self.pot = pot
        self.money = QLabel(f"Pot: {pot.money}€")

        self.layout.addWidget(self.money)

        self.mainWidget.setLayout(self.layout)

    def refreshPot(self):
        self.money.setText(f"Pot: {self.pot.money}")

class PlayerProperties:
    def __init__(self, name, money, bet, hand, status):# status --> aktive or not
        self.name = name
        self.money = money
        self.bet = bet
        self.handcards = hand.cards     # list of cards
        self.card_item_list = CardItemList(self.handcards) #list of game items containing pics of cards
        self.status = status

    def setActive(self):
        self.status = True


class PlayerPropertiesView: #--> view won't need player
    def __init__(self, player):
        self.mainWidget = QWidget()
        self.layout = QVBoxLayout()
        self.player = player

        self.name = QLabel()
        self.money = QLabel()
        self.bet = QLabel()
        self.activeText = QLabel("active")
        self.activeText.setStyleSheet("background-color : red;")

        self.refreshView()
        self.refreshStatus()

        self.layout.addWidget(self.name)
        self.layout.addWidget(self.money)
        self.layout.addWidget(self.bet)
        self.layout.addWidget(self.activeText)

        self.mainWidget.setLayout(self.layout)

    def refreshView(self):
        self.name.setText(f"{self.player.name}")
        self.money.setText(f"Money: {self.player.money}")
        self.bet.setText(f"Bet: {self.player.bet}")

    def refreshStatus(self):
        if self.player.status:
            self.activeText.show()
        else:
            self.activeText.hide()

class CardItem(QGraphicsSvgItem):
    """ A simple overloaded QGraphicsSvgItem that also stores the card position """
    def __init__(self, card, position, status_open): #status--> open:TRUE or flipped:FAlSE
        super().__init__()
        self.card = card
        self.setSharedRenderer(CardRenderer(card, status_open).renderer)
        self.position = position
        self.status_open = status_open

    def changeStatus(self, status_open):
        self.status_open = status_open
        self.setSharedRenderer(CardRenderer(self.card, self.status_open).renderer)

class CardItemList():
    def __init__(self, cards):
        self.cards = []
        self.ini(cards)


    def ini(self, cards):
        for indices, card in enumerate(cards):
            carditem = CardItem(card, indices,False)
            self.cards.append(carditem)

class CardView:
    def __init__(self, cards):
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setGeometry(0, 0, 100, 110)
        self.cards = cards.cards

        for card in self.cards:
            card.setPos(card.position * 125, 0)
            self.scene.addItem(card)

    def addCardItem(self, card):
        self.cards.append(card)
        for card in self.cards:
            card.setPos(card.position * 125, 0)
            self.scene.addItem(card)

class CardRenderer:
    def __init__(self, card, status):

        self.dicValue = {11: "J",
                        12: "Q",
                        13: "K",
                        14: "A"}

        self.mappedsuit = card.suit.name[0]

        if card.value > 10:
            self.mappedvalue = self.dicValue[card.value]
        else:
            self.mappedvalue = card.value

        if status:
            self.open()
        else:
            self.flipped()

    def flipped(self):
        self.renderer = QSvgRenderer('cards/Red_Back_2.svg')

    def open(self):
        self.renderer = QSvgRenderer(f'cards/{str(self.mappedvalue) + self.mappedsuit}.svg')

def openCard(cardItemList, position): #position of card in ItemList
    cardItemList.cards[position].changeStatus(True)

def coverCard(cardItemList, position):
    cardItemList.cards[position].changeStatus(False)

#####################################################

qt_app = QApplication(sys.argv)
window = Window()

#####################################
deck = cardlib.StandardDeck()
deck.shuffle()

hand1 = cardlib.Hand()
hand2 = cardlib.Hand()

tableCards = []

hand1.add_card(deck.draw())
hand2.add_card(deck.draw())
hand1.add_card(deck.draw())
hand2.add_card(deck.draw())

for i in range(5):
    tableCards.append(deck.draw())

###################################
pot = Pot(0)

player1 = PlayerProperties("Fabilinski", 100, 0, hand1, True)
player2 = PlayerProperties("Mafabi", 100, 0, hand2, False)

tableCardsItemList = CardItemList(tableCards)

#open cards
for i in range(2):
    openCard(player1.card_item_list, i) ##can do same thing with close

for i in range(2):
    openCard(player2.card_item_list, i)

for i in range(3):
    openCard(tableCardsItemList, i)
####################################

cardview1 = CardView(player1.card_item_list)
cardview2 = CardView(player2.card_item_list)
cardviewtable = CardView(tableCardsItemList)
buttons1 = ButtonsView()
potView = PotView(pot)

window.addView(PlayerPropertiesView(player1).mainWidget, 1, 3)
window.addView(PlayerPropertiesView(player2).mainWidget, 1, 0)
window.addView(cardview1.view, 0, 0)
window.addView(cardview2.view, 0, 3)
window.addView(cardviewtable.view, 0, 1)
window.addView(buttons1.mainWidget, 3,1)
window.addView(potView.mainWidget, 1, 1)

window.show()
qt_app.exec_()
