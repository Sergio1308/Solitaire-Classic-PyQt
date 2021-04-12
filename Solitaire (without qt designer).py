from PyQt5 import QtGui, QtWidgets, uic, QtCore
import random
import os
import sys


class Card(QtWidgets.QLabel):
    card_values = [i for i in range(1, 14)]
    card_suits = ['C', 'D', 'H', 'S']
    window_size = 1000, 650
    card_offset = 0
    iter = 0
    SIDE_FACE = 0
    SIDE_BACK = 1

    def __init__(self, parent=None):
        super().__init__(parent)

        # self.label_field = {'1': None, '2': None, '3': None, '4': None,'5': None, '6': None, '7': None}
        self.label_field = [str(i) for i in range(1, 8)]
        self.label_pile = []
        self.pile_capture = False
        self.side = None

        self.stack = []
        self.pile = []
        for value in self.card_values:
            for suit in self.card_suits:
                self.stack.append([str(value), suit])

        self.setGeometry(500, 200, *self.window_size)
        self.setWindowTitle("Solitaire Classic")

        self.bg_image = QtWidgets.QLabel(self)
        self.bg_image.resize(*self.window_size)
        self.bg_image.setStyleSheet("border-image : url(cards/bg.png)")

        self.pushButton = QtWidgets.QPushButton('Next card', self)
        self.pushButton.setGeometry(200, 200, 91, 51)

        self.pushButton_2 = QtWidgets.QPushButton('Previous card', self)
        self.pushButton_2.setGeometry(200, 300, 91, 51)

        self.pushButton_3 = QtWidgets.QPushButton('Shuffle', self)
        self.pushButton_3.setGeometry(650, 240, 91, 51)

        self.pushButton_4 = QtWidgets.QPushButton('Remove card', self)
        self.pushButton_4.setGeometry(770, 240, 91, 51)

        self.pushButton.clicked.connect(self.next_card)
        self.pushButton_2.clicked.connect(self.previous_card)
        self.pushButton_3.clicked.connect(self.shuffle_deck)
        self.pushButton_4.clicked.connect(self.remove_card)

        # layout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel('', self)  # Shirt card
        self.label.setGeometry(360, 220, 80, 116)
        self.label_2 = QtWidgets.QLabel('', self)  # Current card
        self.label_2.setGeometry(490, 220, 80, 116)

        self.label_3 = QtWidgets.QLabel('', self)  # Number of cards
        self.label_3.setGeometry(440, 300, 101, 151)
        self.label_4 = QtWidgets.QLabel('', self)  # Removed card
        self.label_4.setGeometry(710, 340, 101, 151)

        self.label_2.mousePressEvent = self.mouse_press
        self.label_2.mouseReleaseEvent = self.mouse_release

        self.label.setPixmap(
            QtGui.QPixmap(os.path.join('cards', 'shirt')))  # skin for a face-down card

        self.label_2.setPixmap(QtGui.QPixmap(os.path.join('cards', '1C')))
        self.label_3.setText(f'Cards: {len(self.stack)}')

        for name in self.label_field:
            self.new_widget = QtWidgets.QLabel(name, self)
            self.label_pile.append(self.new_widget)

            # self.label_pile[name].setVisible(False)
            # self.label_field[name] = label_pile
            # name.setText('LOL')
            # name.setGeometry(200, 600, 91, 51)
            # self.label_field[name].setText('Kekw')
            # label_pile.move(50, 50 + self.q)
            # print(self.label_field[name])
        self.load_images()
        self.show()

    def load_images(self):
        self.face = QtGui.QPixmap(os.path.join('cards', '%s%s.png' % (self.stack[0][0], self.stack[0][1])))

        self.back = QtGui.QPixmap(os.path.join(os.path.join('cards', 'shirt')))

    def open_card(self):
        self.side = self.SIDE_FACE
        self.setPixmap(self.face)

    def close_card(self):
        self.side = self.SIDE_BACK
        self.setPixmap(self.back)

    @property
    def is_open_card(self):
        return self.side == self.SIDE_FACE

    def mouseMoveEvent(self, event):
        if self.flag_capture:
            self.label_2.move(event.x() - self.pos.x(), event.y() - self.pos.y())
            if event.x() - self.pos.x() == 710:
                self.pile_capture = True
            else:
                self.pile_capture = False

    def mouse_press(self, event):
        self.flag_capture = True
        self.pos = event.pos()

    def mouse_release(self, event):
        self.flag_capture = False
        if self.pile_capture:
            self.label_2.move(710, 370 + self.card_offset)
            # print(self.label_2.pos())
        else:
            self.label_2.move(490, 220)

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
        self.label_2.setPixmap(pixmap.scaled(80, 116))
        self.label_3.setText(f'Cards: {len(deck)}')

    def next_card(self):
        self.build_deck(-1, self.stack)

    def previous_card(self):
        self.build_deck(0, self.stack)

    def shuffle_deck(self):
        for i in range(len(self.stack) - 1, 0, -1):
            random_nmb = random.randint(0, i)
            self.stack[i], self.stack[random_nmb] = self.stack[random_nmb], self.stack[i]
            pixmap = QtGui.QPixmap(os.path.join('cards', '%s%s.png' % (self.stack[0][0], self.stack[0][1])))
            self.label_2.setPixmap(pixmap)

    def remove_card(self):
        """if len(self.stack) > 2:
            self.pile.append(self.stack[0])
            del self.stack[0]
            pixmap = QtGui.QPixmap(os.path.join('cards', '%s%s.png' % (self.pile[-1][0], self.pile[-1][1])))
            self.label_4.setPixmap(pixmap)
            self.label_4.move(710, 340 + self.card_offset)
            self.label_2.setPixmap(QtGui.QPixmap(os.path.join('cards', f'{self.stack[0][0]}{self.stack[0][1]}.png')))
            self.label_3.setText(f'Cards: {len(self.stack)}')

            self.card_offset += 5"""

        if self.iter < 7:
            self.card_offset += 10  # coordinate offset

            self.pile.append(self.stack[0])
            del self.stack[0]
            # print(self.label_pile)
            pixmap = QtGui.QPixmap(os.path.join('cards', '%s%s.png' % (self.pile[-1][0], self.pile[-1][1])))
            self.label_pile[self.iter].setPixmap(pixmap)
            self.label_pile[self.iter].setGeometry(710, 340 + self.card_offset, 101, 151)
            # self.current_removed = pixmap
            if self.iter > 0:
                self.label_pile[self.iter - 1].setPixmap(QtGui.QPixmap(os.path.join('cards', 'shirt')).scaled(80, 116))

            self.iter += 1
            self.label_2.setPixmap(QtGui.QPixmap(os.path.join('cards', f'{self.stack[0][0]}{self.stack[0][1]}.png')))
            self.label_3.setText(f'Cards: {len(self.stack)}')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Card()
    window.label_2.raise_()
    sys.exit(app.exec())
