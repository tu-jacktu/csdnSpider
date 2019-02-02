# -*- coding: utf-8 -*-

#引入requests库,没有安装 请 cmd> pip install requests
import requests

#要使用的代理 IP
#我在西刺上找的,过期了的话自己找过
#西刺: https://www.xicidaili.com/
proxy = "119.101.112.15:9999"
#设置代理
proxies = {
    'http': 'http://' + proxy,      #处理http连接的
    'https': 'https://' + proxy,    #处理https连接的
}
#设置请求头
User_Agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3"
headers = {'User-Agent': User_Agent}
try:
    #这段,设置自动关闭多余连接,不然容易报 MaxRetryError
    s = requests.session()  #获取 会话
    s.keep_alive = False  #保持连接,设为 false
    s.adapters.DEFAULT_RETRIES = 300  #最大连接 改为300
    #打印请求头,代理信息
    print("headers",headers)
    print("proxies",proxies)
    #发起请求
    response = s.get( #不用 s.get( 的话 可以直接用 requests.get(
            #你用浏览器直接访问这个地址,可以看到你的IP
            "http://httpbin.org/get",
            proxies=proxies,
            headers=headers,
            timeout=5
    )
    #打印响应内容,结果有你代理IP的字样就成功了
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print('Error', e.args)
