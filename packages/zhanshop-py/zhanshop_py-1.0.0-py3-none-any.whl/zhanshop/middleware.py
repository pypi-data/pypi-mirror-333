# +----------------------------------------------------------------------
# | zhanshop-py    [ 2024/1/1 上午12:00 ]
# +----------------------------------------------------------------------
# | Copyright (c) 2011~2024 zhangqiquan All rights reserved.
# +----------------------------------------------------------------------
# | Author: Administrator <768617998@qq.com>
# +----------------------------------------------------------------------
import json
import time

from flask import request

from zhanshop.app import App
from zhanshop.log import Log


def middleware(app):
    @app.before_request
    def before_request():
        """
        $response->header('Access-Control-Allow-Origin', '*');
        $response->header('Access-Control-Allow-Headers', '*');
        $response->header('Access-Control-Allow-Methods', 'GET, POST, PATCH, PUT, DELETE');
        $response->header('Access-Control-Max-Age', '3600');
        @return:
        """
        """
        前置中间件
        """
        request.headers.set('time', time.time())

    @app.after_request
    def after_request(response):
        """
        后置中间件
        """
        App.make(Log).debug(json.dumps({
            "url": str(request.path),
            "method": str(request.method),
            "ip": str(request.remote_addr),
            "agent": request.headers.get('User-Agent'),
            "token": request.headers.get('token', ""),
            "authorization": request.headers.get('authorization', ""),
            "request": {
                "get": request.args.to_dict(),
                "post": request.form.to_dict(),
                "file": list(request.files.values())
            },
            "response": response.data,
            "runtime": time.time() - request.headers.get('time')
        }, default=str, ensure_ascii=False))
        return response
