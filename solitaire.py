"""
Студент Гайдук Сергей КН-19-1
Solitaire Classic
"""

import random
import os
import sys

from PyQt5 import QtGui, QtWidgets, uic, QtCore
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtCore import pyqtSignal, QPoint
from PyQt5.QtGui import QPixmap, QDesktopServices
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QMainWindow, QWidget, QApplication, QFrame, QMessageBox


class Card(QLabel):
    """
    A class called Card that represent a playing card in Solitaire.
    This class contains a constructor to initialize the data attributes,
    and other methods that return values.
    """
    pos = QPoint()
    card_clicked = pyqtSignal()

    def __init__(self, value, suit, parent=None):
        """__init__ is a constructor that uses the parameters to initialize the data attributes.

        Keywords arguments:
        :param suit: suit of our card.
        :param value: value of our card (from twos to aces).
        """
        QWidget.__init__(self, parent)

        self.suit = suit
        self.value = value
        self.image = QPixmap()
        self.stack = None
        self.child = None
        self.side = None
        self.faced_up = False
        self.flag_capture = False

        self.set_image()
        self.setPixmap(self.image)

    def set_image(self):
        """A method that sets the appropriate image depending on whether the card is open (face up) or not."""
        if self.faced_up:
            self.image = QPixmap(os.path.join('cards', '%s%s.png' % (self.value, self.suit)))
        else:
            self.image = QPixmap(os.path.join(os.path.join('cards', 'shirt')))

    def mouseMoveEvent(self, event):
        """A method (event) that fires at an element when a mouse is moved while the cursor's hotspot is inside it.
        This event handler can be reimplemented in a subclass to receive widget move events
        which are passed in the event parameter."""
        if event.buttons() == QtCore.Qt.LeftButton and self.flag_capture and self.faced_up:
            delta = QPoint(event.globalPos() - self.pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.pos = event.globalPos()

            print(self.x() + delta.x(), self.y() + delta.y())

    def mousePressEvent(self, event):
        """This event handler, for event event, can be reimplemented in a subclass to
        receive mouse press events for the widget."""
        self.flag_capture = True
        self.pos = event.globalPos()

        if event.buttons() == QtCore.Qt.LeftButton and not self.faced_up:
            self.card_clicked.emit()
        elif event.buttons() == QtCore.Qt.RightButton:
            print(self.value, self.suit)

    def mouseReleaseEvent(self, event):
        """This event handler, for event event, can be reimplemented in a subclass to
        receive mouse release events for the widget."""
        self.flag_capture = False

    def different_suits(self, value):
        """This is a method that returns Heart or Diamond suit if the card has Club or Spade suit,
        otherwise returns Spade or Club suit.

        C - Clubs | S - Spades | H - Hearts | D - Diamonds
        :param value: our playing card.
        :return: Heart or Diamond suit if the card has Club or Spade suit, else Spade or Club suit.
        """
        if self.suit == "C" or self.suit == "S":
            # print(f'{self.suit} == Hearts or Diamonds')
            return value.suit == "H" or value.suit == "D"
        else:
            return value.suit == "S" or value.suit == "C"
            # print(f'{self.suit} == Spades or Clubs')

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

    def face_up(self, value):
        """A method that takes a boolean value and sets the state of the game card to face up.
        Depending on whether the value is true or false, displays the corresponding image of the game card
        (shirt or current suit and value of the card).

        :param value: takes the value of true or false. If the value is true, the card face up, if false - closed.
        """
        self.faced_up = value
        self.set_image()
        self.setPixmap(self.image)


class Deck:
    """
    A class called Deck which represent a deck of cards in Solitaire.
    This class contains a constructor to initialize the data attributes,
    and other methods that return values.
    """
    card_values = [i for i in range(1, 14)]
    card_suits = ['C', 'D', 'H', 'S']

    def __init__(self):
        """__init__ is a constructor that uses the parameters to initialize the data attributes."""
        self.cards = []
        self.build_cards()
        self.shuffle_deck()

    def build_cards(self):
        """This is a method that builds the deck."""
        for suit in self.card_suits:
            for value in range(1, 14):
                self.cards.append(Card(value, suit))

    def shuffle_deck(self):
        """ This is a method that shuffles the deck."""
        for i in range(len(self.cards) - 1, 0, -1):
            random_nmb = random.randint(0, i)
            self.cards[i], self.cards[random_nmb] = self.cards[random_nmb], self.cards[i]


class MainWindow(QMainWindow):
    """
    A class called MainWindow that displays all content in the program window and
    contains state and behavior that are necessary to play the Solitaire.
    This class contains a constructor to initialize the data attributes, and other methods that return values.
    """
    stock_shirt = []
    tableau_cards = [
        [], [], [], [], [], [], []  # tableau piles
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi('Table.ui')
        self.deck = Deck()

        self.wastePile_x, self.wastePile_y = 35, 25  # closed cards in stock bias
        self.cardX, self.cardY = 80, 116  # width and height of the card
        self.bias_deck = 0  # shifting decks of cards (stock)
        self.bias_table = 0  # shifting decks of cards on the tableau

        self.frame_style = "border: 3px solid #000000; border-radius: 10px; border-style: solid; " \
                           "padding: 5px; border-image: #555;"

        # for waste piles
        for item in self.deck.cards:
            item.card_clicked.connect(self.waste_pile)

        # status bar
        self.statusLeft = QLabel('')
        self.statusLeft.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.statusLeft.setAlignment(Qt.AlignHCenter)
        self.statusRight = QLabel('')
        self.statusRight.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.statusRight.setAlignment(Qt.AlignHCenter)

        self.ui.statusbar.addPermanentWidget(self.statusLeft, 1)
        self.ui.statusbar.addPermanentWidget(self.ui.lcdNumber, 1)

        # timer
        self.current_time = QtCore.QTime(00, 00, 00)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        self.ui.actionRules.triggered.connect(self.show_rules)
        self.ui.actionRestart.triggered.connect(self.restart_game)
        self.ui.actionQuit.triggered.connect(self.quit_game)

        self.foundation_piles()
        self.deal_deck()
        self.showTime()

        self.ui.show()

    def showTime(self):
        """A method that calculates and displays time."""
        self.current_time = self.current_time.addSecs(1)
        text = self.current_time.toString('hh:mm:ss')
        self.ui.lcdNumber.display(text)

    def foundation_piles(self):
        """A method that displays the frames of the game cards."""
        bias_foundation = 0
        for frame in range(4):
            frame = QLabel('')
            self.ui.stock_layout.addChildWidget(frame)
            frame.setGeometry(690 + bias_foundation, 40, self.cardX, self.cardY)
            frame.setStyleSheet(self.frame_style)
            bias_foundation += 120

        bias_foundation = 0
        for frame in range(2):
            frame = QLabel('')
            self.ui.stock_layout.addChildWidget(frame)
            frame.setGeometry(50 + bias_foundation, 40, self.cardX, self.cardY)
            frame.setStyleSheet(self.frame_style)
            bias_foundation += 120

    def deal_deck(self):
        """A method that builds stock (pile of closed cards) and deals it to tableau."""
        for item in self.deck.cards:
            if self.bias_deck < 15:
                self.bias_deck += 5
            self.ui.stock_layout.addChildWidget(item)
            item.setGeometry(self.wastePile_x + self.bias_deck,
                             self.wastePile_y + self.bias_deck,
                             self.cardX, self.cardY)

        tableau_pileX, tableau_pileY = 0, 0
        for item in range(len(self.tableau_cards)):
            for value in range(item + 1):
                card = self.deck.cards.pop()
                card.raise_()
                card.move(180 + tableau_pileX, 330 + tableau_pileY)
                self.tableau_cards[item].append(card)
                tableau_pileY += 15  # spacing between cards
                self.bias_table += 14
            tableau_pileX += 125
            tableau_pileY = 0
            self.tableau_cards[item][-1].face_up(True)
        print('stock:', len(self.deck.cards))

    def waste_pile(self):
        """A method that displays waste pile and updates stock."""
        if self.stock_shirt:
            card = self.stock_shirt.pop()
            card.move(50, 40)  # show shirt card again
            self.deck.cards.insert(0, card)
            card.face_up(False)

        card = self.deck.cards.pop()
        card.move(170, 40)
        card.raise_()
        self.stock_shirt.insert(0, card)
        card.face_up(True)

    def victory(self):
        """A method that tracks victory in solitaire."""
        for suit, stack in self.card_suits:
            if len(stack) == 0:
                return False
            pile = stack[-1]
            if pile.value != 13:
                return False
        return True

    def show_rules(self):
        """A method that opens the site where the rules of the game of solitaire are written."""
        msg = QMessageBox.question(self, "Open web site", "You will be redirected to a site that describes the rules "
                                                          "of the game of solitaire. Do you want to open a website?",
                                   QMessageBox.Yes | QMessageBox.No)
        if msg == QMessageBox.Yes:
            url = QUrl("https://bicyclecards.com/how-to-play/solitaire/")
            QDesktopServices.openUrl(url)

    def restart_game(self):
        """A method that restarts the game."""
        msg = QMessageBox.question(self, "Restart", "Are you sure you want to start a new game?",
                                   QMessageBox.Yes | QMessageBox.No)
        if msg == QMessageBox.Yes:
            self.ui = MainWindow()

    def quit_game(self):
        """A method that closes the game window."""
        msg = QMessageBox.question(self, "Exit", "Are you sure you want to quit the game?",
                                   QMessageBox.Yes | QMessageBox.No)
        if msg == QMessageBox.Yes:
            self.ui.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
