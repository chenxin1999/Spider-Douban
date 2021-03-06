# -*-coding:utf-8-*-
# 参考原文：https://blog.csdn.net/qiang12qiang12/article/details/81082675

import urllib.request
from bs4 import BeautifulSoup


def getHtml(url):
    """获取url页面"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3607.0 Safari/537.36'}
    req = urllib.request.Request(url, headers=headers)
    req = urllib.request.urlopen(req)
    content = req.read().decode('utf-8')
    return content


def getComment(url):
    """解析HTML页面"""
    html = getHtml(url)
    soupComment = BeautifulSoup(html, 'html.parser')

    comments = soupComment.findAll('span', 'short')
    onePageComments = []
    for comment in comments:
        # print(comment.getText()+'\n')
        onePageComments.append(comment.getText()+'\n')
    return onePageComments


def getShowComment(url):
    """解析HTML页面"""
    html = getHtml(url)
    count = 1
    soupComment = BeautifulSoup(html, 'html.parser')

    comments = soupComment.findAll('span', 'short')
    onePageComments = []
    for comment in comments:
        # print(comment.getText()+'\n')
        onePageComments.append(str(count) + '.' + comment.getText()+'\n\n')
        count = count + 1
    return onePageComments


def writeData(subject):
    f = open('./static/text/Comments.txt',      
             'w', encoding='utf-8')     # 注意：相对路径是相对于 app.py 的(因为该函数在 app.py 中被调用)
    f1 = open('./static/text/showComments.txt',
              'w', encoding='utf-8')
    for page in range(1):  # 豆瓣爬取多页评论需要验证。
        url = 'https://movie.douban.com/subject/' + subject + '/comments?start=' + \
            str(20*page) + '&limit=20&sort=new_score&status=P'
        print('第%s页的评论:' % (page+1))
        print(url + '\n')

        for i in getComment(url):
            f.write(i)
            print(i)
        print('\n')

        for i in getShowComment(url):
            f1.write(i)
