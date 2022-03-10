"""
Assignment 2
author: Annabell Kießler, Davide Alpino
03.03.2022

Game state, main, QApplications
"""
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pokermodel import *
from pokerview import *
from pokermodel import *
import sys

def main():

    qt_app = QApplication(sys.argv)
    game = Game()
    view = PokerView(game)
    view.showView()
    qt_app.exec_()

if __name__ == "__main__":
    main()