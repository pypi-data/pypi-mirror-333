# +----------------------------------------------------------------------
# | zhanshop-py    [ 2024/1/1 上午12:00 ]
# +----------------------------------------------------------------------
# | Copyright (c) 2011~2024 zhangqiquan All rights reserved.
# +----------------------------------------------------------------------
# | Author: Administrator <768617998@qq.com>
# +----------------------------------------------------------------------

import hashlib


class Hash():
    @staticmethod
    def sha1(str):
        """
        sha1加密
        :param str:
        :return:
        """
        sha1 = hashlib.sha1()
        sha1.update(str.encode('utf-8'))
        return sha1.hexdigest()

    @staticmethod
    def md5(str):
        """
        md5加密
        :param str:
        :return:
        """
        md5 = hashlib.md5()
        md5.update(str.encode('utf-8'))
        return md5.hexdigest()