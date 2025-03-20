# _*_ coding: utf-8 _*_
# @Time : 2024/7/31
# @Author : 杨洋
# @Email ： yangyang@doocn.com
# @File : DigiCore
# @Desc : 初始化tidb集群实例
import pymysql
from dbutils.pooled_db import PooledDB


class TiDBConnectionPool(object):
    """
    Tidb\Mysql的连接池，根据提供的账号密码产生一个连接

    未指定连接的数据库，如需要使用原生sql进行数据库操作，
    务必在表名称之前添加对应的数据库名称：如：dwd.dwd_crawler_amazon_on_hand_i_h

    :param host : 数据库或集群连接地址
    :param port ：数据库或集群端口号
    :param user : 用户名
    :param passwd ：密码

    """

    def __init__(self, host, port, user, passwd):

        # mysql 连接池
        self.db_pool = PooledDB(
            creator=pymysql,
            maxcached=1000,
            maxconnections=100,
            blocking=True,
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            cursorclass=pymysql.cursors.DictCursor
        )

    def __enter__(self):
        # 获取一个数据库连接
        self.conn = self.db_pool.connection()
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 提交事务并关闭数据库连接
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()

        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
