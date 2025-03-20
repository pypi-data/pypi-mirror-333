# _*_ coding: utf-8 _*_
# @Time : 2024/7/31
# @Author : 杨洋
# @Email ： yangyang@doocn.com
# @File : DigiCore
# @Desc :
import pymongo
from pymongo import UpdateOne
from loguru import logger
from collections import OrderedDict

from typing import Optional

from doocn_mongo import MONGODB_URL


class MongoDao():
    """
    mongodb事务方法集合
    """

    def __init__(self, mongodb_url: Optional[str] = None):
        self.client = pymongo.MongoClient(
            MONGODB_URL if not mongodb_url else mongodb_url)

    def get_bulk_write_list(self, data_list: list, field_list: list):
        """
        获取批量插入的数据对象列表
        :param self:
        :param data_list: 数据列表
        :param field_list: 主键过滤字段列表
        :return:
        """
        bulk_write_list = []
        for data_json in data_list:
            filter_data = self.get_filter_data(field_list, data_json)
            if not filter_data:
                continue
            bulk_write_list.append(
                UpdateOne(
                    filter=filter_data,
                    update={"$set": data_json},
                    upsert=True
                )
            )
        return bulk_write_list

    def get_filter_data(self, field_list: list, data_json: dict):
        """
        根据传入的过滤条件字段列表，构建一个有序的字典
        :param data_json: 需要插入到数据库的字典数据
        :param field_list: 过滤条件字段
        :return: dict
        """
        # 过滤掉字段列表中没有对应的键
        valid_field_order = [field for field in field_list if field in data_json]
        set_A = set(valid_field_order)
        set_B = set(field_list)
        # 查找两个列表中不相同的字段
        results = set_A.symmetric_difference(set_B)
        if results:
            logger.info(f"{results} 在数据字典中不存在，无法获取筛选条件！")
            logger.error(data_json)
            return {}
        # 过滤掉字段列表中没有对应的键
        filter_data = OrderedDict([(field, data_json[field]) for field in field_list])
        return filter_data

    def load_table_ob(self, db_name, table_name):
        """
        根据mongodb的数据库名称和表名称，创建表对象
        :param db_name: 数据库名称
        :param table_name: 表名称
        :return: object
        """
        db_ob = self.client.get_database(db_name)
        table_ob = db_ob.get_collection(table_name)
        return table_ob

    def create_index(self, field_list: list, table_ob):
        """
        自定义 表的联合索引主键
        :param field_list: 联合索引主键列表
        :return: bool
        """
        if not field_list:
            logger.info("无自定义主键！")
            return
        index_data = [(one, 1) for one in field_list]
        name = '_1_'.join(field_list)
        table_ob.create_index(index_data, unique=True, name=name)

    def bulk_save_data(self, data_list: list, field_list: list, table_ob):
        """
        批量保存数据到数据库
        如果数据存在则根据 自定义主键进行数据更新
        :param data_list: 数据列表
        :param field_list: 主键列表
        :return:
        """
        try:
            self.create_index(field_list, table_ob)
        except Exception as e:
            logger.error("主键以存在！")
        bulk_write_list = self.get_bulk_write_list(data_list, field_list)
        if not bulk_write_list:
            return
        table_ob.bulk_write(bulk_write_list, ordered=False)
