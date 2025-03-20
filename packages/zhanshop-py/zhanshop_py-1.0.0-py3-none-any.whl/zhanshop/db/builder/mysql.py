from zhanshop.error import Error
from zhanshop.helper.array import Array
from zhanshop.helper.str import Str


class Mysql():
    options = None
    def __init__(self, options):
        self.options = options

    def parseJoin(self, join):
        """
        解析多表关联语句
        @param join:
        @return:
        """
        joinStr = ""
        if(join != None):
            for key in join:
                val = join[key]
                joinStr += ' '.val['type']+" JOIN "
                joinStr += val['table'] + " as "+val['alias']
                joinStr += " ON "+val['condition']
        return joinStr

    def parseWhere(self, where):
        whereStr = ""
        ands = where.get('AND', [])
        for map in ands:
            for key in map:
                whereStr += key+" = '"+Str.addslashes(str(map[key]))+"' AND "
        ins = where.get('IN', [])
        for key in ins:
            whereStr = key+' IN("' + Array.implode('","', ins[key])+'"'+") AND "

        notIns = where.get('NotIN', [])
        for map in notIns:
            for key in map:
                whereStr += key + " NotIN (" + str(map[key]) + ") AND "

        raws = where.get('RAW', [])
        for map in raws:
            whereStr += '('
            whereStr += map[0]
            whereStr += ') AND '

        if (whereStr != ""):
            whereStr = whereStr[0:len(whereStr) - 5]
            whereStr = ' WHERE '+whereStr
        return whereStr
    def parseHaving(self, having):
        return ""
    def parseGroup(self, group):
        groupStr = ""
        if(group): groupStr = " GROUP BY "+group+" ";
        return groupStr

    def parseOrder(self, order):
        orderStr = '';
        if(order):
            orderStr = ' ORDER BY '+Str.addslashes(order)+" "
        return orderStr

    def parseLimit(self, limit):
        limitStr = ""
        if(len(limit)):
            limitStr = " LIMIT "+str(limit[0])
            if(limit[1] > 0): limitStr += ","+str(limit[1])
        return limitStr

    def find(self):
        table = self.options.get('table')
        alias = self.options.get('alias', "")
        if(alias): alias = " AS "+alias+" "
        distinct = self.options.get('distinct', "")
        if(distinct): distinct = " DISTINCT "
        field = self.options.get('field', "*")
        joinStr = self.parseJoin(self.options.get("join"))
        whereStr = self.parseWhere(self.options.get("where"))
        havingStr = self.parseGroup(self.options.get("having"))
        groupStr = self.parseGroup(self.options.get("group"))
        orderStr = self.parseOrder(self.options.get("order"))
        #SELECT * FROMsystem_user WHERE user_name = 'admin' LIMIT 1
        sql = "SELECT"+distinct+" "+field+" FROM "+table+alias+joinStr+whereStr+havingStr+groupStr+orderStr+" LIMIT 1"
        return sql

    def select(self):
        table = self.options.get('table')
        alias = self.options.get('alias', "")
        if (alias): alias = " AS " + alias + " "
        distinct = self.options.get('distinct', "")
        if (distinct): distinct = " DISTINCT "
        field = self.options.get('field', "*")
        joinStr = self.parseJoin(self.options.get("join"))
        whereStr = self.parseWhere(self.options.get("where"))
        havingStr = self.parseGroup(self.options.get("having"))
        groupStr = self.parseGroup(self.options.get("group"))
        orderStr = self.parseOrder(self.options.get("order"))
        limitStr = self.parseLimit(self.options.get("limit"));
        sql = "SELECT" + distinct + " " + field + " FROM " + table + alias + joinStr + whereStr + havingStr + groupStr + orderStr + limitStr
        return sql

    def insert(self):
        data = self.options.get('data')
        sql = ""
        if(len(data) > 0):
            data = data[0]
            field = Array.keys(data)
            field = Array.implode(",", field)
            sql = 'INSERT INTO '+self.options.get('table')+' ('+field+') VALUES ('
            value = Array.vals(data)
            sql += '"'+Array.implode('","', value)+'")'
        return sql
    def update(self):
        data = self.options.get('data')
        whereStr = self.parseWhere(self.options.get("where"))
        sql = ""
        if (len(data) > 0):
            data = data[0]
            setVal = " SET "
            for field,value in data.items():
                setVal += field+'="'+str(value)+'", '
            setVal = setVal[0:len(setVal) - 2]
            sql = 'UPDATE ' + self.options.get('table') + setVal + whereStr
        return sql
    def count(self):
        """
        生成统计sql语句
        :return:
        """
        table = self.options.get('table')
        alias = self.options.get('alias', "")
        if (alias): alias = " AS " + alias + " "
        distinct = self.options.get('distinct', "")
        if (distinct): distinct = " DISTINCT "
        field = self.options.get('field', "*")
        joinStr = self.parseJoin(self.options.get("join"))
        whereStr = self.parseWhere(self.options.get("where"))
        havingStr = self.parseGroup(self.options.get("having"))
        groupStr = self.parseGroup(self.options.get("group"))
        orderStr = self.parseOrder(self.options.get("order"))
        limitStr = self.parseLimit(self.options.get("limit"));
        sql = "SELECT" + " count("+distinct+" "+field+") as count FROM " + table + alias + joinStr + whereStr + havingStr + groupStr
        return sql

    def delete(self):
        """
        删除
        :return:
        """
        whereStr = self.parseWhere(self.options.get("where"))
        if(whereStr == ""): Error.setError("delete必须where条件")

        table = self.options.get('table')
        sql = 'DELETE FROM '+table+whereStr
        return sql
