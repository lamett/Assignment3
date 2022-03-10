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
from pokermodel import *

################################################################

#window
class Window(QMainWindow):
    """
    Class Window: Sets window
    """
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

#cards
class CardRenderer:
    """
    Class CardRenderer: Gets Image depending on card value and suit and depending on the state if the card is flipped or open.
    """

    def __init__(self, card: PlayingCard, status):

        self.dicValue = {11: "J",
                        12: "Q",
                        13: "K",
                        14: "A"}

        self.mappedsuit = card.suit.name[0]

        if card.get_value() > 10:
            self.mappedvalue = self.dicValue[card.get_value()]
        else:
            self.mappedvalue = card.get_value()

        if status:
            self.open()
        else:
            self.flipped()

    def flipped(self):
        self.renderer = QSvgRenderer('cards/Red_Back_2.svg')

    def open(self):
        self.renderer = QSvgRenderer(f'cards/{str(self.mappedvalue) + self.mappedsuit}.svg')

class CardItem(QGraphicsSvgItem):
    """
    Class CardItem: A simple overloaded QGraphicsSvgItem that also stores the card position and the state_open
    """
    def __init__(self, card, position, state_open): #state--> open:TRUE or flipped:FAlSE
        super().__init__()
        self.card = card
        self.setSharedRenderer(CardRenderer(card, state_open).renderer)
        self.position = position
        self.status_open = state_open

    def changeState(self, status_open):
        self.status_open = status_open
        self.setSharedRenderer(CardRenderer(self.card, self.status_open).renderer)

class CardItemList:
    """
    Class CardItemList: List of card items.
    """
    def __init__(self, cards):
        self.list_cardItems = []
        self.ini(cards)

    def ini(self, cards):
        for indices, card in enumerate(cards):
            carditem = CardItem(card, indices, False)
            self.list_cardItems.append(carditem)

    def openCard(self, position):  # position of card in ItemList
        self.list_cardItems[position].changeState(True)

    def coverCard(self, position): # position of card in ItemList
        self.list_cardItems[position].changeState(False)

class CardView:
    """
    Class CardView: Shows Cards.
    """
    def __init__(self, cards): # cards: list of PlayingCards
        self.cardItemList = CardItemList(cards)
        self.list_cardItems = self.cardItemList.list_cardItems
        self.scene = QGraphicsScene()

        self.refreshView()

        self.view = QGraphicsView(self.scene)
        self.view.setGeometry(0, 0, 100, 110)

    def open_Player_Cards(self):
        for i in range(2):
            self.cardItemList.openCard(i)

    def cover_Player_Cards(self):
        for i in range(2):
            self.cardItemList.coverCard(i)

    def open_Table_Cards(self):
        i = 0
        self.cardItemList.openCard(i)
        i = i+1

    def refreshView(self):

        self.scene.clear()
        for card in self.list_cardItems:
            card.setPos(card.position * 125, 0)
            self.scene.addItem(card)

#buttons
class ButtonsView:

    def __init__(self): #glaube nicht dass das game hier übergeben werden sollte
        self.mainWidget = QWidget()
        self.layout = QHBoxLayout()
                
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

#pot
class PotView:
    def __init__(self, pot):
        self.mainWidget = QWidget()
        self.layout = QHBoxLayout()

        self.pot = pot

        self.money_label = QLabel("Pot:")

        self.layout.addWidget(self.money_label)

        self.mainWidget.setLayout(self.layout)

    def refresh_Pot_Money(self, money):
        self.money_label.setText(f"Pot: {money}")



class PlayerView: #--> view won't need player?
    def __init__(self, player):

        self.player = player

        self.mainWidget = QWidget()
        self.layout = QVBoxLayout()

        self.name_label = QLabel(f"{self.player.name}")
        self.money_label = QLabel()
        self.bet_label = QLabel()
        self.blind_label = QLabel()
        self.activeText = QLabel("active")
        self.activeText.setStyleSheet("background-color : red;")

        self.refreshView()

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.money_label)
        self.layout.addWidget(self.bet_label)
        self.layout.addWidget(self.blind_label)
        self.layout.addWidget(self.activeText)

        self.mainWidget.setLayout(self.layout)

    def refreshView(self):
        self.money_label.setText(f"Money: {self.player.money}")
        self.bet_label.setText(f"Bet: {self.player.bet}")
        self.blind_label.setText(f"{self.player.blind}")

        #check active_state
        if self.player.active_state:
            self.activeText.show()
        else:
            self.activeText.hide()

class PokerView:
    def __init__(self, game: Game):
        self.game = game

        self.window = Window()
        self.potView = PotView(game.pot) #maybe self.pot is not needed
        self.buttonsView = ButtonsView()
        self.playerView1 = PlayerView(game.player1)
        self.playerView2 = PlayerView(game.player2)
        self.cardView_player1 = CardView(game.player1.handCards)
        self.cardView_player2 = CardView(game.player2.handCards)
        self.cardView_table = CardView(game.tablecards)

        self.window.addView(self.potView.mainWidget, 1, 1)
        self.window.addView(self.buttonsView.mainWidget, 3, 1)
        self.window.addView(self.playerView1.mainWidget, 1, 0)
        self.window.addView(self.playerView2.mainWidget, 1, 2)
        self.window.addView(self.cardView_player1.view, 0, 0)
        self.window.addView(self.cardView_player2.view, 0, 2)
        self.window.addView(self.cardView_table.view, 0, 1)


        #connect signal
        self.buttonsView.raiseButton.clicked.connect(self.game.raise_)
        self.buttonsView.callButton.clicked.connect(self.game.call_)
        self.buttonsView.checkButton.clicked.connect(self.game.check_)
        self.buttonsView.foldButton.clicked.connect(self.game.fold_)

        self.game.refresh_players_view_signal.connect(self.playerView1.refreshView)
        self.game.refresh_players_view_signal.connect(self.playerView2.refreshView)

        #self.game.show_player1_cards_signal.connect(self.cardView_player1.open_Player_Cards)
        #self.game.show_player1_cards_signal.connect(self.cardView_player2.cover_Player_Cards)

        #self.game.show_player2_cards_signal.connect(self.cardView_player2.open_Player_Cards)
        #self.game.show_player2_cards_signal.connect(self.cardView_player1.cover_Player_Cards)

        #self.game.show_tablecards_signal.connect(self.cardView_table.open_Table_Cards)

        #self.game.refresh_card_view_signal.connect(self.cardView_player1.refreshView)
        #self.game.refresh_card_view_signal.connect(self.cardView_player2.refreshView)

    def showView(self):
        self.window.show()


"""
        self.game.refresh_signal.connect(self.player1_prop_view.refresh_view)

        self.game.show_card_signal.connect(lambda: openCard(self.tableCardsItemList, 3))

        self.game.change_active_to1_signal.connect(self.player1_prop_view.refresh_status)
        self.game.change_active_to2_signal.connect(self.player2_prop_view.refresh_status)

    
"""
