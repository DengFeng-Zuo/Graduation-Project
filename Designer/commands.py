from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QEventLoop, QThread, QDateTime
from PyQt5.QtGui import QTextCursor, QPixmap
from PyQt5.QtWidgets import QApplication, QMessageBox
from Prediction.Prediction_plot import *
from Designer.stock_history_plot import *
import time
from Prediction.prediction_test import *
import pyqtgraph as pg
import sqlite3


#信号类，迎来发射标准输出作为信号。实现控制台输出定向到QTextBrowser中
class EmittingStr(QObject):
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))
    QApplication.processEvents()


#槽函数，获取指定日期期间的股票各种数据数据，实现管理员存储舆情数据
def get_stock_history(self):
    stock_code = self.lineEdit.text()
    if (stock_code == ""):
        print(QMessageBox.warning(self, "警告", "股票代码输入不得为空！!", QMessageBox.Yes, QMessageBox.Yes))
        return
    if not (len(str(stock_code))==6):
        print(QMessageBox.warning(self, "警告", "请输入合法的六位数字股票代码！!", QMessageBox.Yes, QMessageBox.Yes))
        return
    start_time = self.startDateEdit.date().toString("yyyyMMdd")
    end_time = self.endDateEdit.date().toString("yyyyMMdd")
    #获取股票历史行情数据
    stock_inform = ak.stock_zh_a_hist(symbol=str(stock_code), start_date=str(start_time), end_date=str(end_time))
    print(stock_inform)

    #实现绘图功能,然后把图片展示在labrl_4上
    stock_history_plot(stock_code, start_time, end_time)
    history_pic = QPixmap("E:\Graduation Project\Designer\img\\new_{}.png".format(stock_code))
    self.label_4.setPixmap(history_pic)

    #如果是管理员，则可以将舆情数据保存在本地数据库
    from Designer.MainWindow import Ui_MainWindow

    if Ui_MainWindow.admin_signal:
        createInformTableString = """
        CREATE TABLE IF NOT EXISTS stock_inform(
            informid INTEGER PRIMARY KEY AUTOINCREMENT,
            inform TEXT
        )"""
        conn = sqlite3.connect(r'E:\Graduation Project\Designer\db\StockPrediction.db')
        cur = conn.cursor()
        cur.execute(createInformTableString)
        with open(r"E:\Graduation Project\Spider\600519_stock_inform.txt") as f:
            lines=f.readlines()
            for line in lines:
                cur.execute("""INSERT INTO stock_inform
                            (informid,inform) VALUES 
                            (NULL,'{0}')
                            """.format(line))
        f.close()
        conn.commit()
        conn.close()

#实现获取当前时间的多线程模块，防止与主线程冲突
class BackendThread(QThread):
    update_date = pyqtSignal(str)

    def run(self):
        while True:
            data = QDateTime.currentDateTime()
            currentTime = data.toString("yyyy-MM-dd hh:mm:ss")
            self.update_date.emit(str(currentTime))
            time.sleep(1)

#用于tab_2的股票预测以及画图
def PredictionPlot(self):
    stock_code = self.lineEdit.text()
    if (stock_code == ""):
        print(QMessageBox.warning(self, "警告", "股票代码输入不得为空！!", QMessageBox.Yes, QMessageBox.Yes))
        return
    if not (len(str(stock_code))==6):
        print(QMessageBox.warning(self, "警告", "请输入合法的六位数字股票代码！!", QMessageBox.Yes, QMessageBox.Yes))
        return
    #预测准确度,展示在前端界面
    svm_score,LR_score=prediction_accuracy(stock_code, ktype="M")
    start_time = self.startDateEdit.date().toString("yyyy-MM-dd")
    end_time = self.endDateEdit.date().toString("yyyy-MM-dd")
    y_predict_yield,y_actually_yield,y_AN_pre,y_SN_pre=Prediction_plot(stock_code, start_time, end_time)

    prediction_information="SVM预测得分是{} 逻辑回归预测得分是{} " \
                           "蓝色线是预测结果 橙色线是实际结果 红色是在最近7天加入舆情信息的预测结果".format(svm_score,LR_score)
    self.label_prediction.setText(prediction_information)

    #画线功能
    self.PredictionPlot.plot(y_predict_yield,title='predict',linewidth=1,pen=pg.mkPen({'color': (0,191,255), 'width': 4}))#蓝色
    self.PredictionPlot.plot(y_actually_yield,title='actual',linewidth=1,pen=pg.mkPen({'color': (255,128,0), 'width': 4}))#橙色
    self.PredictionPlot.plot(y_AN_pre,title='AN_pre',linewidth=1,pen=pg.mkPen({'color': (255,0,0), 'width': 4}))#红色



