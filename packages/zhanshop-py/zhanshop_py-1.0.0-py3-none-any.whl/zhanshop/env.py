import os
from configparser import ConfigParser

class Env():
    rootPath = ""
    """
    环境变量文件数据 【Python类中定义的成员变量直接就是属于类的静态成员变量】
    """
    data = {}

    """
    载入环境变量
    """

    def init(self, path):
        self.rootPath = path
        env = os.getenv('APP_ENV')
        if env is None: env = 'dev'
        config = ConfigParser()
        config.read(self.rootPath + '/' + env + '.ini', encoding="utf-8")
        configDict = {}
        for section in config.sections():
            for option in config.options(section):
                configDict[section + '.' + option] = config.get(section, option)
        self.data = configDict

    """
    获取环境变量
    """
    def get(self, name, default = None):
        result = os.getenv('PY_'+name)
        if None == result:
            return self.getEnv(name, default)
        return result

    """
    从环境变量文件中读取值
    """
    def getEnv(self, name, default = None):
        result = self.data.get(name)
        if None == result:
            return default
        return result
