#-*- coding:utf-8 -*-
import _thread
import  requests
from bs4 import BeautifulSoup
from spider.user_gent import getheaders, ua_list, fullheader

"""
jacktu
create 2019-01-02
"""
unIP_path = "../resources/uncheckip.txt"
IP_path = "../resources/ip.txt"
# 爬取西刺https的代理IP,保存至 uncheckip.txt
def saveIP(num_page=5):
    print("正在写入代理:")
    for i in range(1,num_page+1):#抓取 1-num_page 页的代理
        url = "https://www.xicidaili.com/wn/" + str(num_page) # 构建爬取的页面URL
        try:
            response = requests.get(url, headers=fullheader('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50'))
            soup = BeautifulSoup(response.text,'lxml')#'lxml'参数,把 r.text 作为网页处理
            trs = soup.find_all('tr')#获取所有 <tr></tr> 元素
            print(i,end=",")
            for i in range(1,len(trs)):
                tr = trs[i]
                tds = tr.find_all('td')
                ip_item = tds[1].text + ':' + tds[2].text
                with open(r""+unIP_path, 'a', encoding='utf-8') as f:# 追加 内容,不存在则创建
                    f.writelines(ip_item + '\n')
        except Exception as e:
            print("访问"+url+" 失败",e.args)
def getFullProxy(ip):
    return {
            'http': 'http://' + ip,  # 处理http连接的
            'https': 'https://' + ip,  # 处理https连接的
        }
#检测IP是否可用,可用返回该IP代理
def check(ip_port):
    try:
        proxy = ip_port.replace('\n', '').replace(" ","")
        proxies =getFullProxy(proxy)
        # 这段,设置自动关闭多余连接,不然容易报 MaxRetryError
        s = requests.session()  # 获取 会话
        s.keep_alive = False  # 保持连接,设为 false
        s.adapters.DEFAULT_RETRIES = 300  # 最大连接 改为300
        response = s.get(
            "https://www.taobao.com/",
            proxies=proxies,
            headers={'User-Agent': "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50"},
            timeout=10  # 请求超时时间,跟你网速有关
        )
        return proxies
    except Exception as e:
        return 0
#保存check 通过的ip
def writeIP(ip):
    # with open(r"" + IP_path, 'a+', encoding='utf-8') as f:
    #     if f.readlines().count(ip) < 1:
    #         f.write(ip+"\n")
    #     else:
    #         print('已有该IP')
    pass
#逐个检测IP
def check_ip():
    num = 0
    content = ""
    with open(r"" + unIP_path, 'r', encoding='utf-8') as f:
        content = f.readlines()
    for ip in content:#把检测通过的 ip 写入文件
        num += 1
        res = check(ip)
        if res!=0:
            print("\n"+ip+"successful")
            writeIP(ip)
        else:
            print(num,end=",")

def clearfile(path):#清空文件
    with open(path,"w") as f:
        pass
def clearUncheck():
    clearfile(unIP_path)

"""对外提供"""
index = 0
#逐个获取IP
def getIP(num_page=5):
    global  index
    with open(r""+unIP_path,"r", encoding='utf-8') as f:
        lines = f.readlines()
        ip = lines[index].strip("\n")
        index +=1
        if len(lines) <= index:
            print('当前 index'+str(index), 'max'+str(len(lines)),"重置IP")
            index = 0
            clearUncheck()
            saveIP(num_page)
        elif len(lines)==0:
            saveIP(num_page)
        return ip
def link():
    getFullProxy()
    saveIP()



