import sqlite3
import tushare as ts
import pandas as pd
from sklearn import svm
import numpy as np
import datetime

#设置输出窗口显示的最多行数，超过则将多余数据用省略号表示
pd.set_option('display.max_rows', 20000)
#是设置输出窗口显示的最多列数，超过则将多余的列用省略号表示
pd.set_option('display.max_columns', 100)
#设置输出窗口显示的最大宽度，如果一行数据的宽度多余所设置的最大宽度会
pd.set_option('display.width', 20000)



#绘制预测图像
#参数格式：股票代码 年-月-日
def Prediction_plot(code,startdate,enddate):
    #获取数据
    df=ts.get_k_data(code,startdate,enddate)
    #取的周期是20，每一行会添加20列，代表从前1天到前20天的收盘价
    for i in range(1,21,1):
        df['close - ' + str(i) + 'd'] = df['close'].shift(i)
    #过滤掉控制，会把前20行过滤掉，因为有空值。
    df_20d = df[[x for x in df.columns if 'close' in x]].iloc[20:]#要20天以后的，20天以前的有空值
    df_20d = df_20d.iloc[:,::-1]#得到的数据就是close-20、close-19d...close-1d,close
    #建立模型，连续型的数据应该用SVR做预测
    clf=svm.SVR(kernel='linear')

    train_num=len(df_20d)/2
    #前半部分数据用于训练
    features_train = df_20d[:int(train_num)]
    labels_train = df_20d['close'].shift(-1)[:int(train_num)]

    features_test = df_20d[int(train_num):]#test是预测
    labels_test = df_20d['close'].shift(-1)[int(train_num):]
    # 模型的训练过程
    clf.fit(features_train,labels_train)#用得到的模型做预测
    #用训练后的模型做预测
    predict = clf.predict(features_test)
    #label_test是当日收盘价
    dft = pd.DataFrame(labels_test)
    dft['predict'] = predict #把前面预测的测试集的股价给添加到DataFrame中;
    #Next Close为实际的下一个收盘价，Predict Next Close为预测到的下一个收盘价
    dft = dft.rename(columns = {' close' : 'Next Close', ' predict':' Predict Next Close' })

    #current_close为现在的收盘价，next_open为现在的开盘价
    current_close = df_20d[['close']].iloc[int(train_num):]
    next_open = df[['open']].iloc[int(train_num)+20: ].shift(-1)

    df1 = pd.merge(dft, current_close, left_index=True,right_index=True)
    df2 = pd.merge(df1,next_open,left_index=True, right_index=True)

    #把上面做出的数据拼接起来
    df2.columns = ['Next Close', 'Predicted Next Close', 'Current Close', 'Next Open']

    #股市交易中的”信号“，当预测到的收盘价大于下一个的开盘价的时候，把标签贴为1，否则贴为0
    df2['Signal'] = np.where(df2['Predicted Next Close' ] > df2['Next Open'] ,1,0)
    #如果信号等于1，收益率为下一个收盘价减去下一个开盘价除以下一个开盘价
    df2['PL'] = np.where(df2['Signal'] == 1,(df2['Next Close'] - df2['Next Open'])/ df2['Next Open'],0)
    #算累计收益率，是模型得出来的
    df2['Strategy'] = (df2['PL'].shift(1)+1).cumprod()
    #实际的收益率
    df2['return'] = (df2['Next Close'].pct_change()+1).cumprod()
    #把模型算出的收益率与实际收益率放在同一个dataframe中
    df3=df2[['Strategy', 'return']].dropna()
    df3.plot(figsize=(10,6))

    #获取收益率,大于1为正收益，小于1为负收益
    predict_yield=df3["Strategy"].tolist()
    actually_yield=df3["return"].tolist()

    #提取舆情数据并且进行处理
    now = datetime.datetime.now()
    time = now.strftime("%Y%m%d")
    conn = sqlite3.connect(r'E:\Graduation Project\Designer\db\StockPrediction.db')
    cur = conn.cursor()
    fetchednum=cur.execute("""SELECT count(informid) FROM {name}
                            """.format(name='news_sentiment'+time))
    #获取数据库中的文本条数
    news_count=fetchednum.fetchall()[0][0]

    #获取数据库中AN列
    fetchedAN=cur.execute("""SELECT AN FROM {name}""".format(name='news_sentiment'+time))
    AN_sentiment=fetchedAN.fetchall()
    AN_sentiment_list=[]
    for i in range(news_count):
        AN_sentiment_list.append(AN_sentiment[i][0])

    #获取数据库中SN列
    fetchedSN=cur.execute("""SELECT SN FROM {name}""".format(name='news_sentiment'+time))
    SN_sentiment=fetchedSN.fetchall()
    SN_sentiment_list=[]
    for i in range(news_count):
        SN_sentiment_list.append(SN_sentiment[i][0])

    #以7天为预测时间段，划分数据库中的舆情数据集
    listcount=news_count/7
    listcount=int(listcount)
    #划分AN情感分析结果集
    split_list_AN=[]
    for i in range(0, len(AN_sentiment_list), listcount):
        split_list_AN.append(AN_sentiment_list[i:i + listcount])
    print(split_list_AN)
    #划分SN情感分析结果集
    split_list_SN = []
    for i in range(0, len(SN_sentiment_list), listcount):
        split_list_SN.append(SN_sentiment_list[i:i + listcount])

    #对AN情感结果集进行处理，得到每日的舆情倾向参数
    AN_results=[]
    for lists in split_list_AN:#对split_list_ANs数组中的每组数据进行分析
        AN_pos = 0
        for list in lists:
            if list >0.5:
                AN_pos+=1#统计每组数据中情感倾向为正的条数
        AN_results.append(AN_pos/listcount)#将情感为正的条数除以每组总条数，得到每日情感正向概率

    SN_results = []
    for lists in split_list_SN:
        SN_pos = 0
        for list in lists:
            if list > 0.5:
                SN_pos += 1
        SN_results.append(SN_pos/listcount)

    #影响的天数 8
    sentiment_days=len(AN_results)

    #计算舆情情感倾向正负参数
    SN_sen_days=[]
    AN_sen_days=[]
    #每日情感倾向为正的概率-0.5 除以 每组新闻条数，作为影响股票收益率的参数
    for result in AN_results:
        AN_sen_days.append((result-0.5)/listcount)

    for result in SN_results:
        SN_sen_days.append((result-0.5)/listcount)

    AN_days_list=predict_yield[:]#将未加入舆情信息的预测结果赋值给AN预测结果
    SN_days_list=predict_yield[:]

    for i in range(1,sentiment_days+1):#从数组的最后一位开始，利用前面的AN_sen_days数据来修正预测结果
        AN_days_list[-i]=(AN_days_list[-i]+AN_sen_days[i-1])

    for i in range(1,sentiment_days+1):
        SN_days_list[-i]=SN_days_list[-i]+SN_sen_days[i-1]




    return predict_yield,actually_yield,AN_days_list,SN_days_list





