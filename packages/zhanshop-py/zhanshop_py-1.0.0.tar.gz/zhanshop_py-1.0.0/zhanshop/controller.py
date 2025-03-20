import json
import time
# +----------------------------------------------------------------------
# | zhanshop-py    [ 2024/1/1 上午12:00 ]
# +----------------------------------------------------------------------
# | Copyright (c) 2011~2024 zhangqiquan All rights reserved.
# +----------------------------------------------------------------------
# | Author: Administrator <768617998@qq.com>
# +----------------------------------------------------------------------

from flask import Response


class Controller():
    @staticmethod
    def result(data, code = 0, msg = 'OK'):
        if (isinstance(data, str) or isinstance(data, int)):
            return data
        else:
            result = {
                'code': code,
                'msg': msg,
                'data': data,
                'time': time.time()
            }
            response = Response(json.dumps(result, default=str, ensure_ascii=False))
            response.headers['Content-Type'] = "application/json; charset=utf-8"
            if(code >= 20000):
                response.status = 417
            elif(code > 504):
                response.status = 200
            elif(code >= 200):
                response.status = code

            return response