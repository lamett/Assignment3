"""
Assignment 3
author: Annabell Kießler, Davide Alpino
03.03.2022

GUI elements
"""

from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *

import cardlib
from pokermodel import *


# window
class Window(QGroupBox):
    """
    Class Window: Sets the window
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Texas Holdem")
        self.setStyleSheet("background-image:url(cards/table.png);")
        self.layout = QGridLayout()
        self.setLayout(self.layout)

    def add_view(self, widget, column, row):
        self.layout.addWidget(widget, column, row)


class CardItem(QGraphicsSvgItem):
    """
    Class CardItem: A simple overloaded QGraphicsSvgItem that also stores the card position and the state_open
    """

    def __init__(self, card_img, position):
        super().__init__()
        self.setSharedRenderer(card_img)
        self.position = position


class CardView(QGraphicsView):
    """
    Class CardView: Shows Cards.
    """

    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

    def change_cards(self, card_imgs):
        cardItem_list = []
        for pos, card_img in enumerate(card_imgs):
                cardItem_list.append(CardItem(card_img, pos))

        for cardItem in cardItem_list:
            cardItem.setPos(cardItem.position * 125, 0)
            self.scene.addItem(cardItem)


# buttons
class ButtonsView(QWidget):
    """
    Class ButtonView: class for all the different buttons(raise, call, check, fold, amount to raise and next
    """

    def __init__(self):
        """
        inits all the Layouts and buttons and sets everything to our mainWIdget
        """
        super().__init__()

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

        self.setLayout(self.layout_v)

    def set_next_button_active(self) :# alles zu einer funktion mergen**
        QPushButton.setDisabled(self.next_button, False)

    def set_next_button_disabled(self) :
        QPushButton.setDisabled(self.next_button, True)

    def set_buttons_active(self) :
        QPushButton.setDisabled(self.raiseButton, False)
        QPushButton.setDisabled(self.callButton, False)
        QPushButton.setDisabled(self.checkButton, False)
        QPushButton.setDisabled(self.foldButton, False)

    def set_buttons_disabled(self) :
        QPushButton.setDisabled(self.raiseButton, True)
        QPushButton.setDisabled(self.callButton, True)
        QPushButton.setDisabled(self.checkButton, True)
        QPushButton.setDisabled(self.foldButton, True)


class TableView(QWidget):
    """
    class TableView: View of middle table
    """

    def __init__(self, game, pot, all_card_imgs):
        super().__init__()

        self.pot = pot
        self.game = game
        self.all_card_imgs = all_card_imgs
        layout = QVBoxLayout()

        self.cardView = CardView()

        self.pot_label = QLabel()

        self.refresh_view()

        layout.addWidget(self.cardView)
        layout.addWidget(self.pot_label)

        self.setLayout(layout)

    def refresh_view(self):
        self.pot_label.setText(f"Pot: {self.pot.get_value()}")

        card_imgs = []
        cards_open = [0, 3, 4, 5, 5]

        for i, amount in enumerate(cards_open):
            if i == self.game.round_number:
                for card_index in range(0, cards_open[i]):
                    graphic_key = (self.game.tableCards[card_index].get_value(), self.game.tableCards[card_index].get_suit())
                    card_imgs.append(self.all_card_imgs[graphic_key])
                for card_index in range(cards_open[i], 5):
                    card_imgs.append(self.all_card_imgs["back"])
                break

        self.cardView.change_cards(card_imgs)


class PlayerView(QWidget):
    """
    class PlayerView: View of one player
    """

    def __init__(self, player, all_card_imgs):
        """
        inits the view for one player
        @param player: the player for whicht the view will be initialised
        """
        super().__init__()

        self.player = player
        self.all_card_imgs = all_card_imgs
        layout = QVBoxLayout()

        self.cardView = CardView()

        name_label = QLabel(f"{self.player.name}")
        self.money_label = QLabel()
        self.bet_label = QLabel()
        self.activeText = QLabel("active")
        self.activeText.setStyleSheet("color: red;")

        self.refresh_view()

        layout.addWidget(self.cardView)
        layout.addWidget(name_label)
        layout.addWidget(self.money_label)
        layout.addWidget(self.bet_label)
        layout.addWidget(self.activeText)

        self.setLayout(layout)

    def refresh_view(self):
        self.money_label.setText(f"Money: {self.player.money}")
        self.bet_label.setText(f"Bet: {self.player.bet}")

        # check active_state
        if self.player.active_state:
            self.activeText.show()
        else:
            self.activeText.hide()

        # refresh card graphics
        card_imgs = []
        if self.player.active_state:
            for handCard in self.player.handCards:
                graphic_key = (handCard.get_value(), handCard.get_suit())
                card_imgs.append(self.all_card_imgs[graphic_key])
        else:
            for i in range(len(self.player.handCards)):
                card_imgs.append(self.all_card_imgs["back"])

        self.cardView.change_cards(card_imgs)


def read_cards():
    all_cards = dict()  # Dictionaries let us have convenient mappings between cards and their images

    for suit in cardlib.Suit:  # You'll need to map your suits to the filenames here. You are expected to change this!
        for value_file, value in zip(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'], range(2, 15)):
            file = value_file + suit.name[0]
            key = (value, suit)  # I'm choosing this tuple to be the key for this dictionary

            all_cards["back"] = QSvgRenderer('cards/Red_Back_2.svg')
            all_cards[key] = QSvgRenderer('cards/' + file + '.svg')

    return all_cards

class PokerView:
    """
    class PokerView: View to aggregate all other views and connect all signals and messages
    """

    def __init__(self, game: Game):
        """
        aggregates all other views together and connects the views to the game logic
        @param game: the logic behind everything
        """
        self.game = game

        all_card_imgs = read_cards()

        self.window = Window()
        tableView = TableView(self.game, self.game.pot, all_card_imgs)
        buttonsView = ButtonsView()
        playerViews = []
        for player in self.game.players:
            playerViews.append(PlayerView(player, all_card_imgs))


        self.window.add_view(tableView, 0, 1)
        self.window.add_view(buttonsView, 3, 1)

        position_player_views = [0, 2]
        for i, pos in enumerate(position_player_views):
            self.window.add_view(playerViews[i], 0, pos)

        buttonsView.set_next_button_disabled()

        # connect signal #muss in die classen geschrieben werden**
        buttonsView.raiseButton.clicked.connect(lambda: self.game.raise_(buttonsView.raise_input.text()))
        buttonsView.callButton.clicked.connect(self.game.call_)
        buttonsView.checkButton.clicked.connect(self.game.check_)
        buttonsView.foldButton.clicked.connect(self.game.fold_)
        buttonsView.next_button.clicked.connect(self.game.next_match)

        for playerView in playerViews:#muss in class connected werden**
            self.game.refresh_player_view.connect(playerView.refresh_view)

        self.game.refresh_table_view.connect(tableView.refresh_view) #muss in class connected werden**

        self.game.enable_next_button.connect(buttonsView.set_next_button_active)#enable,disable button nicht speziel für next sondern generell, werden auch in class connectet**
        self.game.disable_next_button.connect(buttonsView.set_next_button_disabled)

        self.game.enable_buttons.connect(buttonsView.set_buttons_active)
        self.game.disable_buttons.connect(buttonsView.set_buttons_disabled)

        # messages
        self.msg = QMessageBox() #ein msg signal mit übergabe des txt**

        self.game.game_state_message.connect(lambda x: self.show_message(x))

    
    def show_message(self, message):
        if(message == "raise_error"):
            self.show_raise_error_message()
        elif(message == "show_check_error"):
            self.show_check_error_message()
        elif(message == "tie"):
            self.show_tie_message()
        elif(message == "game_winner"):
            self.show_game_winner_message(self.game.get_winner().name)
        elif(message == "fold_winner"):
            self.show_fold_win_message(self.game.get_winner().name,self.game.pot.get_value())
        elif(message == "match_winner"):
            self.show_match_winner_message(self.game.get_winner().name,self.game.pot.get_value(),self.game.get_winning_handtype())


    def show_raise_error_message(self) :
        self.msg.setWindowTitle("Raise_Error")
        self.msg.setText("You don't have enough money")
        self.msg.setBaseSize(QSize(100, 100))
        self.msg.exec()

    def show_check_error_message(self) :
        self.msg.setWindowTitle("Check_Error")
        self.msg.setText("Your bet have to be higher or equal to the others")
        self.msg.setBaseSize(QSize(100, 100))
        self.msg.exec()

    def show_tie_message(self) :
        self.msg.setWindowTitle("Match Over")
        self.msg.setText(f"It's a tie!")
        self.msg.setBaseSize(QSize(100, 100))
        self.msg.exec()

    def show_game_winner_message(self, name) :
        self.msg.setWindowTitle("Game Over")
        self.msg.setText(f"{name} wins the game!")
        self.msg.setBaseSize(QSize(100, 100))
        self.msg.exec()

    def show_fold_win_message(self, name, pot_value) :
        self.msg.setWindowTitle("Match Over")
        self.msg.setText(f"A Player folded their cards. {name} wins {pot_value}!")
        self.msg.setBaseSize(QSize(100, 100))
        self.msg.exec()

    def show_match_winner_message(self, name, pot_value, handtype) :
        self.msg.setWindowTitle("Match Over")
        self.msg.setText(f"{name} wins {pot_value} with {handtype}!")
        self.msg.setBaseSize(QSize(100, 100))
        self.msg.exec()

    def show_view(self) :
        self.window.show()
