"""Solitaire Classic."""

from PyQt5 import QtGui, QtWidgets, uic
import random
import os
import sys


class QLabelExample(QtWidgets.QMainWindow):
    card_values = [i for i in range(1, 14)]
    card_suits = ['C', 'D', 'H', 'S']

    def __init__(self, parent=None):
        super().__init__(parent)

        self.stack = []
        for value in self.card_values:
            for suit in self.card_suits:
                self.stack.append([str(value), suit])

        self.ui = uic.loadUi('Table.ui')

        self.ui.pushButton.clicked.connect(self.next_card)
        self.ui.pushButton_2.clicked.connect(self.previous_card)
        self.ui.pushButton_3.clicked.connect(self.shuffle_deck)
        self.ui.pushButton_4.clicked.connect(self.remove_card)
        
        self.ui.label.setPixmap(QtGui.QPixmap(os.path.join('cards', 'shirt')).scaled(101, 151))  # skin for a face-down card
        self.ui.label_2.setPixmap(QtGui.QPixmap(os.path.join('cards', '1C')).scaled(101, 151))  # first displayed card
        self.ui.label_3.setText(f'Cards: {len(self.stack)}')

        self.ui.show()
    
    def build_deck(self, step, deck):
        """
        :param step: step to shift a list item.
        :param deck: deck of cards.
        """
        if step < 0:
            for i in range(1):
                deck.append(deck.pop(0))
        else:
            for i in range(1):
                deck.insert(0, deck.pop())
        pixmap = QtGui.QPixmap(os.path.join('cards', '%s%s.png' % (deck[0][0], deck[0][1])))
        self.ui.label_2.setPixmap(pixmap.scaled(101, 151))
        self.ui.label_3.setText(f'Cards: {len(deck)}')

    def next_card(self):
        self.build_deck(-1, self.stack)  # shift of the list item to the left

    def previous_card(self):
        self.build_deck(0, self.stack)  # shift of a list item to the right

    def shuffle_deck(self):
        for i in range(len(self.stack) - 1, 0, -1):
            random_nmb = random.randint(0, i)
            self.stack[i], self.stack[random_nmb] = self.stack[random_nmb], self.stack[i]
            pixmap = QtGui.QPixmap(os.path.join('cards', '%s%s.png' % (self.stack[0][0], self.stack[0][1])))
            self.ui.label_2.setPixmap(pixmap.scaled(101, 151))
            
    def remove_card(self):
        if len(self.stack) > 2:
            del self.stack[-1]
            self.ui.label_3.setText(f'Cards: {len(self.stack)}')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QLabelExample()
    sys.exit(app.exec())
