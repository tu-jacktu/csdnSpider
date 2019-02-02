# -*- coding: utf-8 -*-

import logging.handlers

from spider.initConf import confparams


class Log():
    LOG_FILE = r'../log/log.txt'
    open = False
    def log(self):
        # 实例化handler
        handler = logging.handlers.RotatingFileHandler(self.LOG_FILE, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8')
        fmt = '%(asctime)s - %(levelname)s - %(message)s'

        formatter = logging.Formatter(fmt)  # 实例化formatter
        handler.setFormatter(formatter)  # 为handler添加formatter

        logger = logging.getLogger('tst')  # 获取名为tst的logger
        logger.addHandler(handler)  # 为logger添加handler
        logger.setLevel(logging.DEBUG)
        return logger
    def info(self,strMsg):
        if  self.open:
            if (type(strMsg) == str):
                return self.log().info(strMsg)
            elif (type(strMsg) == list):
                msg = ""
                for varStr in strMsg:
                    msg = msg+"\n"+varStr
                return self.log().info(msg)
            else:
                return self.log().warning("传入参数有误!")

    def warning(self, strMsg):
        if self.open:
            if (type(strMsg) == str):
                return self.log().warning(strMsg)
            elif (type(strMsg) == list):
                msg = ""
                for varStr in strMsg:
                    msg = msg + "\n" + varStr
                return self.log().warning(msg)
            else:
                return self.log().warning("传入参数有误!")

    def debug(self, msg, *args, **kwargs):
        if self.open:
            return self.log().debug(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        if self.open:
            return self.log().error(msg, *args, **kwargs)
# model:  info,debug,warning
mylog = Log()
# 设置 log 模式,打开/关闭
str_open = confparams['log']
if str_open=='False' or str_open=='false':
    mylog.open = False
    print("关闭 log")
else:
    mylog.open = bool(str_open)
    print("启用 log")