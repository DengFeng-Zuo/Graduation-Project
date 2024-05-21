from aip import AipNlp

#调用AipNlp对文本数据进行情感分析,参数是文件名
def bd_analysis(line):
    global positive_prob
    """ 你的 APPID AK SK """
    APP_ID = ''
    API_KEY = ''
    SECRET_KEY = ''

    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
    #对非空字符串进行情感分析
    if not line.isspace():
        news_line=line.strip()
    #逐行进行情感倾向分析
    result=client.sentimentClassify(news_line)
    #判断item键值对是否存在，存在则有效
    if "items" in result.keys():
        positive_prob=result["items"][0]["positive_prob"]

    return positive_prob

