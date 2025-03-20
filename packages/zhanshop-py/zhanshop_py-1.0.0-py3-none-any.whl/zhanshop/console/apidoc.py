import importlib
import inspect
import json
import os

from zhanshop.app import App
from zhanshop.env import Env
from zhanshop.hash import Hash
from zhanshop.helper.annotations import Annotations
from zhanshop.helper.file import File
from zhanshop.helper.str import Str


class Apidoc():
    apiPath = 'app/api'
    title = "api文档"
    description = "一键生成基于控制器配置的注解路由"
    def execute(self, server):

        rootPath = App.make(Env).rootPath
        file_list = os.listdir(rootPath+'/'+self.apiPath)
        file_list = sorted(file_list, reverse=True)
        menus = {}
        versions = {}
        for version in file_list:
            controllerPath = App.make(Env).rootPath+'/'+self.apiPath+"/"+version+"/controller"
            controllerList = os.listdir(controllerPath)
            for controller in controllerList:
                if controller.endswith('.py') and not controller.startswith('__'):
                    moduleName = controller[:-3]
                    className = Str.camelize(moduleName)
                    className = className[0].upper() + className[1:]
                    classPath = self.apiPath+"/"+version+"/controller/"+moduleName
                    classPath = classPath.replace("/", ".")
                    print(classPath)
                    module = importlib.import_module(classPath)
                    className = getattr(module, className)
                    for name, func in inspect.getmembers(className, predicate=inspect.isfunction):
                        if(func.__doc__ and "@api" in func.__doc__):
                            menu = self.getMenu(version, moduleName, func)
                            if(menu):
                                menus[menu["group"]] = {
                                    "id": Hash.md5(menu["group"]),
                                    "name": menu["group"],
                                    "pid": 0,
                                    "icon": "mdi mdi-file-word",
                                    "url": "",
                                    "target": "_self"
                                }
                                if(versions.get(menu["url"])):
                                    try:
                                        versions[menu["url"]][menu["method"][0]].append(version)
                                    except Exception:
                                        versions[menu["url"]][menu["method"][0]] = [version]
                                else:
                                    versions[menu["url"]] = {menu["method"][0]: [version]}

                                if(menu.get(menu["url"])):
                                    menus[menu["url"]]["methods"].append(menu["method"][0])
                                else:
                                    menus[menu["url"]] = menu

        apiMenu = []
        for k in menus:
            apiMenu.append(menus[k])

        File.putContents(App.make(Env).rootPath+"/runtime/apidoc/menu.json", json.dumps(apiMenu, default=str, ensure_ascii=False))
        File.putContents(App.make(Env).rootPath + "/runtime/apidoc/version.json",
                         json.dumps(versions, default=str, ensure_ascii=False))

    def getMenu(self, version, moduleName, func):
        an = Annotations(func.__doc__)
        titles = an.api()
        group = an.apiGroup()
        if(titles != None and len(titles)):
            return {
                "id": moduleName+"."+titles[1],
                "name": titles[2],
                "group": group,
                "pid": Hash.md5(group),
                "icon": "",
                "url": "apis/"+moduleName+"/"+titles[1],
                "uri": moduleName+"/"+titles[1],
                "method": [titles[0]],
                "target": "api",
            }
        return None

    def apiMenus(self):
        menus = File.getContents(App.make(Env).rootPath + "/runtime/apidoc/menu.json")
        menus = json.loads(menus)
        return {
            "code": 0,
            "msg": "ok",
            "data": {
                "menu": menus,
                "user": {
                    "user_id": 0,
                    "user_name": "开发者",
                    "avatar": "./images/profile.png"
                }
            }
        }

    def apis(self, request):
        uri = request.json.get("uri")
        menus = File.getContents(App.make(Env).rootPath + "/runtime/apidoc/menu.json")
        menus = json.loads(menus)
        menu = None
        for val in menus:
            if(val.get("uri") == uri):
                menu = val
                break
        memberFunc = ""
        apiDoc = []
        if(menu != None):
            versions = File.getContents(App.make(Env).rootPath + "/runtime/apidoc/version.json")
            versions = json.loads(versions)
            version = versions.get("apis/"+uri)
            if(version != None):
                # 再去获取注释
                for method in version:
                    v = version[method][0]
                    upath = Str.explode("/", uri)
                    classPath = self.apiPath + "/" + v + "/controller/" + upath[0]
                    classPath = classPath.replace("/", ".")
                    module = importlib.import_module(classPath)

                    className = Str.camelize(upath[0])
                    className = className[0].upper() + className[1:]
                    moduleName = getattr(module, className)

                    memberFunc = method.lower()+upath[1].capitalize()
                    for name, func in inspect.getmembers(moduleName, predicate=inspect.isfunction):
                        if(memberFunc == name):
                            if (func.__doc__ and "@api" in func.__doc__):
                                an = Annotations(func.__doc__)
                                titles = an.api()
                                description = an.apiDescription()
                                headers = an.apiHeader()
                                success = an.apiSuccess()
                                error = an.apiError()
                                param = an.apiParam()
                                detail = {
                                    "uri": v + "/" + uri,
                                    "title": titles[2],
                                    "description": description,
                                    "method": method,
                                    "header": headers,
                                    "param": param,
                                    "success": success,
                                    "error": error,
                                    "version": v,
                                    "versions": version[method]
                                }
                                apiDoc.append(detail)
        code = 0
        msg = "ok"
        if(len(apiDoc) == 0):
            code = 500
            msg = memberFunc+" 没有定义任何注释文档"
        return {
            "code": code,
            "msg": msg,
            "data": apiDoc
        }

    def api(self, request):
        uri = request.json.get("uri")
        upath = Str.explode("/", uri)
        method = request.json.get("method")
        classPath = self.apiPath + "/" + upath[0] + "/controller/" + upath[1]
        classPath = classPath.replace("/", ".")

        module = importlib.import_module(classPath)
        className = Str.camelize(upath[1])
        className = className[0].upper() + className[1:]
        moduleName = getattr(module, className)

        memberFunc = method.lower() + upath[2].capitalize()


        detail = None
        for name, func in inspect.getmembers(moduleName, predicate=inspect.isfunction):
            if (memberFunc == name):
                if (func.__doc__ and "@api" in func.__doc__):
                    an = Annotations(func.__doc__)
                    titles = an.api()
                    description = an.apiDescription()
                    headers = an.apiHeader()
                    success = an.apiSuccess()
                    error = an.apiError()
                    param = an.apiParam()
                    detail = {
                        "uri": "/"+uri,
                        "title": titles[2],
                        "description": description,
                        "method": method,
                        "header": headers,
                        "param": param,
                        "success": success,
                        "error": error,
                        "version": upath[0],
                        "versions": []
                    }
        return {
            "code": 0,
            "msg": "ok",
            "data": detail
        }


