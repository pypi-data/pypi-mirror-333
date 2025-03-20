# +----------------------------------------------------------------------
# | zhanshop-py    [ 2023/1/1 上午12:00 ]
# +----------------------------------------------------------------------
# | Copyright (c) 2011~2023 zhangqiquan All rights reserved.
# +----------------------------------------------------------------------
# | Author: Administrator <768617998@qq.com>
# +----------------------------------------------------------------------
from flask import Flask
from apscheduler.triggers.cron import CronTrigger

import json
import os
import sys
import time
import traceback

from flask import request, redirect, Blueprint
from werkzeug.serving import WSGIRequestHandler
from apscheduler.schedulers.background import BackgroundScheduler

from config.route import route
from zhanshop.app import App
from zhanshop.cache import Cache
from zhanshop.config import Config
from zhanshop.console.apidoc import Apidoc
from zhanshop.controller import Controller
from zhanshop.env import Env
from zhanshop.helper.array import Array
from zhanshop.helper.str import Str
from zhanshop.log import Log


class Server():
    name = "zhanshop"
    type = "http"
    staticFolder = "public"
    config = None
    def __init__(self, name):
        self.name = name
        self.config = {}

    def setConfig(self, key, val):
        self.config[key] = val

    def http(self):
        app = Flask(self.name, static_folder=self.staticFolder, static_url_path="/")
        for k,v in self.config.items():
            app.config[v] = v

        WSGIRequestHandler.server_version = 'zhanshop'
        WSGIRequestHandler.sys_version = ''
        App.make(Log).setApp(app)
        Server.errorhandler(app)
        Server.route(app)
        Server.middleware(app)
        Server.defaultApi(app)
        App.make(Cache).init(app)

        if ("gunicorn" not in sys.orig_argv[1]):
            command = Array.get(sys.orig_argv, 2)
            if (command != None):
                from zhanshop.console.apidoc import Apidoc
                from zhanshop.console.help import Help
                App.make(Config).map["console"]["apidoc"] = Apidoc
                App.make(Config).map["console"]["help"] = Help
                console = App.make(Config).get("console")
                consoleApp = console.get(command, Help)
                (consoleApp()).execute(app)
                return

            Server.crontab()

            app.run(host=App.make(Env).get("server.host", "::"), port=int(App.make(Env).get("server.port", "9021")),
                    debug=Str.toToBool(App.make(Env).get("server.debug", "")))

        return app
    def start(self):

        servType = getattr(self, self.type)
        return servType()

    @staticmethod
    def route(app):
        for router in route:
            if isinstance(router, Blueprint):
                app.register_blueprint(router)


    @staticmethod
    def errorhandler(app):
        @app.errorhandler(Exception)
        def error(err):
            """
            全部异常
            @param err:
            @return:
            """
            code = 500
            if 'code' in dir(err):
                code = err.code

            description = type(err).__name__+":"+str(err)#"系统出错,请稍后再试！"

            if 'description' in dir(err):
                description = err.description

            if (code == 500):
                App.make(Log).error(traceback.format_exc())
            return Controller.result(None, code, description)
    @staticmethod
    def middleware(app):
        """
        中间件处理
        @param app:
        @return:
        """
        @app.before_request
        def before():
            """
            前置中间件
            """
            request.time = time.time()

        @app.after_request
        def after(response):
            """
            后置中间件
            """
            respJson = None
            if(response.default_mimetype == "application/json; charset=utf-8"):
                respJson = response.data
            App.make(Log).request(json.dumps({
                "url": str(request.path),
                "method": str(request.method),
                "ip": str(request.remote_addr),
                "agent": request.headers.get('User-Agent'),
                "token": request.headers.get('token', ""),
                "authorization": request.headers.get('authorization', ""),
                "status": response.status,
                "request": {
                    "get": request.args.to_dict(),
                    "post": request.form.to_dict(),
                    "file": list(request.files.values())
                },
                "response": respJson,
                "runtime": time.time() - request.time
            }, default=str, ensure_ascii=False))
            return response


    @staticmethod
    def crontab():
        crontabs = App.make(Config).get("crontab")
        scheduler = BackgroundScheduler()
        for obj in crontabs:
            scheduler.add_job(getattr(obj, 'execute'), CronTrigger.from_crontab(obj.rule))
        scheduler.start()

    @staticmethod
    def defaultApi(app):
        @app.route('/')
        def index():
            return redirect('/index.html')

        @app.route('/admin')
        def admin():
            return redirect('/admin/index.html')

        @app.route('/admin/')
        def _admin():
            return redirect('/admin/index.html')

        @app.route('/apidoc')
        def apidoc():
            return redirect('/apidoc/index.html')

        @app.route('/apidoc/')
        def _apidoc():
            return redirect('/apidoc/index.html')

        @app.route('/v1/api.doc', methods=['GET', 'POST'])
        def apis():
            if(request.method == "POST"):
                method = request.json.get("_method")
                try:
                    return getattr(App.make(Apidoc), method)(request)
                except Exception:
                    return ""
            else:
                return App.make(Apidoc).apiMenus()

        @app.route('/demo/')
        def demo():
            path = Env.rootPath + "/public/demo"
            domain = path.replace(Env.rootPath + "/public", "")
            suffix = ".html"
            all_files = os.listdir(path)
            # 筛选以指定后缀名结尾的文件
            files = [file for file in all_files if file.endswith(suffix)]

            html = "<html><head><meta charset='UTF-8'><title>demo列表</title></head><body><h1>demo列表</h1><br /><hr /><ul>"
            for key, val in enumerate(files):
                html += "<li><a  target='_blank' href='" + domain +"/"+ val + "'>" + val + "</li>"
            html += "</ul>"
            html += "</body></html>"
            return html



