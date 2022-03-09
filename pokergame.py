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

    game = Game()
    qt_app = QApplication(sys.argv)
    window = QWidget()
    window.setLayout(PokerView(game, window))
    window.show()

    qt_app.exec_()
if __name__ == "__main__":
    main()