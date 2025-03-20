import pymysql
from pymysql import Connection

from zhanshop.app import App
from zhanshop.config import Config
from zhanshop.error import Error
from zhanshop.log import Log


class Connection():
    connect = None
    def __init__(self):
        pass

    def conn(self)->Connection:
        """
        连接到数据库
        :return:
        """
        if(self.connect == None):
            dbconf = App.make(Config).get('database')
            self.connect = pymysql.connect(
             host=dbconf['hostname'],
             user=dbconf['username'],
             password=dbconf['password'],
             db=dbconf['database'],
             port=dbconf['hostport'],
             charset=dbconf['charset'],
             connect_timeout=dbconf.get('conntime', 3),
             read_timeout=dbconf.get('readtime', 5),
             autocommit=dbconf.get('commit', True),
             cursorclass=pymysql.cursors.DictCursor
            )
        return self.connect

    def query(self, sql, multi=True, isRetry=False):
        """
        查询语句
        :param sql:
        :param multi:
        :return:
        """
        result = None
        try:
            with self.conn().cursor() as cursor:
                cursor.execute(sql)
                if(multi):
                    result = cursor.fetchall()
                else:
                    result = cursor.fetchone()
                self.connect = None
        except Exception as e:
            self.conn().close()
            self.connect = None
            errStr = str(e)
            App.make(Log).error(errStr)
            if(isRetry == False):
                self.query(sql, multi, True)
            else:
                Error.setError(errStr)
        return result
    def execute(self, sql, lastid = False, isRetry=False):
        """
        执行sql语句
        :param sql:
        :param lastid:
        :return:
        """
        result = 0
        try:
            with self.conn().cursor() as cursor:
                cursor.execute(sql)
                if (lastid):
                    result = cursor.lastrowid
                else:
                    result = cursor.rowcount
                self.connect = None
        except Exception as e:
            self.conn().close()
            self.connect = None
            errStr = str(e)
            App.make(Log).error(errStr)
            if (isRetry == False):
                self.execute(sql, lastid, True)
            else:
                Error.setError(errStr)
        return result

    def __del__(self):
        if(self.connect != None):
            self.connect.close()
            self.connect = None