import json

from zhanshop.docker.engineapi import Engineapi

class Images(Engineapi):
    def getList(self):
        """
        获取镜像列表
        @return:
        """
        result = self.request("/images/json")
        return json.loads(result.get('body'))