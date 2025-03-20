# +----------------------------------------------------------------------
# | zhanshop-ai / file.py    [ 2024/6/6 下午2:10 ]
# +----------------------------------------------------------------------
# | Copyright (c) 2011~2024 zhangqiquan All rights reserved.
# +----------------------------------------------------------------------
# | Author: Administrator <768617998@qq.com>
# +----------------------------------------------------------------------
import os
import time
from datetime import datetime
import random

import requests
from qiniu import Auth

from zhanshop.app import App
from zhanshop.config import Config
from zhanshop.env import Env
from zhanshop.error import Error


class File():
    @staticmethod
    def getContents(path, code='utf-8'):
        """
        读取文件
        :param path:
        :return:
        """
        try:
            with open(path, "r", encoding=code) as file:
                content = file.read()
            return content
        except Exception:
            return False

    @staticmethod
    def putContents(path, content, code='utf-8'):
        """
        写入文件
        @param path:
        @param content:
        @param code:
        @return:
        """
        with open(path, "w", encoding=code) as file:
                file.write(content)

    @staticmethod
    def uploadToken(type, expireTime=600):
        accessKey = App.make(Config).get("sns.qiniu.access_key")
        secretKey = App.make(Config).get("sns.qiniu.secret_key")
        if (accessKey == None or secretKey == None): Error.setError("qiniu的access/secret配置参数未定义")
        # 构建认证对象
        qiniu = Auth(accessKey, secretKey)
        # 要上传的空间
        bucket = App.make(Config).get("sns.qiniu.buckets." + type)
        if (bucket == None): Error.setError("qiniu配置bucket " + type + "参数未定义")

        return {
            "token": qiniu.upload_token(bucket["bucket"], expires=expireTime),
            "domain": bucket["domain"],
        }

    @staticmethod
    def uploadQiniu(token, domain, filePath):
        """
        上传到七牛
        @param token:
        @param filePath:
        @return:
        """
        url = 'http://upload.qiniup.com/'  # 这里替换为你的上传地址
        # 使用files参数上传文件
        files = {'file': open(filePath, 'rb')}
        suffix = filePath.split(".")[-1]
        currentDate = datetime.now().date()
        newFilePath = currentDate.strftime('%Y%m%d') + '/' + str(os.getpid()) + str(time.time()) + str(
            random.randint(0, 10000)) + "." + suffix
        postdata = {
            'token': token,
            'key': newFilePath
        }
        response = requests.post(url, files=files, data=postdata)
        jsonData = response.json()
        return domain + '/' + jsonData['key']

    @staticmethod
    def getNewFilePath(suffix='png', saveDir='/runtime/file/') -> str:
        """
        生成一个新的文件名
        @param fileName:
        @return:
        """
        rand = str(random.randint(0, 10000))
        return App.make(Env).rootPath + saveDir + str(os.getpid()) + str(time.time()) + rand + "." + suffix

    @staticmethod
    def exists(path):
        """
        判断一个文件是否存在
        @param path:
        @return:
        """
        if os.path.exists(path):
            return True
        else:
            return False

    @staticmethod
    def unlink(path):
        """
        删除文件
        :param path:
        :return:
        """
        try:
            os.remove(path)
            return True
        except Exception:
            return False


