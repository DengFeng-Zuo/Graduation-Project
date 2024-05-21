from snownlp import SnowNLP
from snownlp import sentiment
import jieba

#调用准备好的jieba分词词典
jieba.load_userdict(r"E:\Graduation Project\SentimentAnalysis\stock_words.txt")
def snlp_analysis(line):
    # 加载自己准备的常用词词典(分词词典)
    s = SnowNLP(line.strip())
    return s.sentiments


