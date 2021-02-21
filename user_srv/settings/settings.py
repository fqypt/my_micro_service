# 使用数据库连接池
from playhouse.pool import PooledMySQLDatabase
# 数据库连接池一段时间不使用会被关闭，用这个库的方法可以重新启动链接，不配置就容易出现mysql gone away错误
from playhouse.shortcuts import ReconnectMixin


class ReconnectMysqlDatabase(ReconnectMixin,PooledMySQLDatabase):
    # 不用内容，就完成继承过程就行
    # ReconnectMixin中的super不是调用父类，而是python中的mro原理
    pass


MYSQL_DB = "mxshop_user_srv"
MYSQL_HOST = "192.168.220.30"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"

DB = ReconnectMysqlDatabase(MYSQL_DB, host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD)
