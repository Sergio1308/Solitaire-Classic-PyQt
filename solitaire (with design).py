"""
Студент Гайдук Сергей КН-19-1
Solitaire Classic
"""
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

        self.ui.pushButton.clicked.connect(self.load_stack)
        self.ui.pushButton_2.clicked.connect(self.last_card)
        self.ui.pushButton_3.clicked.connect(self.shuffle_deck)

        self.ui.label.setPixmap(QtGui.QPixmap(os.path.join('cards', '1C')))

        self.ui.show()

    def load_stack(self):
        for i in range(1):
            self.stack.append(self.stack.pop(0))
            pixmap = QtGui.QPixmap(os.path.join('cards', '%s%s.png' % (self.stack[0][0], self.stack[0][1])))
            self.ui.label.setPixmap(pixmap)

    def last_card(self):
        for i in range(1):
            self.stack.insert(0, self.stack.pop())
            pixmap = QtGui.QPixmap(os.path.join('cards', '%s%s.png' % (self.stack[0][0], self.stack[0][1])))
            self.ui.label.setPixmap(pixmap)

    def shuffle_deck(self):
        for i in range(len(self.stack) - 1, 0, -1):
            random_nmb = random.randint(0, i)
            self.stack[i], self.stack[random_nmb] = self.stack[random_nmb], self.stack[i]
            pixmap = QtGui.QPixmap(os.path.join('cards', '%s%s.png' % (self.stack[0][0], self.stack[0][1])))
            self.ui.label.setPixmap(pixmap)
        print('Debug log: shuffled:', len(self.stack), self.stack)

    def label_image(self):
        pixmap = QtGui.QPixmap('')
        self.ui.label.setPixmap(pixmap)

    def label_animation(self):
        movie = QtGui.QMovie('')
        self.ui.label.setMovie(movie)
        movie.start()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QLabelExample()
    sys.exit(app.exec())
