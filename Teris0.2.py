#coding:utf8
"""
    这个版本实现用键盘的左右键控制T形左右移动
    为了实现移动，我们用两个变量self.x和self.y，表示T形的坐标
    注意：一个T形有4有4个正方形，这里的坐标指的是其中相对坐标为(0 ,0)的那个正方形的坐标

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
        self.update()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    app.exec_()