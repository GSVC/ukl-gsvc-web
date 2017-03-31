# -*- coding: utf-8 -*-
"""
    webModifySqlAPI
    ~~~~~~~~~~~~~~
    为web应用与后台数据库操作（插入，更新，删除操作）的接口
    api_functions 中的DataApiFunc.py为其接口函数汇聚点，所有全局变量设置都在此；所有后台函数调用都在此设置
    Implementation helpers for the JSON support in Flask.

    :copyright: (c) 2015 by Armin kissf lu.
    :license: ukl, see LICENSE for more details.
"""

from . import api
from flask import json
from flask import request
from bson import json_util
# DataApiFunc 为数据库更新、插入、删除数据等操作函数
from .api_functions.DataApiFunc import (deleManuleVsimSrc,
                                       insertManuleVsimSrc,
                                       updateManuleVsimSrc,
                                       deleteNewVsimTestInfo,
                                       insertNewVsimTestInfo,
                                       updateNewVsimTestInfo)


@api.route('/delet_manulVsim/', methods=['POST'])
def delet_manulVsim():
    """

    :return:
    """
    if request.method == 'POST':
        arrayData = request.get_array(field_name='file')

        return deleManuleVsimSrc(array_data=arrayData)

    else:
        returnJsonData = {'err': True, 'errinfo': '操作违法！', 'data': []}

        return json.dumps(returnJsonData, sort_keys=True, indent=4, default=json_util.default)


@api.route('/insert_manulVsim/', methods=['POST'])
def insert_manulVsim():
    """

    :return:
    """
    if request.method == 'POST':
        arrayData = request.get_array(field_name='file')

        return insertManuleVsimSrc(array_data=arrayData)

    else:
        returnJsonData = {'err': True, 'errinfo': '操作违法！', 'data': []}

        return json.dumps(returnJsonData, sort_keys=True, indent=4, default=json_util.default)


@api.route('/update_manulVsim/', methods=['POST'])
def update_manulVsim():
    """

    :return:
    """
    if request.method == 'POST':
        arrayData = request.get_array(field_name='file')

        return updateManuleVsimSrc(array_data=arrayData)

    else:
        returnJsonData = {'err': True, 'errinfo': '操作违法！', 'data': []}

        return json.dumps(returnJsonData, sort_keys=True, indent=4, default=json_util.default)


@api.route('/delet_newvsimtest_info_table/', methods=['POST'])
def delet_newvsimtest_info_table():
    """

    :return:
    """
    if request.method == 'POST':
        arrayData = request.get_array(field_name='file')

        return deleteNewVsimTestInfo(array_data=arrayData)

    else:
        returnJsonData = {'err': True, 'errinfo': '操作违法！', 'data': []}

        return json.dumps(returnJsonData, sort_keys=True, indent=4, default=json_util.default)


@api.route('/insert_newvsimtest_info_table/', methods=['POST'])
def insert_newvsimtest_info_table():
    """

    :return:
    """
    if request.method == 'POST':
        arrayData = request.get_array(field_name='file')

        return insertNewVsimTestInfo(array_data=arrayData)

    else:
        returnJsonData = {'err': True, 'errinfo': '操作违法！', 'data': []}

        return json.dumps(returnJsonData, sort_keys=True, indent=4, default=json_util.default)


@api.route('/update_newvsimtest_info_table/', methods=['POST'])
def update_newvsimtest_info_table():
    """

    :return:
    """
    if request.method == 'POST':
        arrayData = request.get_array(field_name='file')

        return updateNewVsimTestInfo(array_data=arrayData)

    else:
        returnJsonData = {'err': True, 'errinfo': '操作违法！', 'data': []}

        return json.dumps(returnJsonData, sort_keys=True, indent=4, default=json_util.default)