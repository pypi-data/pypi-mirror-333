# +----------------------------------------------------------------------
# | zhanshop-py    [ 2024/1/1 上午12:00 ]
# +----------------------------------------------------------------------
# | Copyright (c) 2011~2024 zhangqiquan All rights reserved.
# +----------------------------------------------------------------------
# | Author: Administrator <768617998@qq.com>
# +----------------------------------------------------------------------
import socket

import json
import os
import time

import requests

from zhanshop.app import App
from zhanshop.helper.array import Array
from zhanshop.helper.str import Str
from zhanshop.log import Log


class HttpClient():
    config = None

    def __init__(self):
        self.config = {}
        self.config["timeout"] = 3
        self.config["cookie"] = {}
        self.config["header"] = {"user-agent": 'Mozilla/5.0 (Windows NT 11.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0'}
        self.config["uploadfile"] = {}
        self.config["proxy"] = None
        self.config["debug"] = False

    def setTimeout(self, timeout = 3000):
        self.config["timeout"] = timeout / 1000;

    def debug(self):
        self.config["debug"] = True

    def httpproxy(self, ip,  port,  user = "",  password = ""):
        proxy = ""
        if (user and password):
            proxy += user + ":" + password + "@";
        proxy += ip+":"+str(port)
        self.config["proxy"] = {
                'http': 'http://'+proxy,
                'https': 'http://'+proxy
        }

    def socks5(self, ip,  port,  user = "",  password = ""):
        proxy = ""
        if (user and password):
            proxy += user + ":" + password + "@";
        proxy += ip + ":" + str(port)
        self.config["proxy"] = {
            'http': 'socks5://' + proxy,
            'https': 'socks5://' + proxy
        }

    def setHeader(self, key, val):
        self.config["header"][key] = val

    def setCookie(self, key, val):
        self.config["cookie"][key] = val

    def setUploadFile(self, key, filePath):
        self.config["uploadfile"][key] = (os.path.basename(filePath), open(filePath, 'rb'), 'text/plain')

    def request(self, url, method = 'GET', param = None):
        """
        请求
        @param string url:
        @param string method:
        @param string param:
        @return:
        """
        result = {
            "code": -1,
            "header": {},
            "body": "",
            "runtime": time.time()
        }
        try:
            response = requests.request(method, url, data=param, timeout = self.config["timeout"], headers=self.config["header"], cookies=self.config["cookie"], files = self.config["uploadfile"], proxies=self.config["proxy"])
            result["code"] = response.status_code
            result["header"] = response.headers
            result["body"] = response.text
            result["runtime"] = time.time() - result["runtime"]
        except requests.exceptions.RequestException as e:
            if(e.response == None):
                result["body"] = str(e)
            else:
                result["code"] = e.response.status_code
                result["header"] = e.response.headers
                result["body"] = e.response.text
            result["runtime"] = time.time() - result["runtime"]

        self.debugLog(url, method, param, result)
        return result

    def download(self, url, method = 'GET', savePath = None, param = None):
        result = {
            "code": -1,
            "header": {},
            "body": "",
            "runtime": time.time()
        }
        try:
            with requests.request(method, url, stream=True, data=param, timeout=self.config["timeout"],
                                        headers=self.config["header"], cookies=self.config["cookie"],
                                        files=self.config["uploadfile"], proxies=self.config["proxy"]) as r:
                # 检查请求是否成功
                if r.status_code == 200:
                    # 使用 with 语句打开本地文件，确保文件操作完成后自动关闭
                    with open(savePath, 'wb') as f:
                        # 以块的形式读取文件内容并写入本地文件
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)

                else:
                    result["code"] = r.status_code
                    result["code"] = r.text
        except requests.exceptions.RequestException as e:
            if (e.response == None):
                result["body"] = str(e)
            else:
                result["code"] = e.response.status_code
                result["header"] = e.response.headers
                result["body"] = e.response.text
            result["runtime"] = time.time() - result["runtime"]

        return result

    def chunk(self, url, method, param, callback):
        """
        分块请求
        :param url:
        :param method:
        :param param:
        :param callback:
        :return:
        """
        result = {
            "code": -1,
            "header": {},
            "body": "",
            "runtime": time.time()
        }
        try:
            with requests.request(method, url, stream=True, data=param, timeout=self.config["timeout"],
                                  headers=self.config["header"], cookies=self.config["cookie"],
                                  files=self.config["uploadfile"], proxies=self.config["proxy"]) as r:
                # 检查请求是否成功
                if r.status_code == 200:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            callback(chunk)

                else:
                    result["code"] = r.status_code
                    result["code"] = r.text
        except requests.exceptions.RequestException as e:
            if (e.response == None):
                result["body"] = str(e)
            else:
                result["code"] = e.response.status_code
                result["header"] = e.response.headers
                result["body"] = e.response.text
            result["runtime"] = time.time() - result["runtime"]

        return result

    def unixSocket(self, host, path, method = 'GET', param = "", ChunkCallback = None):
        """
        unixSocket请求
        @param host:
        @param path:
        @param method:
        @param param:
        @param isChunk:
        @return:
        """
        self.config["header"]['Connection'] = 'close'

        data = ""
        if isinstance(param, dict):
            data = json.dumps(param, default=str, ensure_ascii=False)
        self.config["header"]['Content-Length'] = str(len(data))

        headerStr = ''
        for key, value in self.config["header"].items():
            headerStr += key+": "+value+"\r\n";

        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.settimeout(self.config["timeout"])
        # 连接到socket文件
        client.connect(host)

        if method == "POST":
            http_request = method + " " + path + " HTTP/1.1\r\n"+headerStr+"\r\n" + data
        else:
            http_request = method + " " + path + param + " HTTP/1.1\r\n"+headerStr+"\r\n\r\n"
        client.send(http_request.encode('utf-8'))
        # 接收响应
        response = b''
        chunk = client.recv(10240)
        response += chunk
        while chunk:
            chunk = client.recv(10240)
            if (ChunkCallback == None):
                response += chunk
                break
            else:
                if(response != b''):
                    respArr = Str.explode("\r\na", response.decode('utf-8'))
                    httpBody = respArr[len(respArr) - 1]
                    if (len(httpBody) == 0): httpBody = respArr[len(respArr) - 2]
                    ChunkCallback(httpBody)
                    response = b''
                respArr = Str.explode("\r\n", chunk.decode('utf-8'))
                httpBody = respArr[len(respArr) - 1]
                if (len(httpBody) == 0): httpBody = respArr[len(respArr) - 2]
                if(len(httpBody) > 0): ChunkCallback(httpBody)

        # 关闭连接
        client.close()

        if (ChunkCallback == None):
            respArr = Str.explode("\r\n", response.decode('utf-8'))
            first = Str.explode(' ', respArr[0])
            httpCode = first[1]
            httpMsg = first[2]
            httpBody = respArr[len(respArr) - 1]
            if (len(httpBody) == 0): httpBody = respArr[len(respArr) - 2]
            if (len(httpBody) == 0): httpBody = respArr[len(respArr) - 3]
            if (len(httpBody) == 0): httpBody = respArr[len(respArr) - 4]
            header = {}

            del respArr[0]
            del respArr[len(respArr) - 1]
            for key,val in enumerate(respArr):
                if(len(val) > 3):
                    arr = Str.explode(":", val)
                    default = Array.get(arr, 1)
                    if(default != None):
                        header[arr[0]] = (arr[1]).lstrip()

            return {
                "code": httpCode,
                "header": header,
                "msg": httpMsg,
                "body": httpBody
            }

    def debugLog(self, url, method, param, result):
        if(self.config["debug"]):
            App.make(Log).info(
                json.dumps({
                    "url": str(url),
                    "method": str(method),
                    'header': self.config["header"],
                    "param": param,
                    "response": result
                }, default=str, ensure_ascii=False)
            )

