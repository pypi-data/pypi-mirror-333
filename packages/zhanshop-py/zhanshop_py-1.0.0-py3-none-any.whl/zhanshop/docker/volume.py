import json

from zhanshop.docker.engineapi import Engineapi

class Volume(Engineapi):
    def getList(self):
        """
        获取数据卷列表
        @return:
        """
        result = self.request("/volumes")
        return json.loads(result.get('body'))