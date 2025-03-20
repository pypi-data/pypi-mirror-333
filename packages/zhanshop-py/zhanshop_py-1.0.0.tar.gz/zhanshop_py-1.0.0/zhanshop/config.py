# +----------------------------------------------------------------------
# | zhanshop-py    [ 2024/1/1 上午12:00 ]
# +----------------------------------------------------------------------
# | Copyright (c) 2011~2024 zhangqiquan All rights reserved.
# +----------------------------------------------------------------------
# | Author: Administrator <768617998@qq.com>
# +----------------------------------------------------------------------

import config


class Config():
    map = {}

    """
    载入配置
    """
    def __init__(self):
        attributes = dir(config)
        for item in attributes:
            if "__" not in item:
                Config.map[item] = getattr(config, item)

    """
    获取配置
    """
    def get(self, name, default=None):
        array = name.split('.')
        config = Config.map
        for key in array:
            config = config.get(key)
            if config is None:
                break

        if config is None:
            return default
        return config