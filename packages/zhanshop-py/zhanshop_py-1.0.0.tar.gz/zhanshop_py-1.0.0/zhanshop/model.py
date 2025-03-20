# +----------------------------------------------------------------------
# | zhanshop-py    [ 2024/1/1 上午12:00 ]
# +----------------------------------------------------------------------
# | Copyright (c) 2011~2024 zhangqiquan All rights reserved.
# +----------------------------------------------------------------------
# | Author: Administrator <768617998@qq.com>
# +----------------------------------------------------------------------
from zhanshop.db.query import Query


class Model():
    table = None
    query = None
    def __init__(self):
        self.query = Query(self.table)

    def getQuery(self)->Query:
        return self.query

