# _*_ coding: utf-8 _*_
# @Time : 2024/7/31
# @Author : 杨洋
# @Email ： yangyang@doocn.com
# @File : DigiCore
# @Desc : redis链接池使用工具
import json
from typing import Optional

from doocn_redis import REDIS_SERVER, REDIS_PORT, REDIS_PWD, ERP321_COOKIES, ERP321_AUTH_TOKEN, DINGDING_AUTH_TOKEN, \
    DIANXIAOMI_CRSWLER_COOKIE, LINGXING_CRSWLER_ACCESS_TOKEN, LINGXING_API_ACCESS_TOKEN
from doocn_redis.init import RedisConnectionPool


class RedisDao:

    def __init__(self,
                 host: Optional[str] = REDIS_SERVER,
                 port: Optional[int] = REDIS_PORT,
                 password: Optional[str] = REDIS_PWD,
                 db: Optional[int] = 5
                 ):
        self.conn = RedisConnectionPool(host, port, password, db)

    def format_data_json(self, bson_data):
        """F
        格式化返回的数据
        """
        if not bson_data:
            return None
        if b"{" in bson_data:
            json_data = json.loads(bson_data)
            return json_data
        else:
            return bson_data.decode("utf-8")

    def get_task_list_len(self, task_name: str):
        """
        获取任务列表长度
        :param task_name: 任务队列名称
        :return: int
        """
        with self.conn as redis_conn:
            return redis_conn.llen(task_name)

    def push_task(self, queue: str, task_list: list):
        """
        将任务添加到redis进行缓存
        :param queue: 任务队列名称
        :param task_list: 任务实例
        :return: True
        """
        with self.conn as redis_conn:
            for task_json in task_list:
                bson_data = json.dumps(task_json)
                redis_conn.lpush(queue, bson_data)

    def pop_task(self, queue: str):
        """
        从任务队列中弹出一个任务实例

        队列存在数据的时候 返回 json格式数据
        队列不存在数据的时候，返回 None
        :param queue: 任务队列名称
        :return: json/None
        """
        with self.conn as redis_conn:
            bson_data = redis_conn.rpop(queue)
            return self.format_data_json(bson_data)

    def get_lingxing_api_access_token(self):
        """
        获取领星API的token
        """
        with self.conn as redis_conn:
            bson_data = redis_conn.get(LINGXING_API_ACCESS_TOKEN)
            data_json = self.format_data_json(bson_data)
            return data_json.get('access_token') or None

    def get_lingxing_crawler_auth_token(self):
        """
        获取领星爬虫页面的token
        """
        with self.conn as redis_conn:
            token = redis_conn.srandmember(LINGXING_CRSWLER_ACCESS_TOKEN).decode()
            return token or None

    def del_task_from_redis(self, queue: str):
        """
        删除任务队列
        :param queue:
        :return:
        """
        with self.conn as redis_conn:
            redis_conn.delete(queue)

    def get_dianxiaomi_cookie(self):
        """
        获取店小秘页面的cookie
        """
        with self.conn as redis_conn:
            bson_data = redis_conn.get(DIANXIAOMI_CRSWLER_COOKIE)
            return self.format_data_json(bson_data)

    def get_dingding_access_token(self):
        """
        获取钉钉的access_token
        """

        with self.conn as redis_conn:
            bson_data = redis_conn.get(DINGDING_AUTH_TOKEN)
            return bson_data.decode().replace('"', '') if bson_data else None

    def get_erp321_access_token(self):
        """
        获取聚水潭API的access-token
        """
        with self.conn as redis_conn:
            bson_data = redis_conn.get(ERP321_AUTH_TOKEN)
            return self.format_data_json(bson_data)

    def get_erp321_cookie(self):
        """
        获取聚水潭爬虫页面的cookie
        """
        with self.conn as redis_conn:
            bson_data = redis_conn.get(ERP321_COOKIES)
            return self.format_data_json(bson_data)

    def hset_data(self,
                  queue: str,
                  data_json: dict):
        """
        保存数据
        """
        with self.conn as redis_conn:
            for key, value in data_json.items():
                redis_conn.hset(queue, key, value)

    def hget_data(self,
                  queue: str,
                  key: str):
        """
        保存数据
        """
        with self.conn as redis_conn:
            bson_data = redis_conn.hget(queue, key)
            return bson_data.decode() if bson_data else None

    def set_data(self,
                 queue: str,
                 values: list):
        """
        保存数据
        """
        with self.conn as redis_conn:
            for value in values:
                redis_conn.set(queue, value)

    def get_data(self, queue: str):
        """
        获取缓存数据
        :param queue:
        :return:
        """
        with self.conn as redis_conn:
            bson_data = redis_conn.get(queue)
            return self.format_data_json(bson_data)

    def get_all_list_data(self, queue: str):
        """
        获取redis队列中的全部数据
        """
        with self.conn as redis_conn:
            bson_list = redis_conn.hgetall(queue)
            result_list = [self.format_data_json(value) for _, value in bson_list.items()]
            return result_list

    def set_expire(self, queue: str, timeout: int):
        with self.conn as redis_conn:
            redis_conn.expire(queue, timeout)

    def setnx_run_sign(self, queue: str):
        with self.conn as redis_conn:
            # 不存在则返回1，存在则返回0
            return redis_conn.setnx(queue, 1)

