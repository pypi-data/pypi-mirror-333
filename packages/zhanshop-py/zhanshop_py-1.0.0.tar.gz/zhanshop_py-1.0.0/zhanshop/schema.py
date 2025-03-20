import os.path

import json

from zhanshop.env import Env
from zhanshop.app import App
from zhanshop.database import Database
from zhanshop.helper.array import Array
from zhanshop.helper.file import File
from zhanshop.helper.str import Str
from zhanshop.json import Json
class Schema():
    @staticmethod
    def create(table):
        old = Schema.oldSchema(table)
        data = Schema.newSchema(table)
        for key,val in data.items():
            oldRow = old.get(key, None)
            if(oldRow != None):
                data[key]["search"] = oldRow.get("search", False)
                data[key]["value"] = oldRow.get("value", {})
                data[key]["in_list"] = oldRow.get("in_list", True)
                data[key]["in_field"] = oldRow.get("in_field", True)
                data[key]["width"] = oldRow.get("width", 120)
                data[key]["value_menu"] = oldRow.get("value_menu", "")
                data[key]["input_type"] = oldRow.get("input_type", "text")
                data[key]["input_maxlength"] = oldRow.get("input_maxlength", 0)
                data[key]["templet"] = oldRow.get("templet", None)
                data[key]["edit"] = oldRow.get("edit", None)
                data[key]["escape"] = oldRow.get("escape", None)
                data[key]["sort"] = oldRow.get("sort", True)
                data[key]["unresize"] = oldRow.get("unresize", None)
                data[key]["event"] = oldRow.get("event", None)
                data[key]["style"] = oldRow.get("style", None)
                data[key]["align"] = oldRow.get("align", "left")
        with open(Env.rootPath+'/app/schema/'+table+'.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return data

    @staticmethod
    def oldSchema(table):
        """
        获取历史表结构
        @param table:
        @return:
        """
        data = {}
        jsonPath = Env.rootPath + "/app/schema/" + table + ".json"
        if(os.path.exists(jsonPath)):
            jsonData = File.getContents(jsonPath)
            data = Json.decode(jsonData)
        return data

    @staticmethod
    def newSchema(table):
        """
        获取最新的表结构
        @param table:
        @return:
        """
        data = {}
        result = App.make(Database).table(table).query("SHOW FULL COLUMNS FROM "+table)
        for row in result:
            maxlength = 0
            types = Str.explode("(", row["Type"])
            if(Array.get(types, 1)):
                num = Str.explode(")", Array.get(types, 1))[0]
                num = Str.explode(",", num)[0]
                maxlength = int(num)

            inputType = "text"
            if(row["Key"] == "PRI" and row['Extra'] == "auto_increment"):
                inputType = "hidden"

            data[row["Field"]] = {
                "field": row["Field"],
                "type": types[0],
                "null": row['Null'].lower(),
                "default": row['Default'],
                "title": row['Comment'],
                "search": False,
                "value": {},
                "in_list": True,
                "in_field": True,
                "width": 120,
                "value_menu": "",
                "input_type": inputType,
                "input_maxlength": maxlength,
                "templet": None,
                "edit": None,
                "escape": None,
                "sort": True,
                "unresize": False,
                "event": None,
                "style": None,
                "align": "left",
            }
        return data

    @staticmethod
    def getTitle(table, default):
        result = App.make(Database).table(table).query("show create table " + table)
        if(result != None):
            createStr = Array.get(result[0], 'Create Table')
            if(createStr == None): return default
            arr = Str.explode("COMMENT='", createStr)
            commit = Array.get(arr, 1, table)
            return Str.explode("'", commit)[0]
        return default
