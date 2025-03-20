import json
import re

from zhanshop.helper.array import Array
from zhanshop.helper.str import Str


class Annotations():
    docComment = None
    def __init__(self, docComment):
        self.docComment = docComment

    def api(self):
        pattern = r"@api\s+(\w+)\s+(\w+)\s+(.*)"

        # 使用re.search查找匹配项
        match = re.search(pattern, self.docComment)
        if(match != None):
            return [match.group(1), match.group(2), match.group(3)]
        return None
    def apiGroup(self):
        pattern = r"@apiGroup\s+(.*)"
        match = re.search(pattern, self.docComment)
        if (match != None):
            return match.group(1)
        return None

    def apiDescription(self):
        pattern = r"@apiDescription\s+(.*)"
        match = re.search(pattern, self.docComment)
        if (match != None):
            if("\n" in match.group(0)): return ""
            return match.group(1)
        return None

    def apiParam(self):
        pattern = r"@apiParam\s+([a-zA-Z]+)\s+(\S+)\s+(.*)"
        matchs = re.findall(pattern, self.docComment)
        if(matchs != None):
            data = self.listParam(matchs)
            param = {}
            for k,v in enumerate(data):
                if(v['pname'] == None):
                    param[v['name']] = v
                    self.moreParam(param[v['name']]["children"], data, v['name'])
            param = self.paramValues(param)
            return param

        return None

    def apiHeader(self):
        pattern = r"@apiHeader\s+([a-zA-Z]+)\s+(\S+)\s+(.*)"
        matchs = re.findall(pattern, self.docComment)
        if (matchs != None):
            data = self.listParam(matchs)
            param = {}
            for k, v in enumerate(data):
                if (v['pname'] == None):
                    param[v['name']] = v
                    self.moreParam(param[v['name']]["children"], data, v['name'])
            param = self.paramValues(param)
            return param
        return None
    def apiSuccess(self):
        pattern = r"@apiSuccess\s+([a-zA-Z]+)\s+(\S+)\s+(.*)"
        matchs = re.findall(pattern, self.docComment)
        if (matchs != None):
            data = self.listParam(matchs)
            param = {}
            for k, v in enumerate(data):
                if (v['pname'] == None):
                    param[v['name']] = v
                    self.moreParam(param[v['name']]["children"], data, v['name'])
            param = self.paramValues(param)
            return param
        return None
    def apiError(self):
        pattern = r"@apiError\s+([0-9]+)\s+(\S*)"
        matches = re.findall(pattern, self.docComment)
        data = []
        for match in matches:
            data.append({"code": match[0], "description": match[1]})
        return data
    def listParam(self, matches):
        data = []
        for match in matches:
            field = match[1]
            fieldsDefault = Str.explode('=', field)
            fields = fieldsDefault[0]
            default = Array.get(fieldsDefault, 1, None)
            fields = Str.explode('.', fields)
            pidIndex = len(fields) - 2
            pid = Array.get(fields, pidIndex, None)
            fieldIndex = len(fields) - 1
            field = Array.get(fields, fieldIndex, None)
            if(field == pid):
                pid = None
            row = {
                "name": field,
                "pname": pid,
                "type": match[0],
                "required": (True if default == None else False),
                "default": default,
                "description": match[2],
                "children": {}
            }
            data.append(row)
        return data

    def moreParam(self, param, data, id):
        for k,v in enumerate(data):
            if(v.get('pname') == id):
                param[v['name']] = v
                self.moreParam(param[v['name']]['children'], data, v['name'])

    def paramValues(self, json_obj, parent_key=''):
        result = []
        for key, value in json_obj.items():
            item = {
                'name': key,
                'type': value['type'],
                'pname': parent_key if parent_key else None,
                'required': 'required' in json_obj[key] and json_obj[key]['required'],
                'default': json_obj[key].get('default'),
                'description': json_obj[key].get('description')
            }

            if 'children' in json_obj[key] and isinstance(json_obj[key]['children'], dict):
                item['children'] = self.paramValues(json_obj[key]['children'], key)
            else:
                item['children'] = []

            result.append(item)

        return result
