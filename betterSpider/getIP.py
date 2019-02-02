#-*- coding:utf-8 -*-
import random
import time

import  requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'}
#最近抓取的IP页面
path = "../ip.txt"
#历史抓取的IP页面
pathLog = "../log_ip.txt"
#抓取IP地址,并保存至 ../ip.txt
def saveIP(page):
    for num_page in range(1,page+1):
        # 爬取西刺代理的IP，此处选的是国内https
        url_part = "http://www.xicidaili.com/wn/"
        # 构建爬取的页面URL
        url = url_part + str(num_page)
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            #'lxml'参数,把 r.text 作为网页处理
            soup = BeautifulSoup(r.text,'lxml')
            #获取所有 <tr></tr> 元素
            trs = soup.find_all('tr')
            # 清空最新IP文件
            with open(r"" + path, 'a', encoding='utf-8') as f:
                pass
            for i in range(1,len(trs)):
                tr = trs[i]
                tds = tr.find_all('td')
                ip_item = tds[1].text + ':' + tds[2].text
                # print('抓取第'+ str(page) + '页第' + str(i) +'个：' + ip_item)
                with open(r""+path, 'a', encoding='utf-8') as f:
                    f.writelines(ip_item + '\n')
                with open(r""+pathLog, 'a', encoding='utf-8') as f:
                    f.writelines(ip_item + '\n')
                # time.sleep(1)
            return ('存储成功')
#随机获取文件中的一个IP
def get_ip():
    # with open 与 try...finally 作用一样
    #不论出不出异常都会 关闭文件
    with open(r""+path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        return random.choice(lines)
#检测IP是否可用,可用返回该IP代理
def check_ip():
    proxies = {'HTTPS': 'HTTPS://' + get_ip().replace('\n', '')}
    try:
        r = requests.get('http://httpbin.org/ip', headers=headers, proxies=proxies, timeout=10)
        if r.status_code == 200:
            return proxies
    except Exception as e:
        print(e)

def main():
    saveIP(1) # 抓取第一页，一页100个url
    try:
        return check_ip()
    except Exception as e:
        print(e)
        check_ip()

if __name__ == '__main__':
    main()
