"""
Assignment 2
author: Annabell Kießler, Davide Alpino
03.03.2022

GUI elements
"""

from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
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
        self.setStyleSheet("background-image:url(cards/table.png);")

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
    def __init__(self, cards): #cards: list of PlayingCards
        self.cardItemList = CardItemList(cards)
        self.list_cardItems = self.cardItemList.list_cardItems
        self.scene = QGraphicsScene()

        self.refreshView()

        self.view = QGraphicsView(self.scene)
        self.view.setGeometry(0, 0, 100, 110)

    def change_Cards(self, cards):
        print(cards)
        self.cardItemList = CardItemList(cards)
        self.list_cardItems = self.cardItemList.list_cardItems

    def open_Player_Cards(self):
        for i in range(2):
            self.cardItemList.openCard(i)

    def cover_Player_Cards(self):
        for i in range(2):
            self.cardItemList.coverCard(i)

    def cover_Table_Cards(self):
        for i in range(5):
            self.cardItemList.coverCard(i)

    def show_first3_table_cards(self):
        for i in range(3):
            self.cardItemList.openCard(i)

    def show_fourth_card(self):
        self.cardItemList.openCard(3)

    def show_fifth_card(self):
        self.cardItemList.openCard(4)

    def refreshView(self):

        self.scene.clear()
        for card in self.list_cardItems:
            card.setPos(card.position * 125, 0)
            self.scene.addItem(card)

#buttons
class ButtonsView: #**changed input layout

    def __init__(self):
        self.mainWidget = QWidget()
        self.widget_h1 = QWidget()
        self.widget_h2 = QWidget()

        self.layout_v = QVBoxLayout()
        self.layout_h1 = QHBoxLayout()
        self.layout_h2 = QHBoxLayout()

        self.raiseButton = QPushButton("RAISE")
        self.callButton = QPushButton("CALL")
        self.checkButton = QPushButton("CHECK")
        self.foldButton = QPushButton("FOLD")

        self.raise_amount_text = QLabel("Amount to raise:")
        self.raise_input = QLineEdit("0")
        self.space_label = QLabel()
        self.next_button = QPushButton("NEXT")

        self.layout_h1.addWidget(self.raiseButton, 2)
        self.layout_h1.addWidget(self.callButton, 2)
        self.layout_h1.addWidget(self.checkButton, 2)
        self.layout_h1.addWidget(self.foldButton, 2)

        self.layout_h2.addWidget(self.raise_amount_text)
        self.layout_h2.addWidget(self.raise_input)
        self.layout_h2.addWidget(self.space_label, 1)
        self.layout_h2.addWidget(self.next_button)

        self.widget_h1.setLayout(self.layout_h1)
        self.widget_h2.setLayout(self.layout_h2)

        self.layout_v.addWidget(self.widget_h1)
        self.layout_v.addWidget(self.widget_h2)

        self.mainWidget.setLayout(self.layout_v)

    def set_next_button_Active(self):
        QPushButton.setDisabled(self.next_button, False)

    def set_next_button_Disabled(self):
        QPushButton.setDisabled(self.next_button, True)

    def set_buttons_Active(self):
        QPushButton.setDisabled(self.raiseButton, False)
        QPushButton.setDisabled(self.callButton, False)
        QPushButton.setDisabled(self.checkButton, False)
        QPushButton.setDisabled(self.foldButton, False)

    def set_buttons_Disabled(self):
        QPushButton.setDisabled(self.raiseButton, True)
        QPushButton.setDisabled(self.callButton, True)
        QPushButton.setDisabled(self.checkButton, True)
        QPushButton.setDisabled(self.foldButton, True)

#pot
class PotView:
    def __init__(self, pot):
        self.mainWidget = QWidget()
        self.layout = QHBoxLayout()

        self.pot = pot

        self.money_label = QLabel("Pot:")

        self.layout.addWidget(self.money_label)

        self.mainWidget.setLayout(self.layout)

    def refresh_Pot_Money(self):
        self.money_label.setText(f"Pot: {self.pot.get_value()}")

class PlayerView: #--> view won't need player?
    def __init__(self, player):

        self.player = player

        self.mainWidget = QWidget()
        self.layout = QVBoxLayout()

        self.name_label = QLabel(f"{self.player.name}")
        self.money_label = QLabel()
        self.bet_label = QLabel()
        self.activeText = QLabel("active")
        self.activeText.setStyleSheet("color: red;")

        self.refreshView()

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.money_label)
        self.layout.addWidget(self.bet_label)
        self.layout.addWidget(self.activeText)

        self.mainWidget.setLayout(self.layout)

    def refreshView(self):
        self.money_label.setText(f"Money: {self.player.money}")
        self.bet_label.setText(f"Bet: {self.player.bet}")

        #check active_state
        if self.player.active_state:
            self.activeText.show()
        else:
            self.activeText.hide()

class PokerView:
    def __init__(self, game: Game):
        self.game = game

        self.window = Window()
        self.potView = PotView(self.game.pot)
        self.buttonsView = ButtonsView()
        self.playerView1 = PlayerView(self.game.player1)
        self.playerView2 = PlayerView(self.game.player2)
        self.cardView_player1 = CardView(self.game.player1.handCards)
        self.cardView_player2 = CardView(self.game.player2.handCards)
        self.cardView_table = CardView(self.game.tableCards)

        self.window.addView(self.potView.mainWidget, 1, 1)
        self.window.addView(self.buttonsView.mainWidget, 3, 1)
        self.window.addView(self.playerView1.mainWidget, 1, 0)
        self.window.addView(self.playerView2.mainWidget, 1, 2)
        self.window.addView(self.cardView_player1.view, 0, 0)
        self.window.addView(self.cardView_player2.view, 0, 2)
        self.window.addView(self.cardView_table.view, 0, 1)

        self.cardView_player1.open_Player_Cards()
        self.buttonsView.set_next_button_Disabled()

        #connect signal
        self.buttonsView.raiseButton.clicked.connect(lambda: self.game.raise_(self.buttonsView.raise_input.text()))
        self.buttonsView.callButton.clicked.connect(self.game.call_)
        self.buttonsView.checkButton.clicked.connect(self.game.check_)
        self.buttonsView.foldButton.clicked.connect(self.game.fold_)
        self.buttonsView.next_button.clicked.connect(self.game.next_match)

        self.game.refresh_players_view_signal.connect(self.playerView1.refreshView)
        self.game.refresh_players_view_signal.connect(self.playerView2.refreshView)

        self.game.show_player1_cards_signal.connect(self.cardView_player1.open_Player_Cards)
        self.game.cover_player1_cards_signal.connect(self.cardView_player1.cover_Player_Cards)

        self.game.show_player2_cards_signal.connect(self.cardView_player2.open_Player_Cards)
        self.game.cover_player2_cards_signal.connect(self.cardView_player2.cover_Player_Cards)

        self.game.refresh_card_view_signal.connect(self.cardView_player1.refreshView)
        self.game.refresh_card_view_signal.connect(self.cardView_player2.refreshView)
        self.game.refresh_card_view_signal.connect(self.cardView_table.refreshView)

        self.game.cover_tablecards_signal.connect(self.cardView_table.cover_Table_Cards)
        self.game.show_first3_cards_signal.connect(self.cardView_table.show_first3_table_cards)
        self.game.show_fourth_card_signal.connect(self.cardView_table.show_fourth_card)
        self.game.show_fifth_card_signal.connect(self.cardView_table.show_fifth_card)

        self.game.refresh_pot_view_signal.connect(self.potView.refresh_Pot_Money)

        self.game.enable_next_button_signal.connect(self.buttonsView.set_next_button_Active)
        self.game.disable_next_button_signal.connect(self.buttonsView.set_next_button_Disabled)

        self.game.enable_buttons_signal.connect(self.buttonsView.set_buttons_Active)
        self.game.disable_buttons_signal.connect(self.buttonsView.set_buttons_Disabled)

        self.game.change_cards_signal.connect(lambda: self.cardView_player1.change_Cards(self.game.player1.handCards))
        self.game.change_cards_signal.connect(lambda: self.cardView_player2.change_Cards(self.game.player2.handCards))
        self.game.change_cards_signal.connect(lambda: self.cardView_table.change_Cards(self.game.tableCards))

        #messages
        self.msg = QMessageBox()

        self.game.trigger_tie_message.connect(self.show_tie_message)
        self.game.trigger_game_winner_message_signal.connect(lambda: self.show_game_winner_message(self.game.get_winner().name))
        self.game.trigger_fold_winner_message_signal.connect(lambda: self.show_fold_win_message(self.game.get_winner().name,\
                                                                                                     self.game.pot.get_value()))
        self.game.trigger_match_winner_message_signal.connect(lambda: self.show_match_winner_message(self.game.get_winner().name,\
                                                                                                     self.game.pot.get_value(),\
                                                                                                     self.game.get_winning_handtype()))
        self.game.raise_error_msg_signal.connect(self.show_raise_error_message)
        self.game.check_error_msg_signal.connect(self.show_check_error_message)

    def show_raise_error_message(self):
        self.msg.setWindowTitle("Raise_Error")
        self.msg.setText("You don't have enough money")
        self.msg.setBaseSize(QSize(100, 100))
        self.msg.exec()

    def show_check_error_message(self):
        self.msg.setWindowTitle("Check_Error")
        self.msg.setText("Your bet have to be higher or equal to the others")
        self.msg.setBaseSize(QSize(100, 100))
        self.msg.exec()

    def show_tie_message(self):
        self.msg.setWindowTitle("Match Over")
        self.msg.setText(f"It's a tie!")
        self.msg.setBaseSize(QSize(100, 100))
        self.msg.exec()

    def show_game_winner_message(self, name):
        self.msg.setWindowTitle("Game Over")
        self.msg.setText(f"{name} wins the game!")
        self.msg.setBaseSize(QSize(100, 100))
        self.msg.exec()

    def show_fold_win_message(self, name, pot_value):
        self.msg.setWindowTitle("Match Over")
        self.msg.setText(f"A Player folded their cards. {name} wins {pot_value}!")
        self.msg.setBaseSize(QSize(100, 100))
        self.msg.exec()

    def show_match_winner_message(self, name, pot_value, handtype):
        self.msg.setWindowTitle("Match Over")
        self.msg.setText(f"{name} wins {pot_value} with {handtype}!")
        self.msg.setBaseSize(QSize(100, 100))
        self.msg.exec()

    def showView(self):
        self.window.show()