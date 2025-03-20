import re


class VarChecker():
    @staticmethod
    def isInt(data):
        pass

    @staticmethod
    def isAlphaNumUnderscore(data):
        # 正则表达式匹配变量名
        # ^ 表示开始，[a-zA-Z] 表示任何一个字母，
        # \w 表示字母、数字、下划线，+ 表示一个或多个
        # $ 表示结束
        var_pattern = re.compile(r'^[a-zA-Z]\w+$')
        return bool(var_pattern.match(data))