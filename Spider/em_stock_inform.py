import requests
from bs4 import BeautifulSoup

#请求头
header = {
    'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
}
#获取东方财富网的股吧评论数据
#东方财富网是用JS加载的动态网页
#分析抓取后的数据，用bs4来分析数据比较好

def get_em_newsdata(code,page):
    titles = []
    if page>=1:
        for page in range(1, page + 1):
            if page==1:
                url = "http://guba.eastmoney.com/list,{},f.html".format(code)
            if page>1:
                url = "http://guba.eastmoney.com/list,{},f_{}.html".format(code,page)
            response = requests.get(url=url, headers=header)
            response.encoding = response.apparent_encoding
            # 获取网页数据
            res_con = response.text
            #bs解析数据
            soup = BeautifulSoup(res_con, "html.parser")
            for each in soup.find_all('span', 'l3 a3'):
                first = each.select('a:nth-of-type(1)')
                for i in first:
                    title=i.get("title")
                    titles.append(title)
            #将抓取到的title写入文件里
            with open("{}_stock_inform.txt".format(code), "a+",encoding='utf-8') as f:
                for t in titles:
                    if len(t)>16 :
                        f.write(t+"\n")
                f.close()
        page=page-1
    print("get_em_newsdata执行完毕")