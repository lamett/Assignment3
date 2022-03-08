"""
Assignment 2
author: Annabell Kießler, Davide Alpino
08.03.2022

Library
"""
#imports
import enum
import sys
import abc
import random

class Suit(enum.Enum):
    """
        Enum Suit: represents the suits of the cards
    """

    Hearts = 1
    Spades = 2
    Clubs = 3
    Diamonds = 4

class Handtype(enum.Enum):
    """
        Enum Handtype: represents the handtypes and their value
    """
    Highcard = 1
    One_pair = 2    #2 of same value
    Two_pair = 3    #2x 2 of same value
    Three_of_kind = 4   #3 of same value
    Straight = 5    #increasing value with different colours
    Flush = 6       #5 of same suit
    Full_house = 7  #2 of same value and 3 of same value
    Four_of_a_kind = 8  #4 of same value
    Straight_flush = 9  #increasing value with same suit

class PlayingCard(metaclass=abc.ABCMeta):
    """
        Abstract class PlayingCard: represents a playing card
        Attributes: Suit
    """
    def __init__(self, suit):
        self.suit = suit

    def __lt__(self, other):
        """
            Override of the arithmetic operator < : compares the values of two playing cards
            :param other:
            :return: bool: true if smaller, false if higher or equal
        """
        return self.get_value() < other.get_value()

    def __eq__(self, other):
        """
            Override of the arithmetic operator == : compares the values of two playing cards
            :param other:
            :return: bool: true if equal, false not equal
        """
        return self.get_value() == other.get_value()

    @abc.abstractmethod
    def get_value(self):
        """:return: value"""

    @abc.abstractmethod
    def get_suit(self):
        """:return: suit"""

    def __repr__(self):
        return str((self.get_value(), self.get_suit()))

class NumberedCard (PlayingCard):
    """
        Class NumberedCard: represents a numbered playing card
        Attributes: value: int , suit: Suit
    """
    def __init__(self, val: int, s: Suit):
        super().__init__(suit=s)
        if 1 < val < 11:
            self.value = val
        else:
            sys.exit("Wrong value. Accepted values: int [2-10]")

    def get_value(self):
        return self.value

    def get_suit(self):
        return self.suit

class JackCard (PlayingCard):
    """
        Class JackCard: represents a Jackcard with the value = 11
        Attributes: suit: Suit
    """

    def __init__(self, s: Suit):
        super().__init__(suit=s)

    def get_value(self):
        return 11

    def get_suit(self):
        return self.suit

class QueenCard (PlayingCard): #value = 12
    """
        Class QueenCard: represents a Queencard with the value = 12
        Attributes: suit: Suit
    """

    def __init__(self, s: Suit):
        super().__init__(suit=s)

    def get_value(self):
        return 12

    def get_suit(self):
        return self.suit

class KingCard (PlayingCard):
    """
        Class KingCard: represents a Kingcard with the value = 13
        Attributes: suit: Suit
    """

    def __init__(self, s: Suit):  # create a card
        super().__init__(suit=s)

    def get_value(self):
        return 13

    def get_suit(self):
        return self.suit

class AceCard (PlayingCard):
    """
        Class AceCard: represents a Acecard with the value = 14
        Attributes: suit: Suit
    """

    def __init__(self, s: Suit):  # create a card
        super().__init__(suit=s)

    def get_value(self):
        return 14

    def get_suit(self):
        return self.suit

class StandardDeck:
    """
        Class StandardDeck: represents a full Carddeck with 52 Cards
    """

    def __init__(self):
        self.cards = []
        for s in list(Suit):
            for val in range(2, 11):
                self.cards.append(NumberedCard(val, s))  # appendnumbercards

            self.cards.append(JackCard(s))  # append jacks
            self.cards.append(QueenCard(s))  # append queens
            self.cards.append(KingCard(s))  # append kings
            self.cards.append(AceCard(s))  # append aces

    def shuffle(self):
        """
            Shuffles StandardDeck.
            :return: void
        """
        random.shuffle(self.cards)

    def draw(self):
        """
            Returns the first card of the StandardDeck and deletes it from the StandardDeck cards list.
            :return: PlayingCard
        """
        return self.cards.pop(0)

class Hand:
    """
        Class Hand: represents the current cards in the hand of a player
    """

    def __init__(self):
        self.cards = []

    def __repr__(self):
        return str(self.cards)

    def add_card(self, card):
        """
            Adds a PlayingCard to the Hand.
            :param card: Playingcard
            :return: void
        """
        self.cards.append(card)

    def drop_cards(self, index_list_cards):
        """
            Deletes a certain card depending on its index from the Hands cards list.
            :param index_list_cards: index of card
            :return: void
        """
        index_list_cards.sort(reverse=True)
        for index in index_list_cards:
            if index <= len(self.cards)-1:
                self.cards.remove(self.cards[index])

    def sort(self):
        """
            Sorts the cards list of the Hand to its values.
            :return: void
        """
        self.cards.sort()

    def best_poker_hand(self, cards):
        """
            Calculates PokerHand.
            :param cards: additional cards
            :return: PokerHand
        """
        best_hand = PokerHand(self.cards + cards)
        return best_hand

class PokerHand:
    """
        Class PokerHand: represents the best Handtype and their five best cards calculated from a list of cards.
        Attributes: cards: list of card objects
    """

    def __init__(self, cards):
        self.cards = cards
        self.handtype, self.best_cards = self.find_handtype()

    def __repr__(self):
        return str(f"Type: {self.handtype} Bestcards: {self.best_cards}")

    def __lt__(self, other):    #compares Handtype and if equal --> every value in best_cards[]
        """
            Override of the arithmetic operator < : compares the handtype and five best cards of to  PokerHands.
            :param other:
            :return: bool: true if smaller, false if higher or equal
        """

        if self.handtype.value < other.handtype.value:
            return True

        if self.handtype.value == other.handtype.value:  #**changed comparison
            if self.best_cards < other.best_cards:
                return True

        return False

    #methodes: handtypes
    def pair(self, cards):
        """
            Checks cards for one or two pairs.
            :param cards: list of PlayingCards
            :return: count: int number of pairs, five_best_cards: List of five best PlayingCards in this handtype
        """
        cards.sort(reverse=True)
        cards_for_search = cards.copy()
        five_best_cards = []        #list with the values of the 5 important cards
        count = 0                  #counts the pairs

        for i in range(len(cards) - 1):
            if count < 2:       #the third pair is not relevant
                if cards[i].get_value() == cards[i + 1].get_value():  # three_of_kind got checked already
                    count += 1

                    five_best_cards.append(cards[i].get_value())  #adds value of the pair
                    five_best_cards.append(cards[i+1].get_value())

                    cards_for_search = list(filter(lambda x: x.get_value() != cards[i].get_value(), cards_for_search))  #removes pair to calculate the highcard beside the pair

        if len(cards_for_search) >= 5-len(five_best_cards): # to avoid error when fullhouse get checked and cards is incomplete
            for i in range(5-len(five_best_cards)):
                five_best_cards.append(cards_for_search.pop(0).get_value())   #adds highcards

        return count, five_best_cards

    def three_of_kind(self):
        """
            Checks cards for three_of_kind.
            :param:
            :return: bool: true if three PlayingCards of the same value, five_best_cards: List of five best PlayingCards in this handtype
        """
        cards = self.cards
        cards.sort(reverse=True)
        cards_for_search = cards.copy()


        for i in range(len(cards) - 2):
            if cards[i].get_value() == cards[i + 2].get_value():

                triple_indice = i
                five_best_cards = []  # list with the values of the 5 important cards

                for i in range(3):
                    five_best_cards.append(cards_for_search.pop(triple_indice).get_value())  #adds value of triple to best_cards and removes them from cards_for search to evaluate high_cards besides tripple

                for i in range(2):
                    five_best_cards.append(cards_for_search.pop(0).get_value())   #adds highcards

                return True, five_best_cards

        return False, [0]

    def straight(self, cards):
        """
            Checks cards for straight.
            :param cards: list of PlayingCards
            :return: bool: true if straight depending on their value, five_best_cards: List of five best PlayingCards in this handtype
        """
        cards_dupl_rm = map(lambda card: card.get_value(), cards)      #list of values only
        cards_dupl_rm = list(set(cards_dupl_rm))        #to make values unique

        cards_dupl_rm.sort(reverse=True)     #list with just their values and no duplicates

        five_best_cards = []  # list with the values of the 5 important cards

        if cards_dupl_rm[0] == 14:      #adds the value 1 to the list, because the ace can be both
            cards_dupl_rm.append(1)
        for i in range(len(cards_dupl_rm) - 4):     #compares i with i+4 element, if the value of i+4 is 4 lower than the value of i, it is straight
            if cards_dupl_rm[i] == cards_dupl_rm[i + 4] + 4:
                five_best_cards = cards_dupl_rm[i:i+5]      #adds the five highest cards of the straight to five_best_cards
                return True, five_best_cards

        return False, five_best_cards

    def flush(self):
        cards = self.cards
        self.cards.sort(key=lambda x: x.suit.value)     #sort cards by suits

        five_best_cards = []

        for i in range(len(cards)-4):       #if the suit of i equals the suit i+4 it is flush
            if cards[i].suit == cards[i+4].suit:
                five_best_cards = list(map(lambda card: card.get_value(), cards[i:i+5]))        #adds five highest values of flush
                return True, five_best_cards

        return False, five_best_cards

    def fullhouse(self):
        """
            Checks cards for fullhouse.
            :param:
            :return: bool: true if three and two PlayingCards of the same value, five_best_cards: List of five best PlayingCards in this handtype
        """
        bool_tripple, best_cards_tripple = self.three_of_kind()     #checks for three of kind
        five_best_cards = [0]       #needs value 0 for find_handtype logik

        if bool_tripple == True:
            five_best_cards = best_cards_tripple
            cards2 = self.cards.copy()
            cards2 = list(filter(lambda x: x.get_value() != best_cards_tripple[0], cards2)) #removes three of kind from list
            count_pair, best_cards_pair = self.pair(cards2)  #checks if pair

            if count_pair > 0:
                five_best_cards = best_cards_tripple[0:3] + best_cards_pair[0:2]
                return True, five_best_cards

        return False, five_best_cards

    def four_of_kind(self):
        """
            Checks cards for four_of_kind.
            :param:
            :return: bool: true if four PlayingCards of the same value, five_best_cards: List of five best PlayingCards in this handtype
        """
        cards = self.cards
        cards.sort(reverse=True)
        cards_for_search = cards.copy()
        five_best_cards = []

        for i in range(len(cards)-3):       #if value of i equals value of i+3 it is a four of kind
            if cards[i].get_value() == cards[i+3].get_value():
                cards_for_search = list(filter(lambda x: x.get_value() != cards[i].get_value(), cards_for_search))      #removes for of kind from search_list
                five_best_cards = list(map(lambda card: card.get_value(), cards[i:i+4] + cards_for_search[0:1]))        #adds four of kind values and highest card besides
                return True, five_best_cards

        return False, five_best_cards

    def straight_flush(self):
        """
            Checks cards for straight_flush.
            :param:
            :return: bool: true if PlayingCards of same suit are straight, five_best_cards: List of five best PlayingCards in this handtype
        """
        cards = self.cards

        for suit in Suit:
            oneColored = list(filter(lambda x: x.get_suit() == suit, cards))    #creates list for every colour
            if len(oneColored) < 5:     #if there are 5 or more values in the oneColour list it is a flush
                continue
            boo, best_cards_straight = self.straight(oneColored)     #takes the oneColour list and checks if straight
            if boo:
                return True, best_cards_straight        #five_best_cards_straight of OneColourlist is best_cards_flush

        return False, 0

#logik
    def find_handtype(self):
        """
            Calculates best handtype and the five best Playingcards in this handtype.
            :param:
            :return: Handtype, five_best_cards: List of five best PlayingCards in this handtype
        """
        #straight_flush
        boo, five_best_cards = self.straight_flush()
        if boo:
            return Handtype.Straight_flush, five_best_cards

        #four_of_kind
        boo, five_best_cards = self.four_of_kind()
        if boo:
            return Handtype.Four_of_a_kind, five_best_cards

        #full_house
        boo, five_best_cards = self.fullhouse()
        if boo:
            return Handtype.Full_house, five_best_cards

        #saves if three of kind
        boo_three_of_kind = five_best_cards[0]
        five_best_cards_tripple = five_best_cards

        #flush
        boo, five_best_cards = self.flush()
        if boo:
            return Handtype.Flush, five_best_cards

        #straight
        boo,five_best_cards = self.straight(self.cards)
        if boo:
            return Handtype.Straight, five_best_cards

        #three of kind
        if boo_three_of_kind != 0:
            return Handtype.Three_of_kind, five_best_cards_tripple

        #pair
        count, five_best_cards = self.pair(self.cards)

        #two pair
        if count == 2:
            return Handtype.Two_pair, five_best_cards
        #one pair
        if count == 1:
            return Handtype.One_pair, five_best_cards

        #sort by value for highcard
        cards = self.cards
        cards.sort(reverse=True)

        #highcard
        return Handtype.Highcard, list(map(lambda card: card.get_value(), cards[0:5]))
