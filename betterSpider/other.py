# -*- coding:utf-8 -*-
import random
import urllib

import requests
from bs4 import BeautifulSoup

"""
类说明：下在百姓网客户信息
Modify:2018-12-26
"""

class downloader(object):

    def __init__(self):
        self.target = 'http://qingyuan.baixing.com/jiatingzhuangxiu/?query=%E6%A9%B1%E6%9F%9C'
        self.urls = []  # 存放页面链接
        self.cus = []  # 存放客户信息
        self.ip_list = []  # 存放ip地址
        self.proxy_rand = {}

    # 获取代理ip地址列表
    def get_ip_list(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
        url = 'https://www.xicidaili.com/nn/'
        web_data = requests.get(url, headers=headers)
        soup = BeautifulSoup(web_data.text, 'html')
        ips = soup.find_all('tr')
        for i in range(1, len(ips)):
            ip_info = ips[i]
            tds = ip_info.find_all('td')
            self.ip_list.append(tds[1].text + ':' + tds[2].text)

        for ip in self.ip_list:
            try:
                proxy_host = "http://" + ip
                proxy_temp = {"http://": proxy_host}
                res = urllib.request.urlopen(url, proxies=proxy_temp).read()
            except Exception as e:
                self.ip_list.remove(ip)
                continue
        return self.ip_list

    # 从已生成的ip列表随机抽取一个生成代理ip
    def get_random_proxy(self):
        proxy_list = []
        for i in self.ip_list:
            proxy_list.append('http://' + i)
        proxy_ip = random.choice(proxy_list)
        proxy_rand = {"http://": proxy_ip}
        return proxy_rand

    """
    函数说明：获取页面链接
    """

    def url_get(self, proxy_rand):
        try:
            reg = requests.get(url=self.target, proxies=proxy_rand)
            html = reg.text
            all_bf = BeautifulSoup(html)
            div_bf = all_bf.find_all('div', class_='media-body-title')
            for i in div_bf:
                div = i.find_all('a', class_='ad-title')
                for each in div:
                    self.urls.append(each.get('href'))
        except requests.exceptions.ConnectionError as e:
            print('Error', e.args)

    # 使用代理访问获取详情页面客户信息
    def cus_get(self, target, proxy_rand):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
        reg = requests.get(url=target,
                           proxies={'http': 'http://58.218.201.188:58093', 'https': 'https://58.218.201.188:58093'},
                           headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6'}
                           )
        html = reg.text
        print('html',html)
        all_bf = BeautifulSoup(html)
        div = all_bf.find_all('div', class_='viewad-meta2-item')
        a_bf = all_bf.find_all('a', class_='contact-no')
        b_bf = all_bf.find_all('a', class_='show-contact')
        if a_bf != []:
            a = str(a_bf[0].string[0:7])
            b = str(b_bf[0].get('data-contact'))
            lis = [(int(a + b))]
            for i in reversed(div):
                txtlist = i.find_all('span')
                for each in txtlist:
                    txtstr = each.string
                    lis.append(txtstr)
                    tlis = str(lis)
                    stlis = tlis[1:-1]

        else:
            stlis = None
        return stlis

    """
    函数说明：将客户信息写入excel
    """

    def writer(self, detail, path):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(detail + '\n')


if __name__ == '__main__':
    dl = downloader()
    dl.get_ip_list()
    dl.url_get(dl.get_random_proxy())
    for i in dl.urls:
        if dl.cus_get(i, dl.url_get(dl.get_random_proxy())) == None:
            continue
        customer = dl.cus_get(i, dl.url_get(dl.get_random_proxy()))
        print(customer)
        # dl.url_get()
    # for i in dl.urls:
    #     if dl.cus_get(i) == None:
    #         continue
    #     dl.writer(dl.cus_get(i),'d:\demoSpider\河源橱柜.txt')
