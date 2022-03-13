"""
Assignment 3
author: Annabell Kießler, Davide Alpino
03.03.2022
"""
from pokerview import *
from pokermodel import *
import sys


def main():
    """
    Creates a new game and PokerView and starts the game.
    """
    qt_app = QApplication(sys.argv)
    game = Game()
    view = PokerView(game)
    view.show_view()
    qt_app.exec_()


if __name__ == "__main__":
    main()
