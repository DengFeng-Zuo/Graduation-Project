import akshare as ak
import mplfinance as mpf
import pandas as pd
import cv2

##设置输出窗口显示的最多行数，超过则将多余数据用省略号表示
pd.set_option('display.max_rows', 20000)
#是设置输出窗口显示的最多列数，超过则将多余的列用省略号表示
pd.set_option('display.max_columns', 100)
#设置输出窗口显示的最大宽度，如果一行数据的宽度多余所设置的最大宽度会
pd.set_option('display.width', 20000)


#日期格式:年月日 例如：20220418
def stock_history_plot(code, sd, ed):
    # "stock_zh_a_hist" A股日频率数据-东方财富
    #symbol为股票代码 两个date为起止日期
    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=str(code), start_date=str(sd),end_date=str(ed))
    #提取出画图需要的数据
    stock_daily_zh_df=stock_zh_a_hist_df[["日期","开盘","最高", "最低", "收盘", "成交量"]]
    # 格式化列名，用于之后的绘制
    stock_daily_zh_df.rename( columns={
                '日期': 'Date', '开盘': 'Open',
                '最高': 'High', '最低': 'Low',
                '收盘': 'Close', '成交量': 'Volume'},
                inplace=True)
    #转化日期格式
    stock_daily_zh_df['Date'] = pd.to_datetime(stock_daily_zh_df['Date'])
    # 将日期列作为行索引
    stock_daily_zh_df.set_index(['Date'], inplace=True)
    # 使用mplfinance库绘图
    s = mpf.make_mpf_style(base_mpf_style='yahoo', rc={'font.family': 'SimHei', 'axes.unicode_minus': 'False'})

    mpf.plot(stock_daily_zh_df, type='candle', ylabel="price", style=s, title=str(code)+"在"+str(sd)+"至"+str(ed)+'期间的蜡烛图附5&10日均线',
             mav=(5, 10), volume=True, ylabel_lower="volume(shares)",savefig="E:\Graduation Project\Designer\img\\{}".format(code),
             figratio=(13,8),figscale=0.8)


    img = cv2.imread("E:\Graduation Project\Designer\img\\{}.png".format(code))
    crop_img = img[0:440, 115:747]
    cv2.imwrite("E:\Graduation Project\Designer\img\\new_{}.png".format(code), crop_img)
