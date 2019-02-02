# -*- coding: utf-8 -*-
"""
获取文章的连接
"""
import random
import requests
from bs4 import BeautifulSoup

#保存url的路径
from spider.initConf import confparams

path = "../resources/articles.txt"
root_url = confparams['rootUrl']
def saveArticles(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3'}

    #构建会话,自动关闭多余连接
    s = requests.session()  # 获取 会话
    s.keep_alive = False  # 保持连接,设为 false
    s.adapters.DEFAULT_RETRIES = 300  # 最大连接 改为300
    rootUrl = root_url+"/article/list/{page}?orderby=UpdateTime"
    url = rootUrl.replace("{page}",str(page))
    #抓取网页
    response = s.get(
        url=url,
        headers = headers,
        timeout=3
    )
    #获取根网页
    soup = BeautifulSoup(response.text,"lxml")
    #获取各个文章标题
    h4 = soup.find_all("h4")[1:]
    #获取各个标题链接,并保存至hrefs
    hrefs = []
    for h4Content in h4:
        href = h4Content.a['href']
        hrefs.append(href)
    #把抓取的url,写入到文件
    with open(path,"a", encoding='utf-8') as f:
        for url in hrefs:
            f.write(url+"\n")
    print("写入第"+str(page)+"页成功")

#抓取 1-4页的链接
def refreshArticles(start=1,end=4):
    with open(path, "w", encoding='utf-8') as f:
        pass
    end = end+1
    for i in range(start,end):
        saveArticles(i)
index = 0
#逐个获取文章链接
def getArticle():
    global  index
    with open(path,"r", encoding='utf-8') as f:
        lines = f.readlines()
        ar = lines[index].strip("\n")
        index +=1
        if len(lines)==index:
            index = 0
        return ar
#获取文章总数
def getCount():
    with open(path,"r", encoding='utf-8') as f:
        lines = f.readlines()
        return len(lines)
