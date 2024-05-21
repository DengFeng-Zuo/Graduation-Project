from xml import etree
import requests
from lxml import etree


#请求头
header = {
    'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
}
#爬取金融界网站股票相关资讯
#用xpath分析抓取后的数据
def get_jrj_newsdata(code,page):
    # 定位网址
    if page>=1:
        #便利输入的页号
        for page in range(1,page+1):
            if page==1:
                url="http://stock.jrj.com.cn/share,{},ggxw.shtml".format(code)
            else:
                url="http://stock.jrj.com.cn/share,{},ggxw_{}.shtml".format(code,page)
            # 获取网页状态码
            web_code = requests.get(url=url).status_code
            response = requests.get(url=url,headers=header)
            response.encoding = response.apparent_encoding
            #获取网页数据
            res_con =response.text

            #解析网页数据
            html_con=etree.HTML(res_con)
            #lxml解析，提取出newlist下股票新闻标题数据
            news_data=html_con.xpath('//ul[@class="newlist"]/li/span/a/text()')
            #print(news_data)
            #写入文件
            for new in news_data:
                new=new
                with open("{}_stock_inform.txt".format(code),"a+",encoding='utf-8') as f:
                    f.write(new)
            f.close()
        page=page-1
    print("get_jrj_newsdata执行完毕")












