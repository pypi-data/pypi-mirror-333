# +----------------------------------------------------------------------
# | zhanshop-py    [ 2024/1/1 上午12:00 ]
# +----------------------------------------------------------------------
# | Copyright (c) 2011~2024 zhangqiquan All rights reserved.
# +----------------------------------------------------------------------
# | Author: Administrator <768617998@qq.com>
# +----------------------------------------------------------------------
from datetime import datetime
import json
import logging

from zhanshop.app import App
from zhanshop.env import Env


class JSONFormatter(logging.Formatter):
    def format(self, record):
        record.msg = json.dumps(record.msg)
        return super().format(record)

class Log():
    app = None
    dataof = None
    logger = None
    def setApp(self, app):
        """
        设置app
        :param app:
        :return:
        """
        self.app = app
        #app.logger.setLevel(logging.ERROR)
        self.config()

    def config(self):
        """
        配置日志
        :return:
        """
        today = datetime.now().strftime("%Y%m%d")
        dayfile = App.make(Env).rootPath+"/runtime/log/"+today+".log"
        self.dataof = today

        # 创建一个日志记录器
        logger = logging.getLogger('zhanshop')
        logger.setLevel(logging.DEBUG)  # 设置日志级别

        # 创建一个handler，用于将日志写入磁盘文件
        file_handler = logging.FileHandler(dayfile, 'a', 'utf-8')  # 指定日志文件名
        file_handler.setLevel(logging.DEBUG)  # 设置文件handler的级别

        # 创建一个handler，用于将日志输出到控制台
        stream_handler = logging.StreamHandler()  # 输出到控制台
        stream_handler.setLevel(logging.ERROR)  # 设置控制台handler的级别

        # 定义handler的输出格式
        formatter = logging.Formatter('[%(asctime)s]%(message)s')
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        # 将handlers添加到日志记录器
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        self.logger = logger

    def request(self, msg):
        self.save("REQUEST", msg)

    def error(self, msg):
        self.save("ERROR", msg)
    def info(self, msg):
        self.save("INFO", msg)
    def debug(self, msg):
        self.save("DEBUG", msg)
    def warn(self, msg):
        self.save("WARN", msg)

    def sql(self, msg):
        self.save("SQL", msg)
    def save(self, type, msg):
        self.write(logging.DEBUG, '###['+type+']###' + msg)
    def write(self, type, msg):
        nowTime = datetime.now()
        today = nowTime.strftime("%Y%m%d")
        if(today != self.dataof): self.config() # 重新配置
        #print("去写日志")
        self.logger.log(type, msg)

    styles = {
        'success': "\033[0;32m%s\033[0m",
        'error': "\033[31;31m%s\033[0m",
        'info': "\033[33;33m%s\033[0m",
        'debug': "\033[36;36m%s\033[0m",
    }
    @staticmethod
    def echo(msg, style = 'info', newLine = True):
        format = Log.styles.get(style, "\033[33;33m%s\033[0m")

        if (newLine):
            format += "\n";
        print(format % msg, sep=' ', end='');
