#coding=utf-8
from urllib import request
import re

class Spider():
    #我要爬取的链接
    start_url = "https://blog.csdn.net/weixin_42144379/article/details/85332330"
    # 目标内容的正则
    regex = '<h1 class="title-article">([\s\S]*?)</h1>'

    #抓取内容,默认 url 参数为 start_url
    def getContent(self,url = start_url):
        #发送请求,获取请求数据
        source = request.urlopen(self.start_url)
        #读取请求数据,直接读取的是 byte
        html = source.read()
        #把读取的数据转为 utf-8 字符串
        html = str(html, encoding="utf-8")
        #打印抓取的网页
        print(html)
        return html

    def parse(self,url=start_url):
        #调用上的方法,抓取网页
        html = self.getContent(url)
        #使用正则,抓取标题
        title = re.findall(self.regex,html)
        #打印标题,re.findall 获取的是一个 list
        print(title)
#实例化爬虫,运行程序
Spider().parse()