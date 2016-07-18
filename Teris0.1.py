#coding:utf8
"""
    这个版本仅实现显示一个窗口，并在窗口中间显示一个“T”的形状。
    窗口固定大小为200*400，“T”形由4个正方形组成，每个正方形边长为10

    俄罗斯方块中每种形状均由4个正方形组成。
    我们用4个点来表示这4个正方形的相对位置，此处需要画坐标轴示意。

"""
from PyQt4 import QtGui
import sys


class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setFixedSize(200, 400)
        self.tshape = [(-1, 0), (0, 0), (1, 0), (0, 1)]
        self.show()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        for coord in self.tshape:
            painter.drawRect(100+coord[0]*10, 200+coord[1]*10, 10, 10)
        painter.end()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    app.exec_()