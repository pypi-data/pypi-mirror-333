# +----------------------------------------------------------------------
# | zhanshop-py    [ 2024/1/1 上午12:00 ]
# +----------------------------------------------------------------------
# | Copyright (c) 2011~2024 zhangqiquan All rights reserved.
# +----------------------------------------------------------------------
# | Author: Administrator <768617998@qq.com>
# +----------------------------------------------------------------------
import json


class Json():
    @staticmethod
    def encode(data, ascii=False):
        """
        json编码
        :param data:
        :param ascii:
        :return:
        """
        return json.dumps(data, default=str, ensure_ascii=ascii)

    @staticmethod
    def decode(data):
        """
        json编码
        :param data:
        :return:
        """
        return json.loads(data)