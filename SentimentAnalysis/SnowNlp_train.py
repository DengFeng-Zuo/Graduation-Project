from snownlp import sentiment


#结巴路径 E:\anaconda3\Lib\site-packages\jieba
#snownlp路径 E:\anaconda3\Lib\site-packages\snownlp

#自己准备的常用词词典：stock_words.txt
#jieba.del_word("不开心")可以删除文件中的分词
#jieba.add_word("不开心")可以添加之

'''
能重新训练的模块有seg（分析词性）、sentiments（情感分析）、tag（词性标注）、normal
找到股评文本积极和消极语料库然后训练一下，保存后修改init.py文件中调用的模型路径
具体步骤：
1.首先要找到能够替换数据集的语料集，数据格式要与原来相同，编码方式为utf-8
2.运行train（）函数

'''

#将准备好的负面情感文本集写入snownlp自带的负面情感文本集中，组成新的训练集
def file_neg_add():
    #读取文件
    neg1 = open(r"E:\Graduation Project\Analysis\neg_add.txt",encoding='UTF-8')
    # 逐行写入
    for line in neg1.readlines():
        with open(r"E:\anaconda3\Lib\site-packages\snownlp\sentiment\neg_new.txt", "a", encoding='UTF-8') as neg_new:
            neg_new.write(line)
            neg_new.close()

    neg2 = open(r"E:\anaconda3\Lib\site-packages\snownlp\sentiment\neg.txt",encoding='UTF-8')
    #逐行写入
    for line in neg2.readlines():
        with open(r"E:\anaconda3\Lib\site-packages\snownlp\sentiment\neg_new.txt","a",encoding='UTF-8') as neg_new:
            neg_new.write(line)
            neg_new.close()
    print("新消极情感文本生成完成")

#将准备好的证明情感文本集写入snownlp自带的正面情感文本集中，组成新的训练集
def file_pos_add():
    # 读取文件
    pos1 = open(r"E:\Graduation Project\Analysis\pos_add.txt", encoding='UTF-8')
    # 逐行写入
    for line in pos1.readlines():
        with open(r"E:\anaconda3\Lib\site-packages\snownlp\sentiment\pos_new.txt", "a", encoding='UTF-8') as pos_new:
            pos_new.write(line)
            pos_new.close()

    neg2 = open(r"E:\anaconda3\Lib\site-packages\snownlp\sentiment\pos.txt", encoding='UTF-8')
    # 逐行写入
    for line in neg2.readlines():
        with open(r"E:\anaconda3\Lib\site-packages\snownlp\sentiment\pos_new.txt", "a", encoding='UTF-8') as pos_new:
            pos_new.write(line)
            pos_new.close()
    print("新积极情感文本生成完成")


#生成新的情感文本，只需要运行一次
file_neg_add()
file_pos_add()

#训练新模型，只需要运行一次
#训练完成后，需要修改init.py文件下的marshal名字，替换为新训练出的模型的名字
sentiment.train(r'E:\anaconda3\Lib\site-packages\snownlp\sentiment\neg_new.txt', r'E:\anaconda3\Lib\site-packages\snownlp\sentiment\pos_new.txt')
sentiment.save(r'E:\anaconda3\Lib\site-packages\snownlp\sentiment\new_sentiment.marshal')

