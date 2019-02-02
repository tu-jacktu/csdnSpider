# -*- coding: utf-8 -*-
from spider.user_gent import loadConf
"""
jacktu
create 2019-01-02
初始化程序配置
"""
from pathlib import Path

confPath = "../csdn.conf"

def writeConf():
    print("启用默认配置...")
    with open(r"" + confPath, "w+", encoding='utf-8') as f:
        content = """rootUrl=https://blog.csdn.net/weixin_42144379
startArticle=1
endArticle=4
xiciPage=5
nightSleep=30
log=False"""
        f.writelines(content)

if not Path(confPath).exists():
    writeConf()
else:
    exists = True
    with open(r"" + confPath, "r+", encoding='utf-8') as f:
        if len(f.readlines())<1:
            exists = False
    if not exists:
        writeConf()

content = loadConf(confPath)
confparams = {}
for i in content:
    confparams[i.split("=")[0]] = i.split("=")[1]
