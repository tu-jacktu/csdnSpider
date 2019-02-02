# -*- coding: utf-8 -*-
import time
import requests
from bs4 import BeautifulSoup
from spider.articles import getArticle,getCount, refreshArticles
from spider.initConf import confparams
from spider.proxies import getIP, getFullProxy, writeIP, saveIP, clearUncheck
from spider.user_gent import getheaders, loadConf, ua_path ,ua_list
from spider.writeLog import mylog
"""
jacktu
create 2019-01-02
"""
visitCount = 0
visitError = 0

#访问博客的方法
def visit(url, headers, p_proxies):
    # 这段,设置自动关闭多余连接,不然容易报 MaxRetryError
    s = requests.session()  # 获取 会话
    s.keep_alive = False  # 保持连接,设为 false
    s.adapters.DEFAULT_RETRIES = 300  # 最大连接 改为300
    mylog.info(["使用的 p_proxies\t" + str(p_proxies), "使用的 headers\t" + str(headers)])
    response = s.get(
        url,
        # "http://httpbin.org/get",
        proxies=p_proxies,
        headers=headers,
        timeout=3  # 请求超时时间,跟你网速有关
    )
    soup = BeautifulSoup(response.text, "lxml")  # 使用 BeautifulSoup 抓取内容
    # title = soup.find_all("h1", class_="title-article")
    readCount = soup.find_all("span", class_="read-count")
    if len(readCount)>0:
        readCount = readCount[0].get_text()
    global visitCount
    visitCount += 1
    print("链接:" + url, "页面标题:" + str(soup.title.text), sep="\t")
    print("阅读数:" + str(readCount),"总共成功访问:" + str(visitCount), sep="\t")
    mylog.info(["链接:" + str(url), "页面标题:" + str(soup.title.text), "阅读数:" + str(readCount),
                "总共成功访问:" + str(visitCount), "------------------------"])

def visitBlob(xiciPage):
    global visitError
    try:
        # sleep(x)
        ip = getIP(xiciPage)
        visit(getArticle(), getheaders(ua_list), getFullProxy(ip))
        writeIP(ip)
        for i in range(0, getCount()):
            visit(getArticle(), getheaders(ua_list), getFullProxy(ip))
    except Exception as e:
        visitError += 1
        if not visitError%10==0:
            print("f-" + str(visitError),end="\t")
        else:
            print("fail:" + str(visitError),e.args)
        mylog.warning(["fail:" + str(visitError), str(e.args)])
print("初始化配置参数")
startArticle = int(confparams['startArticle'])
endArticle = int(confparams['endArticle'])
xiciPage = int(confparams['xiciPage'])
nightSleep = int(confparams['nightSleep'])

print("初始化 user-gent")
ua_list = loadConf(ua_path)

refreshArticles(startArticle,endArticle)
clearUncheck()
saveIP(xiciPage)

while True:
    hour = int(time.strftime("%H", time.localtime()))
    if (hour<7 & hour>23):#时间判断,晚上降低频率
        time.sleep(nightSleep)
        visitBlob(xiciPage)
    else:
        visitBlob(xiciPage)




