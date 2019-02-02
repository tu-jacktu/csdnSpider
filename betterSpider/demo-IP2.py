from urllib import request

import requests
from bs4 import BeautifulSoup

proxies = {'http': '120.236.128.201:8060',
           'https': '120.236.128.201:8060'  }
url="https://ip.cn/"
header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
req= requests.get(url, headers=header, proxies=proxies, timeout=5)
html=req.text
soup=BeautifulSoup(html,'lxml')
print(soup.text)
