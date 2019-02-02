# python3
# 功能：对https://best.zhaopin.com/中的某企业刷点赞
import re
import random
import sys
import time
import datetime
import threading
from random import choice
import requests
import bs4

# 设置user-agent列表，每次请求时，可在此列表中随机挑选一个user-agnet
user_agent = [
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0; Baiduspider-ads) Gecko/17.0 Firefox/17.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9b4) Gecko/2008030317 Firefox/3.0b4",
    "Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; BIDUBrowser 7.6)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko",
]


# 国内高匿代理IP，返回当前页的所有ip
def get_ip_list():
    # 获取代理IP（取当前页的ip列表，每页100条ip）
    url = "http://www.xicidaili.com/nn"
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;",
               "Accept-Encoding": "gzip, deflate, sdch",
               "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
               "Referer": "http://www.xicidaili.com",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
               }
    r = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    data = soup.table.find_all("td")
    # 匹配规则需要用浏览器的开发者工具进行查看
    # 匹配IP：<td>61.135.217.7</td>
    ip_compile = re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>')
    # 匹配端口：<td>80</td>
    port_compile = re.compile(r'<td>(\d+)</td>')
    # 获取所有IP，返回的是数组[]
    ip = re.findall(ip_compile, str(data))
    # 获取所有端口：返回的是数组[]
    port = re.findall(port_compile, str(data))
    # 组合IP+端口，如：61.135.217.7:80
    return [":".join(i) for i in zip(ip, port)]


# 打开页面。执行点赞行为
def do_dz(code=0, ips=[]):
    # 点赞，如果代理IP不可用造成点赞失败，则会自动换一个代理IP后继续点赞
    try:
        # 随机选取一个ip
        ip = choice(ips)
    except:
        return False
    else:
        proxies = {
            "http": ip,
        }
        headers_ = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
            "Referer": "https://best.zhaopin.com/",
            "User-Agent": choice(user_agent),
        }
        # 用浏览器的开发者工具跟踪点赞事件传输的参数值
        datas = {'bestid': 6030, 'source': 'best'}
    try:
        # 点赞网址
        url_dz = "https://best.zhaopin.com/API/Vote.ashx"
        # 执行点赞行为（发送请求）
        r_dz = requests.post(url_dz, headers=headers_, data=datas, proxies=proxies)
    except requests.exceptions.ConnectionError:
        print("Connection Error")
        if not ips:
            print("not ip")
            sys.exit()
        # 删除不可用的代理IP
        if ip in ips:
            ips.remove(ip)
        # 重新请求URL
        get_url(code, ips)
    else:
        # 获取当前时间
        date = datetime.datetime.now().strftime('%H:%M:%S')
        print(u"第%s次 [%s] [%s]：投票%s (剩余可用代理IP数：%s)" % (code, date, ip, r_dz.text, len(ips)))


if __name__ == '__main__':
    ips = []
    # python3把xrange()与rang()e整合为一个range()
    for i in range(5000):
        # 每隔1000次重新获取一次最新的代理IP
        if i % 1000 == 0:
            ips.extend(get_ip_list())
        # 启用线程，隔2秒产生一个线程
        t1 = threading.Thread(target=do_dz, args=(i, ips))
        t1.start()
        # time.sleep的最小单位是毫秒
        time.sleep(2)
