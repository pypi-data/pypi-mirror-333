import json

from zhanshop.app import App
from zhanshop.docker.engineapi import Engineapi
from zhanshop.docker.network import Network
from zhanshop.error import Error
from zhanshop.helper.str import Str


class Container(Engineapi):
    def getList(self):
        """
        获取容器列表
        @return:
        """
        result = self.request("/containers/json?all=1")
        return json.loads(result.get('body'))
    def create(self, name, image, description, version, cmd = "", env = [], ports = [], volumes = [], cpuShares = 0, memory = 0, network = 'docker_zhanshop-network'):
        """
        创建容器
        @param name:
        @param image:
        @param description:
        @param version:
        @param cmd:
        @param env:
        @param ports:
        @param volumes:
        @param cpuShares:
        @param memory:
        @param network:
        @return:
        """
        App.make(Network).create(network)
        hostConfig = {
            "NetworkMode": network,
            "RestartPolicy": {
                "Name": "always",
                "MaximumRetryCount": 0
            },
            "PortBindings": {},
            "Binds": []
        }
        if(cpuShares): hostConfig["CpuShares"] = cpuShares

        if (memory):
            if (memory < 104857600): memory = 104857600; #最小分配100M内存
            hostConfig["Memory"] = memory

        if(volumes):
            for k,v in enumerate(volumes):
                hostConfig["Binds"].append(v)

        if (ports):
            for k,v in enumerate(ports):
                arr = Str.explode(":", v)
                protocol = Str.explode('/', arr[1])
                hostConfig["PortBindings"][protocol[0] + "/" + protocol[1]] = [{
                    "HostIp": "",
                    "HostPort": arr[0]
                }]

        postData = {
            "Env": env,
            "Hostname": name,
            "Domainname": name,
            "Image": image,
            "ExposedPorts": {},
            "HostConfig": hostConfig,
            "Labels": {
                "description": description,
                "version": version
            }
        }

        if(cmd): postData["Cmd"] = cmd

        result = self.request("/containers/create?name="+name, "POST", postData)
        containersId = json.loads(result.get('body')).get("Id")
        if(containersId == False): Error.setError(result)
        self.start(containersId) # 启动

    def start(self, id):
        """
        启动
        @param id:
        @return:
        """
        self.request("/containers/"+id+"/start", "POST")

    def kill(self, id):
        """
        强制停止容器
        @param id:
        @return:
        """
        self.request("/containers/" + id + "/kill", "PUT")

    def stop(self, id):
        """
        停止容器
        @param id:
        @return:
        """
        self.request("/containers/" + id + "/stop", "POST")

    def restart(self, id):
        """
        重启
        @param id:
        @return:
        """
        self.request("/containers/" + id + "/restart", "POST")

    def delete(self, id):
        """
        删除容器
        @param id:
        @return:
        """
        self.request("/containers/" + id , "DELETE")

    def detail(self, id):
        """
        容器详情
        @param id:
        @return:
        """
        result = self.request("/containers/" + id + '/json', "GET")
        result = json.loads(result.get('body').lower())
        if(result.get("config") != None):
            version = result["config"]["labels"].get("version")
            image = result["config"].get("image")
            if(version == None):
                result["config"]["labels"]["version"] = "latest"
            if(":" not in image):
                result["config"]["image"] += ":latest"
        return result

    def stats(self, id):
        result = self.request("/containers/" + id + '/stats', "GET", {}, False)
        return json.loads(result.get('body'))