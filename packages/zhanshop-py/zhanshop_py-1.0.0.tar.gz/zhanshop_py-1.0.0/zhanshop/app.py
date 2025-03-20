# +----------------------------------------------------------------------
# | zhanshop-py    [ 2024/1/1 上午12:00 ]
# +----------------------------------------------------------------------
# | Copyright (c) 2011~2024 zhangqiquan All rights reserved.
# +----------------------------------------------------------------------
# | Author: Administrator <768617998@qq.com>
# +----------------------------------------------------------------------

from typing import TypeVar, Callable

T = TypeVar('T')
class App():
    instances = {}

    @staticmethod
    def make(className: T) -> T:
        """
        构建单例实例
        @param className:
        @return:
        """
        classStr = className.__module__
        if classStr not in App.instances:
            obj = className()
            App.instances[classStr] = obj
            return obj
        else:
            return App.instances[classStr]