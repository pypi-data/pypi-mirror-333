# _*_ coding: utf-8 _*_
# @Time : 2024/7/31
# @Author : 杨洋
# @Email ： yangyang@doocn.com
# @File : DigiCore
# @Desc :
from collections import OrderedDict


def create_ordered_dict(field_list: list, unordered_dict: dict):
    """
    根据传入的列表字段参数，构建一个有序的字典
    :param unordered_dict: 需要插入到数据库的字典数据
    :param field_list: 数据库字段
    :return: dict
    """
    # 原始数据中没有的字段则赋值为 None
    diff_keys = set(field_list) - set(unordered_dict.keys())
    for key in diff_keys:
        unordered_dict[key] = 'None'

    # 原始数据中多的字段，则删除
    diff_keys = set(unordered_dict.keys()) - set(field_list)
    for key in diff_keys:
        unordered_dict.pop(key)

    ordered_dict = OrderedDict([(field, unordered_dict[field]) for field in field_list])
    return ordered_dict


def get_dict_value(json_data: dict):
    """
    获取字典的values，转化为字符转类型
    :param json_data: 插入数据库的数据
    :return: 返回 元组类型 的 字符串
    """
    value_list = []
    # 如果是字符串类型的value，则直接不做处理，
    # 如果是非字符串类型的value，则进行解码
    for value in json_data.values():
        str_value = str(value)
        value_list.append(str_value)
    tup_data = tuple(value_list)
    sql_data = str(tup_data)
    if len(tup_data) == 1:
        values = sql_data.replace(',', '')
    else:
        values = sql_data
    return values


def list_to_sql_values(field_list: list, data_list: [dict]):
    """
    将列表套字典格式的数据，转化为字符串类型的元组：(...),(...),(...)
    :param field_list: 字段列表
    :param data_list: 插入数据库的数据列表
    :return: 字符串类型的元组
    """
    value_list = []
    for json_data in data_list:
        # 对字典数据根据列表顺序进行排序
        ordered_dict = create_ordered_dict(field_list, json_data)
        # 将字典转化为 元组格式的 字符串
        sql_data = get_dict_value(ordered_dict)
        value_list.append(sql_data)
    sql_values = ",".join(value_list)
    return sql_values


def create_insert_sql(db_table: str, field_list: list, sql_values: str):
    """
    根据字段列表 和 字段对应需要插入的数据，构建出insert的sql语句
    :param db_table: 数据库表名称
    :param field_list: 字段列表
    :param sql_values: 字段对应需要插入的values
    :return: str
    """

    # 使用 ', '.join() 将列表组合成完整的结果字符串
    result_str = ', '.join(f"`{element}`" for element in field_list)

    # 生成字符串的生成器表达式
    value_strs = ', '.join(f"`{field}`=values(`{field}`)" for field in field_list)

    # 在 SQL 语句中使用该字符串
    insert_sql = f"INSERT INTO {db_table}({result_str}) VALUES {sql_values} ON DUPLICATE KEY UPDATE {value_strs}"
    return insert_sql
