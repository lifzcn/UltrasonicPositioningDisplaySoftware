"""
# File       : main.py
# Encoding   : utf-8
# Date       ：2023/3/30
# Author     ：LiFZ
# Email      ：lifzcn@gmail.com
# Version    ：python 3.9
# Description：
"""

import sys
import time
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from interface import Ui_Form
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

targetAngle = 0
targetDistance = 0


class mainWindow(QMainWindow, Ui_Form):

    def __init__(self, parent=None):
        super(mainWindow, self).__init__(parent)
        self.setupUi(self)
        self.createItems()
        self.createSignalSlot()
        self.systemInterface()

    def createItems(self):
        self.com = QSerialPort()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(100)

    def createSignalSlot(self):
        self.pushButton_Open.clicked.connect(self.comOpen)
        self.pushButton_Close.clicked.connect(self.comClose)
        self.pushButton_UpdateSerialPort.clicked.connect(self.comRefresh)
        self.com.readyRead.connect(self.receiveData)

    def showTime(self):
        self.label_CurrentTime.setText(time.strftime("%B %d, %H:%M:%S", time.localtime()))

    def receiveData(self):
        try:
            rxData = bytes(self.com.readAll())
            self.lineEdit_TargetPosition.setText(rxData.decode("utf-8"))
            rxDataList = rxData.decode("utf-8").split(',')
            targetAngle = rxDataList[0]
            targetDistance = rxDataList[1]
        except:
            QMessageBox.critical(self, "严重错误", "串口接收数据错误!")

    def comRefresh(self):
        self.comboBox_SerialPortName.clear()
        com = QSerialPort()
        com_list = QSerialPortInfo.availablePorts()
        for info in com_list:
            com.setPort(info)
            if com.open(QSerialPort.ReadWrite):
                self.comboBox_SerialPortName.addItem(info.portName())
                com.close()

    def comOpen(self):
        serialPortName = self.comboBox_SerialPortName.currentText()
        baudRate = int(self.comboBox_BaudRate.currentText())
        self.com.setPortName(serialPortName)
        try:
            if self.com.open(QSerialPort.ReadWrite) == False:
                QMessageBox.critical(self, "严重错误", "串口打开失败!")
                return
        except:
            QMessageBox.critical(self, "严重错误", "串口打开失败!")
            return
        self.pushButton_Close.setEnabled(True)
        self.pushButton_Open.setEnabled(False)
        self.pushButton_UpdateSerialPort.setEnabled(False)
        self.comboBox_SerialPortName.setEnabled(False)
        self.comboBox_BaudRate.setEnabled(False)
        self.label_SerialPortStatement.setText("通信已建立!")
        self.com.setBaudRate(baudRate)

    def comClose(self):
        self.com.close()
        self.pushButton_Close.setEnabled(False)
        self.pushButton_Open.setEnabled(True)
        self.pushButton_UpdateSerialPort.setEnabled(True)
        self.comboBox_SerialPortName.setEnabled(True)
        self.comboBox_BaudRate.setEnabled(True)
        self.label_SerialPortStatement.setText("通信已断开!")

    def close(self):
        sys.exit(app.exec_())

    def systemInterface(self):
        figInit = Figure(figsize=(4, 3), dpi=100)
        self.canvas = FigureCanvas(figInit)
        self.canvas.setParent(self.graphicsView_SystemDisplay)
        figInit.add_subplot(111, polar=True).scatter(targetAngle, targetDistance, color='r')
        scene = QGraphicsScene(self)
        scene.addWidget(self.canvas)
        self.graphicsView_SystemDisplay.setScene(scene)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = mainWindow()
    myWin.show()
    sys.exit(app.exec_())
