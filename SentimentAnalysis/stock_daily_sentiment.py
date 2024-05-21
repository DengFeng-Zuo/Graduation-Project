import sqlite3
import datetime
from SentimentAnalysis.AipNlp import bd_analysis
from SentimentAnalysis.SnowNlp_Analysis import snlp_analysis

now = datetime.datetime.now()
time=now.strftime("%Y%m%d")
#分析出舆情情感倾向并写入数据库，文件名输入为Spider文件夹下的舆情txt文件
def store_daily_sentiment(filename):
    # 创建数据库表的语句

    createInformTableString = """
            CREATE TABLE IF NOT EXISTS {name}(
                informid INTEGER PRIMARY KEY AUTOINCREMENT,
                inform TEXT,
                AN float,
                SN float 
            )""".format(name='news_sentiment'+time)
    conn = sqlite3.connect(r'E:\Graduation Project\Designer\db\StockPrediction.db')
    cur = conn.cursor()
    cur.execute(createInformTableString)
    with open(r"E:\Graduation Project\Spider\{}".format(filename),encoding='gbk') as f:
        lines=f.readlines()
        for line in lines:
            bd_sentiment = bd_analysis(line)
            sn_sentiment = snlp_analysis(line)
            cur.execute("""INSERT INTO {0}
                       (informid,inform,AN,SN) VALUES
                       (NULL,'{1}','{2}','{3}')
                       """.format('news_sentiment'+time,line,bd_sentiment,sn_sentiment))

        print("插入成功")
    f.close()
    conn.commit()
    conn.close()

store_daily_sentiment('600519_stock_inform.txt')