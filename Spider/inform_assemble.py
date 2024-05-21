from Spider.em_stock_inform import get_em_newsdata
from Spider.jrj_stock_inform import get_jrj_newsdata
from Spider.st_stock_inform import get_st_newsdata

#一次性实现抓取舆情信息并整合到股票名_stock_inform.txt文件中
def inform_assemble(code,page):
    get_em_newsdata(code,page)
    get_jrj_newsdata(code,page)
    get_st_newsdata(code,page)
    print("舆情信息抓取完成")

inform_assemble(600519,3)