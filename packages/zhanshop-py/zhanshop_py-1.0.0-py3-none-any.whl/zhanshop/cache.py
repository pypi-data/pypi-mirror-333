from flask_redis import FlaskRedis

from zhanshop.app import App
from zhanshop.config import Config
from zhanshop.error import Error


class Cache():
    redis = None
    def init(self, app):
        config = App.make(Config).get("cache")
        self.redis = FlaskRedis(app, host=config['host'], port=config['port'], password=config['password'], db=config['db'], socket_timeout=config['socket_timeout'], socket_connect_timeout=config['socket_connect_timeout'])

    def getInstance(self)->FlaskRedis:
        if(self.redis == None): App.make(Error).setError("cache没有建立连接")
        return self.redis