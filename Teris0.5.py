#coding:utf8
"""
    这个版本实现形状下落的功能
    我们在主窗口加入一个定时器：QTimer，每隔0.5秒让形状下落一行

"""
from PyQt4 import QtGui, QtCore
import sys


class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setFixedSize(200, 400)
        self.current_shape = Shape()
        self.x = 100
        self.y = 0
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.time_out)
        self.timer.start(500)
        self.show()

    def time_out(self):
        self.y += 10
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.draw_shape(painter, self.current_shape)
        painter.end()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Left:
            self.x -= 10
        elif event.key() == QtCore.Qt.Key_Right:
            self.x += 10
        elif event.key() == QtCore.Qt.Key_Up:
            self.current_shape.rotate_right()
        elif event.key() == QtCore.Qt.Key_Down:
            self.current_shape.rotate_left()
        self.update()

    def draw_shape(self, painter, shape):
        for coord in shape.coordinates:
            painter.drawRect(self.x+coord[0]*10, self.y+coord[1]*10, 10, 10)


class Shape():
    def __init__(self):
        self.coordinates = [(-1, 0), (0, 0), (1, 0), (0, 1)]

    def rotate_right(self):
        self.coordinates = [(-y, x) for (x, y) in self.coordinates]

    def rotate_left(self):
        self.coordinates = [(y, -x) for (x, y) in self.coordinates]


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    app.exec_()