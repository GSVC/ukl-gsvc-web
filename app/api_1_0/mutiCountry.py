# -*- coding: utf-8 -*-

from flask import request
from . import api
from .api_functions.get140countryFlowerStatics import qury140countryFlowerStatics

@api.route('/get_140countryFlowerStatics/',methods=['POST'])
def get_140countryFlowerStatics():
    """
    本API140国卡统计页面统计数据接口
    :return:
    """
    if request.method == 'POST':
        Dic_data = request.get_json()
        begintime = str(Dic_data['beginTime'])
        endtime = str(Dic_data['endTime'])
        TimezoneOffset = str(Dic_data['TimezoneOffset'])

        return qury140countryFlowerStatics(begintime=begintime,
                                           endtime=endtime,
                                           TimezoneOffset=TimezoneOffset)

    return False
