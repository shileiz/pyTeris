#coding:utf8
"""
    这个版本只做小改动：
    1、把空心的正方形改成实心的
    fillRect可以画一个实心无边框的正方形，仍然沿用drawRect给正方形画边框
    注意：要先fillRect再drawRect，不然新fill出来的颜色可能会把边框盖住
    另外，fillRect需要一个颜色参数，这里使用的是：QtCore.Qt.gray ,具体请参看PyQt4的官方文档。

    2、加入了迅速下落功能：当按下空格键的时候，形状迅速触底

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
        self.blocks = [[0 for j in range(10)] for i in range(20)]
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.time_out)
        self.timer.start(500)
        self.show()

    def time_out(self):
        if self.can_move_down():
            self.y += 20
        else:
            for (x, y) in self.current_shape.coordinates:
                self.blocks[(self.y + y*20)/20][(self.x + x*20)/20] = 1
            self.x = 100
            self.y = 0
            self.current_shape = Shape()
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.draw_blocks(painter)
        self.draw_shape(painter, self.current_shape)
        painter.end()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Left:
            if self.can_move_left():
                self.x -= 20
        elif event.key() == QtCore.Qt.Key_Right:
            if self.can_move_right():
                self.x += 20
        elif event.key() == QtCore.Qt.Key_Up:
            self.current_shape.rotate_right()
        elif event.key() == QtCore.Qt.Key_Down:
            self.current_shape.rotate_left()
        elif event.key() == QtCore.Qt.Key_Space:
            self.imm_down()
        self.update()

    def draw_shape(self, painter, shape):
        for coord in shape.coordinates:
            painter.fillRect(self.x+coord[0]*20, self.y+coord[1]*20, 20, 20, QtCore.Qt.gray)
            painter.drawRect(self.x+coord[0]*20, self.y+coord[1]*20, 20, 20)

    def can_move_left(self):
        for (x, y) in self.current_shape.coordinates:
            if x*20 + self.x <= 0 or self.blocks[(y*20 + self.y)/20][(x*20 + self.x)/20 - 1] != 0:
                return False
        return True

    def can_move_right(self):
        for (x, y) in self.current_shape.coordinates:
            if x*20 + self.x + 20 >= 200 or self.blocks[(y*20 + self.y)/20][(x*20 + self.x)/20 + 1] != 0:
                return False
        return True

    def can_move_down(self):
        for (x, y) in self.current_shape.coordinates:
            if y*20 + self.y + 20 >= 400 or self.blocks[(y*20 + self.y)/20 + 1][(x*20 + self.x)/20] != 0:
                return False
        return True

    def draw_blocks(self, painter):
        for i in range(20):
            for j in range(10):
                if self.blocks[i][j] != 0:
                    painter.fillRect(j*20, i*20, 20, 20, QtCore.Qt.gray)
                    painter.drawRect(j*20, i*20, 20, 20)

    def imm_down(self):
        while self.can_move_down():
            self.y += 20
        for (x, y) in self.current_shape.coordinates:
            self.blocks[(self.y + y*20)/20][(self.x + x*20)/20] = 1
        self.x = 100
        self.y = 0
        self.current_shape = Shape()


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