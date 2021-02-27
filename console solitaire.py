"""
Студент Гайдук Сергей КН-19-1
Solitaire Classic
"""

import random


class Card:
    """
    A class called Card which represent a playing card in Solitaire.
    This class contains a constructor to initialize the data attributes,
    method __str__ which returns a string representation our data attributes
    and other methods that return values.
    """
    # rank of cards
    card_values = {
        1: 'A', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: 'J', 12: 'Q', 13: 'K'
    }

    def __init__(self, suit, value):
        """__init__ is a constructor that uses the parameters to initialize the data attributes.

        Keywords arguments:
        :param suit: suit of our card.
        :param value: value of our card (from twos to aces).
        """
        self.name = self.card_values[value]
        self.suit = suit
        self.card_value = value

    def previous_card(self, value):
        """This is a method that returns previous card value.
        :param value: our playing card.
        """
        return self.card_value == (value.card_value - 1)

    def different_suits(self, value):
        """This is a method that returns Heart or Diamond suit if the card has Club or Spade suit,
        otherwise returns Spade or Club suit.

        :param value: our playing card.
        :return: Heart or Diamond suit if the card has Club or Spade suit, else Spade or Club suit.
        """
        if self.suit == "Clubs" or self.suit == "Spades":
            return value.suit == "Hearts" or value.suit == "Diamonds"
        else:
            return value.suit == "Spades" or value.suit == "Clubs"

    def attach_card(self, value):
        """This is a method that returns True if playing card has previous card value and different suit,
        otherwise returns False.

        :param value: our playing card.
        :return: true if playing card has previous card value and different suit, else False
        """
        if value.previous_card(self) and value.different_suits(self):
            return True
        else:
            return False

    def __str__(self):
        """Method __str__ (instance string representation) which returns a string representation
        of the playing card (value and suit)."""
        return f"{self.name} of {self.suit}"


class Deck:
    """
    A class called Deck which represent a deck of cards in Solitaire.
    This class contains a constructor to initialize the data attributes,
    and other methods that return values.
    """
    def __init__(self):
        """__init__ is a constructor that uses the parameters to initialize the data attributes."""
        self.card_suits = ["Clubs", "Hearts", "Spades", "Diamonds"]

        self.cards_list = []
        self.build_cards()

    def __getitem__(self, item):
        """A special method called when the value is accessed by index or key.

        :param item: index.
        :return: name of the card from the deck.
        """
        return self.cards_list[item]

    def build_cards(self):
        """This is a method that builds the deck."""
        for suit in self.card_suits:
            for value in range(1, 14):
                self.cards_list.append((Card(suit, value)))

    def shuffle(self):
        """ This is a method that shuffles the deck."""
        for i in range(len(self.cards_list) - 1, 0, -1):
            random_nmb = random.randint(0, i)
            self.cards_list[i], self.cards_list[random_nmb] = self.cards_list[random_nmb], self.cards_list[i]

    def drawCard(self):
        """This is a method that "flips" and shows the card.

        :return: card from the list and then removes it from the list.
        """
        return self.cards_list.pop()


class Board:
    """
    A class called Board that contains state and behavior that are necessary to play the Solitaire.
    This class contains a constructor to initialize the data attributes,
    and other methods that return values.
    """
    def __init__(self):
        """__init__ is a constructor that uses the parameters to initialize the data attributes."""
        self.suits_stack = {"Clubs": [], "Hearts": [], "Spades": [], "Diamonds": []}

    def addCard(self, value):
        """This is a method that returns true if the card was added to the board, otherwise returns false.

        :param value: our playing card.
        :return: true - if the card was added to the board, and false - if not
        """
        stack = self.suits_stack[value.suit]

        if (len(stack) == 0 and value.card_value == 1) or stack[-1].previous_card(value):
            stack.append(value)
            return True

        else:
            return False

    def victory(self):
        """In future, this will be a method which tracks victory in solitaire."""
        for suit, stack in self.suits_stack.items():
            if len(stack) == 0:
                return False

            pile = stack[-1]
            if pile.card_value != 13:
                return False
        return True


if __name__ == "__main__":
    # c = Card("Spades", 3)
    # print(c)

    d = Deck()
    d.shuffle()
    for card in d:  # shuffled deck, print using a special method
        print(card)
    c = d.drawCard()
    print('\nWe have:', c)

