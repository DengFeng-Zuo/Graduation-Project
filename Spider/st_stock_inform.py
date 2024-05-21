
import requests
from bs4 import BeautifulSoup



#请求头
header = {
    'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
}
#存放新闻标题
newslist = []
#爬取股票之星网站股票相关资讯
def get_st_newsdata(code,page):
        # 定位网址
        if page>=1:
            #便利输入的页号
            for page in range(1,page+1):
                if page==1:
                    url="http://news.stockstar.com/info/dstock_{}_c10.shtml".format(code)
                else:
                    url="http://news.stockstar.com/info/dstock_{}_c10_p{}.shtml".format(code,page)
                # 获取网页状态码
                response = requests.get(url=url,headers=header)
                response.encoding = response.apparent_encoding
                #获取网页数据
                res_con =response.text
                soup = BeautifulSoup(res_con, "html.parser")
                #解析网页数据,获取所有a标签中target为_blank的数据
                for each in soup.find_all('a',attrs={"target": "_blank"}):
                    news=each.get_text()
                    #筛选出新闻标题
                    if len(news)>6:
                        newslist.append(news.strip())
            page=page-1
        with open("{}_stock_inform.txt".format(code), "a+",encoding='utf-8') as f:
            for news in newslist:
                f.write(news+"\n")
        print("get_st_newsdata执行完毕")



