import tushare as ts
import pandas as pd
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


'''
使用sklearn.model_selection.train_test_split随机划分训练集和测试集
'''


#获取股票数据，传入参数是股票代码，ktype是数据类型：D日 M月
def get_code_data_df(code,ktype):
    df = ts.get_k_data(code,ktype=ktype).sort_index()
    #把时间格式化
    df['trade_date']=pd.to_datetime(df.index)
    return df


def clean_data_df(df):
    '''
    今天的收盘价减去昨天的收盘价除以昨天的收盘价，就可以算出涨幅
    df.loc[:,'one']#选取one列的数据
    '''
    df.loc[:,'ld_close_future_pct']=df['close'].shift(-1).pct_change(1)#shift(-1)上移一个单位
    df.loc[:,'当前1d涨跌幅']=df['close'].pct_change(1)
    df.dropna(inplace=True)
    #涨幅大于0赋值为1，涨幅小于等于0设置为0
    df.loc[df['ld_close_future_pct']>0,'未来1d涨跌幅方向']=1
    df.loc[df['ld_close_future_pct']<=0,'未来1d涨跌幅方向']=0
    df=df[['当前1d涨跌幅','未来1d涨跌幅方向']]
    return df

#分割训练数据以及预测数据
def split_train_and_test(df):
    #创建特征X和标签y
    y=df['未来1d涨跌幅方向'].values
    X=df.drop('未来1d涨跌幅方向',axis=1).values
    '''train_test_split划分训练集和测试集
    40%的数据用于训练，其后的数据用于预测
    random_state是随机种子数
    '''
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.4,random_state=42)
    return X_train,X_test,y_train,y_test

#分类好的数据放到逻辑回归模型当中去
def logisticRegression(X_train,X_test,y_train,y_test):
    #创建一个逻辑回归分类器
    logreg=LogisticRegression(solver='liblinear')
    #放入训练集数据进行模型训练
    logreg.fit(X_train,y_train)
    #在测试集数据上进行预测
    new_prediction=logreg.predict(X_test)
    #print Prediction:format (new prediction))
    #测算模型的表现：预测对的个数/总个数，返回一个分数
    return (logreg.score(X_test,y_test))

#svm中的svc，前面把涨跌分为了0和1了，SVC用于做二分类
def svm_svc(X_train, X_test,y_train,y_test):
    clf=svm.SVC(gamma='auto')
    clf.fit(X_train, y_train)
    new_prediction=clf.predict(X_test)
   # print ("Prediction:format (new_prediction))
    return (clf.score(X_test,y_test))


#主函数,用于测试模型准确度，传入的code要为字符串类型
def prediction_accuracy(code,ktype="D"):
    #获取数据
    df = get_code_data_df(code, ktype=ktype)
    print(df)
    #处理数据
    df = clean_data_df(df)
    #获取分割数据的结果
    X_train,X_test,y_train,y_test = split_train_and_test(df)
    #计算逻辑回归预测模型结果准确度
    logisticRegression_score = logisticRegression(X_train,X_test,y_train,y_test)
    #计算SVM模型预测结果准确度
    svm_score = svm_svc(X_train, X_test, y_train, y_test)

    return svm_score,logisticRegression_score







