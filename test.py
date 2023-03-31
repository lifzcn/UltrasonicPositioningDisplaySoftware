import sys
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        # 创建一个 QGraphicsView 控件
        self.graphics_view = QGraphicsView(self)
        self.graphics_view.setGeometry(10, 10, 780, 580)
        self.graphics_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphics_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphics_view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        # 创建一个 Matplotlib 的 FigureCanvasQTAgg 绘图区域
        fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(fig)
        self.canvas.setParent(self.graphics_view)

        # 在 FigureCanvasQTAgg 中绘图
        ax = fig.add_subplot(111, projection='polar')
        t = np.arange(0, 2 * np.pi, 0.01)
        s = np.sin(2 * t)
        ax.plot(t, s)

        # 将 FigureCanvasQTAgg 添加到 QGraphicsScene 中
        scene = QGraphicsScene(self)
        scene.addWidget(self.canvas)
        self.graphics_view.setScene(scene)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
