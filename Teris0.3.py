#coding:utf8
"""
    这个版本实现用键盘的上下键控制T形变形
    为了实现变形，我们需要理解一个形状旋转90度其坐标的变化，这里需要借助坐标轴

"""
from PyQt4 import QtGui, QtCore
import sys


class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setFixedSize(200, 400)
        self.tshape = [(-1, 0), (0, 0), (1, 0), (0, 1)]
        self.x = 100
        self.y = 200
        self.show()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        for coord in self.tshape:
            painter.drawRect(self.x+coord[0]*10, self.y+coord[1]*10, 10, 10)
        painter.end()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Left:
            self.x -= 10
        elif event.key() == QtCore.Qt.Key_Right:
            self.x += 10
        elif event.key() == QtCore.Qt.Key_Up:
            self.rotate_right()
        elif event.key() == QtCore.Qt.Key_Down:
            self.rotate_left()
        self.update()

    def rotate_right(self):
        self.tshape = [(-y, x) for (x, y) in self.tshape]

    def rotate_left(self):
        self.tshape = [(y, -x) for (x, y) in self.tshape]

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    app.exec_()