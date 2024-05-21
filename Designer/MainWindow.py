# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QTextCursor
import pandas as pd
import sys
from pyqtgraph import PlotWidget
import pyqtgraph
from Designer.commands import BackendThread, get_stock_history, PredictionPlot, EmittingStr

#设置输出窗口显示的最多行数，超过则将多余数据用省略号表示


pd.set_option('display.max_rows', 20000)
#是设置输出窗口显示的最多列数，超过则将多余的列用省略号表示
pd.set_option('display.max_columns', 100)
#设置输出窗口显示的最大宽度，如果一行数据的宽度多余所设置的最大宽度会
pd.set_option('display.width', 20000)



class Ui_MainWindow(QMainWindow):
    admin_signal = False

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1122, 738)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(80, 5, 80, 10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.horizontalLayout_2.setStretch(0, 3)
        self.horizontalLayout_2.setStretch(1, 2)
        self.horizontalLayout_2.setStretch(2, 3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.startDateEdit = QtWidgets.QDateEdit(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startDateEdit.sizePolicy().hasHeightForWidth())
        self.startDateEdit.setSizePolicy(sizePolicy)
        self.startDateEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.startDateEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2020, 4, 1), QtCore.QTime(0, 0, 0)))
        self.startDateEdit.setDate(QtCore.QDate(2020, 4, 1))
        self.startDateEdit.setObjectName("startDateEdit")
        self.horizontalLayout_3.addWidget(self.startDateEdit)
        self.label_2 = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.endDateEdit = QtWidgets.QDateEdit(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.endDateEdit.sizePolicy().hasHeightForWidth())
        self.endDateEdit.setSizePolicy(sizePolicy)
        self.endDateEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.endDateEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2022, 1, 2), QtCore.QTime(0, 0, 0)))
        self.endDateEdit.setDate(QtCore.QDate(2022, 1, 2))
        self.endDateEdit.setObjectName("endDateEdit")
        self.horizontalLayout_3.addWidget(self.endDateEdit)
        self.getHistoryInfoButton = QtWidgets.QPushButton(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.getHistoryInfoButton.sizePolicy().hasHeightForWidth())
        self.getHistoryInfoButton.setSizePolicy(sizePolicy)
        self.getHistoryInfoButton.setObjectName("getHistoryInfoButton")
        self.horizontalLayout_3.addWidget(self.getHistoryInfoButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.verticalLayout_5.addLayout(self.verticalLayout_3)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.historyInfoBrowser = QtWidgets.QTextBrowser(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.historyInfoBrowser.sizePolicy().hasHeightForWidth())
        self.historyInfoBrowser.setSizePolicy(sizePolicy)
        self.historyInfoBrowser.setObjectName("historyInfoBrowser")
        self.verticalLayout_6.addWidget(self.historyInfoBrowser)
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        # 图片4在label—4处显示，设置它自适应窗口大小
        self.label_4.setScaledContents(True)
        self.verticalLayout_6.addWidget(self.label_4)
        self.verticalLayout_5.addLayout(self.verticalLayout_6)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        #设置绘图控件的参数
        self.PredictionPlot = PlotWidget(self.tab_2)
        self.PredictionPlot.setTitle("股票价格预测", color='008080', size='18pt')
        self.PredictionPlot.setLabel("left", "收益率")
        self.PredictionPlot.setLabel("bottom", "天数")
        #设置背景色
        self.PredictionPlot.setBackground('w')
        # 显示表格线
        self.PredictionPlot.showGrid(x=True, y=True)
        self.PredictionPlot.setGeometry(QtCore.QRect(0, 79, 1109, 561))
        self.PredictionPlot.setObjectName("PredictionPlot")
        self.widget = QtWidgets.QWidget(self.tab_2)
        self.widget.setGeometry(QtCore.QRect(10, 1, 1091, 71))
        self.widget.setObjectName("widget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_prediction = QtWidgets.QLabel(self.widget)
        self.label_prediction.setObjectName("label_prediction")
        self.horizontalLayout_4.addWidget(self.label_prediction)
        self.PredictionButton = QtWidgets.QPushButton(self.widget)
        self.PredictionButton.setObjectName("PredictionButton")
        self.horizontalLayout_4.addWidget(self.PredictionButton)
        self.horizontalLayout_4.setStretch(0, 7)
        self.horizontalLayout_4.setStretch(1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



        # 获取当前时间
        self.backend = BackendThread()
        self.backend.update_date.connect(self.handleDisplay)
        self.backend.start()

        # 输出同步到historyInfoBrowser中去
        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_5.setText(_translate("MainWindow", "TextLabel"))
        self.label.setText(_translate("MainWindow", "      请输入股票代码"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "请输入股票代码"))
        self.label_3.setText(_translate("MainWindow", "时间范围："))
        self.startDateEdit.setDisplayFormat(_translate("MainWindow", "yyyy-M-d"))
        self.label_2.setText(_translate("MainWindow", "-"))
        self.endDateEdit.setDisplayFormat(_translate("MainWindow", "yyyy-M-d"))
        self.getHistoryInfoButton.setText(_translate("MainWindow", "获取"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "历史行情"))
        self.label_prediction.setText(_translate("MainWindow", ""))
        self.PredictionButton.setText(_translate("MainWindow", "预测结果"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "价格预测"))
        self.action.setText(_translate("MainWindow", "更新股票代码"))


        # 按下按钮，触发获取股票数据的槽函数
        self.getHistoryInfoButton.clicked.connect(lambda: get_stock_history(self))
        self.PredictionButton.clicked.connect(lambda: PredictionPlot(self))

    #显示当前时间
    def handleDisplay(self, data):
        self.label_5.setText("当前时间是：" + data)

    #historyInfoBrowser接受信号str的信号槽
    def outputWritten(self, text):
        cursor = self.historyInfoBrowser.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.historyInfoBrowser.append(text)
        self.historyInfoBrowser.setTextCursor(cursor)
        self.historyInfoBrowser.ensureCursorVisible()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())









