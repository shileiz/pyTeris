#coding:utf8
"""
    这个版本不实现新功能
    我们将程序划分为两个类，一个类仍然是 MainWindow，用来做游戏的主界面，另一个类叫Shape，用来表示一个形状

    画形状单独封装成一个函数draw_shape()
    因为shape单独成为了一个类，为了在主界面中画出一个形状，我们需要把shape作为参数传递给draw_shape()
"""
from PyQt4 import QtGui, QtCore
import sys


class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setFixedSize(200, 400)
        self.current_shape = Shape()
        self.x = 100
        self.y = 200
        self.show()

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