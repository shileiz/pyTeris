#coding:utf8
"""
    这个版本实现两个功能：已经落到底的形状的保留；真正的碰撞检测。
    我们用一个二维数组blocks[i][j]来保存所有已经触底的方块。
    我们把整个游戏屏幕划分成 20行x10列 的方格，用blocks[][]来记录每个方格的坐标：blocks[i][j]代表第i列第j行的那个正方形。
    由于我们每个正方形的边长为20，所以第i行第j列那个正方形的左上角坐标应该是 ：(j*20, i*20)
    反之，如果我们知道了一个正方形左上角的坐标为(x, y)，那么他是第几行第几列呢? 答：第 y/20 行, 第 x/20 列，即 blocks[y/20][x/20]
    最后，我们知道了一个shape的当前坐标(self.cur_x, self.cur_y)，如何推算出这个shape中每个正方形的坐标（x, y）？
    答：（x, y） = (self.cur_x + 20*shape.coordinates[0], self.cur_y + 20*shape.coordinates[1])
    我们定义：block[i][j] == 0 表示该方格为空，block[i][j] == 1 表示该方格不空——即被已经触底的方块占据。

    我们做碰撞检测的函数也要做相应的更改。
    例如，检测是否能继续左移时，我们要检测当前形状中的每一个正方形的左边是否已经有方块了。
    假设当前形状中的某一个正方形处于屏幕的第i排第j列，则我们检查第i排，第j-1列是否有方块，即检查blocks[i][j-1] 是否为0
    只有当前形状中的每一个方块的左边都没有方块时，我们才允许其左移。

    最后，我们在每次有形状触底时（即can_move_down()返回False时），都要刷新blocks[][]，把相应的4个正方形置成1。
    并且每次重画的时候（即paintEvent中），要把已经触底的方块都画出来，即把blocks[][]中不为0的正方形都画出来。

    另外，这个版本并没有解决上个版本遗留的问题：当把形状贴到最边上进行变形时，可能会出现形状的一个正方形变到屏幕外边的情形，我们后续再解决
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
        self.update()

    def draw_shape(self, painter, shape):
        for coord in shape.coordinates:
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
                    painter.drawRect(j*20, i*20, 20, 20)


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