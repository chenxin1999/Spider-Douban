# -*-coding:utf-8-*-
# 原文：https://blog.csdn.net/qiang12qiang12/article/details/81082675

import matplotlib.pyplot as plt
from wordcloud import WordCloud
from scipy.misc import imread
import jieba
from aip import AipNlp


def sentimentClassify():
    texts = open(
        "/home/shirocheng/Documents/CODE/python-course/spider-douban/app/static/text/Comments.txt", "rb").readlines()

    APP_ID = "15268395"
    API_KEY = "Gc1BixscBwkbcaw8tx6OwxK2"
    SECURITY_KEY = "o3RLCx4x8nA8gkevTnq818WLTnZP2j1C"

    client = AipNlp(APP_ID, API_KEY, SECURITY_KEY)

    f = open('/home/shirocheng/Documents/CODE/python-course/spider-douban/app/static/text/NlpResult.txt',
        'w', encoding='utf-8')
    for text in texts:
        text = str(text, encoding='utf-8')
        result = client.sentimentClassify(text)
        print(result)
        f.write(str(result['text']))
        f.write('\n')
        f.write("积极程度：")
        f.write(str(result['items'][0]["positive_prob"]))
        f.write('\n')
        f.write("消极程度：")
        f.write(str(result['items'][0]["negative_prob"]))
        f.write('\n\n')

def setWordCloud():
    text = open(
        "/home/shirocheng/Documents/CODE/python-course/spider-douban/app/static/text/Comments.txt", "rb").read()

    # 结巴分词
    wordlist = jieba.cut(text, cut_all=True)
    wl = " ".join(wordlist)
    # 设置词云
    wc = WordCloud(background_color="white",  # 设置背景颜色
                   mask=imread(
                       '/home/shirocheng/Documents/CODE/python-course/spider-douban/app/static/img/ic_twitter.jpg'),  # 设置背景图
                   width=1045,
                   height=882,
                   max_words=1000,  # 设置最大显示的字数
                   stopwords=["剧场", "剧场版", "剧情", "不是", "就是", "没有", "看到", "画面", "虽然", "简直", "作品",
                              "一部", "有点", "感觉", "真的", "还是", "这个", "啊啊啊", "粉丝", "真是", "完全", "已经"],  # 设置停用词
                   font_path="/usr/share/fonts/adobe-source-han-sans/SourceHanSansCN-Regular.otf",  # 设置为思源黑体 常规
                   # 设置中文字体，使得词云可以显示（词云默认字体是“DroidSansMono.ttf字体库”，不支持中文）
                   max_font_size=80,  # 设置字体最大值
                   random_state=200,  # 设置有多少种随机生成状态，即有多少种配色方案
                   )
    myword = wc.generate(wl)  # 生成词云
    wc.to_file(
        '/home/shirocheng/Documents/CODE/python-course/spider-douban/app/static/img/result.jpg')
    # 返回评论列表

# # 展示词云图
# plt.imshow(myword)
# plt.axis("off")
# plt.show()
