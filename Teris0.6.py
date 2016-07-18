#coding:utf8
"""
    从这个版本开始，我们把正方形的边长改为20像素，这样看起来清楚些。这次改动需要手工修改代码中每一个为10的地方，把10改为20.
    这样很累，我们会在后面的某个版本把正方形的边长（及其他很多东西）用变量来表示，目前先不动。

    这个版本实现基本的碰撞检测——只检测窗口边缘的碰撞
    如果当前形状碰到底部则停止下落，并生成新的当前形状。

    注意，因为一个正方形的坐标是指其左上角的点，所以检测是否能继续右移和下移时，要留出20像素的余量，这是左上角到最右边或者最下边的距离。
    检测能否继续左移时则不需要

    注：这个版本还有一个bug，当把形状贴到最边上进行变形时，可能会出现形状的一个正方形变到屏幕外边的情形，我们下个版本解决
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
        if self.can_move_down():
            self.y += 20
        else:
            self.x = 100
            self.y = 0
            self.current_shape = Shape()
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
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
            if x*20 + self.x <= 0:
                return False
        return True

    def can_move_right(self):
        for (x, y) in self.current_shape.coordinates:
            if x*20 + self.x + 20 >= 200:
                return False
        return True

    def can_move_down(self):
        for (x, y) in self.current_shape.coordinates:
            if y*20 + self.y + 20 >= 400:
                return False
        return True


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