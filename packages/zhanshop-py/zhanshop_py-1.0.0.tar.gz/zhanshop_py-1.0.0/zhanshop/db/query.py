from zhanshop.app import App
from zhanshop.db import builder
from zhanshop.db.connection import Connection
from zhanshop.helper.array import Array
from zhanshop.log import Log


class Query():
    table = None
    builder = None
    connection = None
    options = {
        "table": "",
        "data": [],
        "field": "*",
        "where": {
            "AND": [],
            "IN": [],
            "NotIn":[],
            "RAW":[]
        },
        'order': [],
        "limit": []
    }
    def __init__(self, table, type = 'Mysql'):
        self.options = {
            "table": "",
            "field": "*",
            "where": {
                "AND": [],
                "IN": {},
                "NotIn": {},
                "RAW": []
            },
            'order': [],
            "limit": []
        }
        self.options["table"] = table
        className = getattr(builder, type)
        self.builder = className(self.options)
        self.connection = Connection()
        """
        使用getattr来字符串实例化类
        """
    def distinct(self):
        self.options["distinct"] = True
        return self

    def find(self):
        sql = self.builder.find()
        App.make(Log).sql(sql)
        result = self.connection.query(sql, False)
        return result

    def value(self, field):
        """
        查询一行并获取某个值
        :param field:
        :return:
        """
        self.options["field"] = field
        sql = self.builder.find()
        App.make(Log).sql(sql)
        result = self.connection.query(sql, False)
        if(result):
            return result.get(field)
        return None
    def count(self, field="*"):
        pass

    def where(self, map):
        self.options['where']['AND'].append(map)
        return self

    def whereRaw(self, whereStr, bind = None):
        self.options['where']['RAW'].append([whereStr, bind])
        return self
    def field(self, field):
        self.options['field'] = field;
        return self

    def select(self):
        sql = self.builder.select()
        App.make(Log).sql(sql)
        result = self.connection.query(sql, True)
        return result

    def insert(self, data):
        self.options['data'] = [data];
        sql = self.builder.insert()
        App.make(Log).sql(sql)
        result = self.connection.execute(sql, True)
        return result

    def update(self, data):
        self.options['data'] = [data];
        sql = self.builder.update()
        App.make(Log).sql(sql)
        result = self.connection.execute(sql, False)
        return result

    def delete(self):
        sql = self.builder.delete()
        App.make(Log).sql(sql)
        number = self.connection.execute(sql, False)
        return number

    def order(self, orderBy):
        self.options['order'] = orderBy
        return self
    def limit(self, offset, length = -1):
        self.options['limit'] = [offset, length];
        return self

    def whereIn(self, field, values):
        """
        设置in查询
        :param field:
        :param values:
        :return:
        """
        self.options['where']['IN'][field] = values
        return self
    def query(self, sql):
        result = self.connection.query(sql)
        App.make(Log).sql(sql)
        return result

    def execute(self, sql):
        pass

    def finder(self, page=1, limit=20):
        """
        finder列表
        :param page:
        :param limit:
        :return:
        """
        offset = (page - 1) * limit
        self.options['limit'] = [offset, limit]
        sql = self.builder.count()
        App.make(Log).sql(sql)
        total = self.connection.query(sql, False)['count']
        sql = self.builder.select()
        App.make(Log).sql(sql)
        list = self.connection.query(sql, True)
        return {
            "total": total,
            "list": list
        }

    def column(self, field, key):
        """
        获取指定列
        :param field:
        :param key:
        :return:
        """
        self.options["field"] = key+","+field
        list = self.select()
        data = {}
        if(list != None):
            for k,v in enumerate(list):
                data[v[key]] = v[field]
        if(len(data) == 0): return None
        return data


    def __del__(self):
        self.options = {}
