# +----------------------------------------------------------------------
# | zhanshop-ai / array.py    [ 2024/6/5 下午1:15 ]
# +----------------------------------------------------------------------
# | Copyright (c) 2011~2024 zhangqiquan All rights reserved.
# +----------------------------------------------------------------------
# | Author: Administrator <768617998@qq.com>
# +----------------------------------------------------------------------
from zhanshop.helper.str import Str
from zhanshop.json import Json


class Array():
    @staticmethod
    def column(arr, key):
        """
        获取数据中的指定列
        :param key:
        :return:
        """
        result = []
        for val in arr:
            data = val.get(key, None)
            if(data != None): result.append(data)
        return result

    @staticmethod
    def implode(separator, arr):
        string = ''
        for i in arr:
            string += str(i)+separator

        if(string != ""): string = string[0:(len(string) - len(separator))]
        return string

    @staticmethod
    def get(arr, key, default=None):
        """
        获取数组的指定key
        @param arr:
        @param key:
        @return:
        """
        try:
            return arr[key]
        except Exception:
            return default

    @staticmethod
    def unset(arr, key):
        """
        销毁指定key
        @param key:
        @return:
        """
        if(Array.get(arr, key)):
            del arr[key]

    @staticmethod
    def kjsonToArray(arr):
        data = {}
        for k in arr:
            try:
                explode = Str.explode("[", k)
                key = explode[0]
                field = Str.explode("]", explode[1])[0]
                if (data.get(key, None) == None): data[key] = {}
                data[key][field] = arr[k]
                if (isinstance(arr[k], list) or isinstance(arr[k], dict)):
                    data[key][field] = Json.encode(arr[k])
            except Exception:
                pass

        return data

    @staticmethod
    def keys(arr):
        data = []
        for k in arr:
            data.append(k)
        return data

    @staticmethod
    def vals(arr):
        data = []
        for k in arr:
            data.append(arr[k])
        return data

    @staticmethod
    def merge(arr1, arr2):
        arr1.update(arr2)
        return arr1
