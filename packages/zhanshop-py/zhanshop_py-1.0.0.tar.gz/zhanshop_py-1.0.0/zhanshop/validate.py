# +----------------------------------------------------------------------
# | zhanshop-py    [ 2024/1/1 上午12:00 ]
# +----------------------------------------------------------------------
# | Copyright (c) 2011~2024 zhangqiquan All rights reserved.
# +----------------------------------------------------------------------
# | Author: Administrator <768617998@qq.com>
# +----------------------------------------------------------------------
from urllib.parse import urlparse

from zhanshop.error import Error


class Validate():
    request = {}
    rules = None
    message = {}
    data = {}
    errors = []
    def __init__(self, request, rules, message = {}):
        self.errors = []
        """
        构造方法
        :param request: 请求对象
        :param rules: 验证字段规则
        :param message: 验证字段说明
        """
        if(request.is_json):
            self.request = request.get_json()
        elif(request.method == "POST"):
            self.request = request.form
        else:
            self.request = request.args

        self.rules = rules
        self.message = message
        for key in rules:
            val = rules[key]
            functions = val.split(" | ")
            for value in functions:
                function = value.split(':')
                name = function[0]
                if(name == ""): name = "empty"
                min = "0"
                max = "0"
                length = len(function)
                if(length == 3):
                    min = function[1]
                    max = function[2]
                elif(length == 2):
                    min = function[1]
                data = self.getParam(key, None)
                self.data[key] = data
                #通过字符串调用一个函数
                getattr(self, name)(key, data, min, max)


    def getData(self):
        """
        获取字段数据
        @return:
        """
        if (self.errors):
            error = ','.join(str(i) for i in self.errors)
            Error.setError(error, 99999)

        return self.data
    def getParam(self, key, val):
        """
        获取参数
        @param key:
        @param val:
        @return:
        """
        return self.request.get(key, val)

    def required(self, key, data, min, max):
        """
        不能为空的验证
        :param key:
        :param data:
        :param min:
        :param max:
        :return:
        """
        if(data == None or data == ""):
            self.errors.append(self.message.get(key, key) + "不能为空")

    def max(self, key, data, min, max):
        """
        最大值验证
        :param key:
        :param data:
        :param min:
        :param max:
        :return:
        """
        if (data != None and data != "" and float(data) > float(min)):
            self.errors.append(self.message.get(key, key) + "不能大于"+min)

    def min(self, key, data, min, max):
        """
        最小值验证
        :param key:
        :param data:
        :param min:
        :param max:
        :return:
        """
        if (data != None and data != "" and float(data) < float(min)):
            self.errors.append(self.message.get(key, key) + "不能小于"+min)

    def length(self, key, data, min, max):
        """
        长度验证
        :param key:
        :param data:
        :param min:
        :param max:
        :return:
        """
        if (data != None and data != ""):
            length = len(data)
            if(length > int(max)):
                self.errors.append(self.message.get(key, key) + "长度不能大于"+min+"位")
            elif(length < int(min)):
                self.errors.append(self.message.get(key, key) + "长度不能小于"+min+"位")
    def empty(self, key, data, min, max):
        """空验证直接返回值"""
        return data

    def int(self, key, data, min, max):
        """
        接收int类型
        :param key:
        :param data:
        :param min:
        :param max:
        :return:
        """
        if(type(data) != int): self.errors.append(self.message.get(key, key) + "不是一个有效的int类型")
        return data
    def float(self, key, data, min, max):
        if (type(data) != float): self.errors.append(self.message.get(key, key) + "不是一个有效的float类型")

        return data
    def string(self, key, data, min, max):
        if(type(data) != str): self.errors.append(self.message.get(key, key) + "不是一个有效的str类型")

        return data
    def array(self, key, data, min, max):
        if (type(data) != list): self.errors.append(self.message.get(key, key) + "不是一个有效的list类型")

        return data

    def json(self, key, data, min, max):
        if (isinstance(data, dict) == False): self.errors.append(self.message.get(key, key) + "不是一个有效的字典类型")

        return data

    def url(self, key, data, min, max):
        try:
            result = urlparse(data)
            return data
        except ValueError:
            self.errors.append(self.message.get(key, key) + "不是一个有效的url")

    def __del__(self):
        self.request = {}
        self.rules = None
        self.message = None
        self.data = {}
        self.errors = []
