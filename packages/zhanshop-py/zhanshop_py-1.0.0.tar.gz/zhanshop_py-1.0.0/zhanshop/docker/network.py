import json

from zhanshop.docker.engineapi import Engineapi


class Network(Engineapi):
    def getList(self):
        """
        列表
        @return:
        """
        result = self.request("/networks")
        return json.loads(result.get('body'))

    def inspect(self, networkId):
        """
        查看详情
        @param networkId:
        @return:
        """
        result = self.request("/networks/"+networkId)
        return json.loads(result.get('body'))

    def create(self, name, driver = "bridge"):
        """
        创建网络
        @param name:
        @param driver:
        @return:
        """
        nets = self.getList()
        for k,v in enumerate(nets):
            if(v.get("Name") == name): return;

        result = self.request('/networks/create', "POST", {
            'name': name,
            "Device": driver
        })["body"]
        return json.loads(result)

    def delete(self, networkId):
        """
        删除网络
        @param networkId:
        @return:
        """
        result = self.request("/networks/"+networkId, "DELETE")["body"]
        #print(result)
        return json.loads(result)