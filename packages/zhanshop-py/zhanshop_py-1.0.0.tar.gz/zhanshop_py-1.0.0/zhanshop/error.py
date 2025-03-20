# +----------------------------------------------------------------------
# | zhanshop-py    [ 2024/1/1 上午12:00 ]
# +----------------------------------------------------------------------
# | Copyright (c) 2011~2024 zhangqiquan All rights reserved.
# +----------------------------------------------------------------------
# | Author: Administrator <768617998@qq.com>
# +----------------------------------------------------------------------

import traceback

from zhanshop.app import App
from zhanshop.controller import Controller
from zhanshop.log import Log


class Error(Exception):
    code = None
    description = None
    data = None
    def __init__(self, code, description):
        self.code = code
        self.description = description

    @staticmethod
    def setError(msg, status=500):
        """
        抛出异常
        @param msg:
        @return:
        """
        raise Error(code=status, description=msg)


    @staticmethod
    def errorHandler(app):
        @app.errorhandler(Exception)
        def error(err):
            code = 500
            if 'code' in dir(err):
                code = err.code
            description = "系统出错,请稍后再试！"

            if 'description' in dir(err):
                description = err.description

            if (code == 500):
                App.make(Log).error(traceback.format_exc())
            return Controller.result(None, code, description)