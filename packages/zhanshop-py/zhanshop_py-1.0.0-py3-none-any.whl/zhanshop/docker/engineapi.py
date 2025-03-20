import json
import socket
import urllib

import requests

from zhanshop.env import Env
from zhanshop.app import App
from zhanshop.helper.str import Str


class Engineapi():
    def request(self, path, method = "GET", data = {}, isChunk = True):
        dockerUnix = App.make(Env).get('docker.host', "/var/run/docker.sock")
        dockerHost = dockerUnix
        if('http' not in dockerUnix):
            return self.socketRequest(path, method, data, isChunk)
        else:
            return self.httpRequest(dockerHost+path, method, data, isChunk);

    def httpRequest(self, path, method = "GET", data = {}, isChunk = True):
        if (method == "POST"):
            response = requests.post(path, json=data, timeout=5)
        else:
            response = requests.get(path, json=data, timeout=5)
        return {
            "code": response.status_code,
            "msg": 'xxx',
            "body": json.dumps(response.json(), default=str, ensure_ascii=False)
        }

    def socketRequest(self, path, method = "GET", data = {}, isChunk = True):
        """
        dockerUnix请求
        @param path:
        @param method:
        @param data:
        @return:
        """
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        dockerUnix = App.make(Env).get('docker.host', "/var/run/docker.sock")
        client.settimeout(5.0)
        # 连接到socket文件
        client.connect(dockerUnix)

        if(method == "POST"):
            data = json.dumps(data, default=str, ensure_ascii=False)
            http_request = method + " " + path + " HTTP/1.1\r\nHost: 127.0.0.1\r\nContent-Type: application/json; charset=utf-8\r\nContent-Length: " + str(len(
                data)) + "\r\nConnection: close\r\n\r\n" + data
        else:
            data = urllib.parse.urlencode(data)
            if(len(data) > 0): data = "?"+data
            http_request = method + " " + path +data+ " HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: close\r\n\r\n"

        # 发送HTTP请求
        client.send(http_request.encode('utf-8'))

        # 接收响应
        response = b''
        chunk = client.recv(10240)
        while chunk:
            response += chunk
            chunk = client.recv(10240)
            if(isChunk == False):
                response += chunk
                break
        # 关闭连接
        client.close()

        respArr = Str.explode("\r\n", response.decode('utf-8'))
        first = Str.explode(' ', respArr[0])
        httpCode = first[1]
        httpMsg = first[2]
        httpBody = respArr[len(respArr) - 4]
        if(len(httpBody) == 0): httpBody = respArr[len(respArr) - 2]
        return {
            "code": httpCode,
            "msg": httpMsg,
            "body": httpBody
        }