# -*-coding:utf-8 -*-
"""
jacktu
create 2019-01-02
"""
import random

ua_path = "../resources/user-agent.txt"
ua_list = []

#加载文件,去除其中 #开头,去除每行的 \n 和 空格
def loadConf(path):
    result = []
    with open(r""+path,'r',encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip("\n ")
        if line[0] != "#":
            result.append(line)
    return result

def getheaders(ua_list):
    ua = random.choice(ua_list)
    headers = {'User-Agent': ua}
    return headers
def fullheader(ua):
    return {'User-Agent': ua}
# from spider.user_gent import loadConf, ua_path, getheaders, ua_list
# ua_list = loadConf(ua_path)
# getheaders(ua_list)
