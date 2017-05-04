# -*- coding: utf-8 -*-


from flask import request
# from flask import json
# from bson import json_util
from . import api
from api_functions.getVsimCardCountryInfo import (getVsimCountryStatic, getindexHtmlMutiLineData)
# 导入查询手工维护表、系统资源统计表模块
from api_functions.getonSysSrc import (getVsimManulInfor,
                                       quryonSysSrc)
# 获取gsvchome国家维度卡资源统计栏
from api_functions.getCountrySrcConIndexGrid import qurycountrySrcCon
# 获取问题初诊的信息函数
from api_functions.getCountryProbDic import getProbFisrtDic
# new vsim test model
from api_functions.newVsimTest import get_new_vsim_test_info
# org ajax model
from api_functions.selectAjax.getSelectData import get_org


# ("以下为资源页面API接口-------------------------------------------------------------------------------------------------")
@api.route('/get_srcVsimManulInfor/', methods=['POST'])
def get_Country():
    """
    本api为资源页获取手工维护表数据
    :return:
    """
    if request.method == 'POST':
        Dic_data = request.get_json()
        country = str(Dic_data['country'])
        person = str(Dic_data['person'])
        imsi = str(Dic_data['imsi'])

        return getVsimManulInfor(country, person=person, imsi=imsi)

    return False


@api.route('/get_onSysSrc/', methods=['POST'])
def get_onSysSrc():
    """
    本API为获取系统平台中的卡资源数据接口
    :return:
    """
    if request.method == 'POST':
        Dic_data = request.get_json()
        country = str(Dic_data['country'])
        imsi = str(Dic_data['imsi'])
        status = str(Dic_data['status'])
        business_status = str(Dic_data['business_status'])
        slot_status = str(Dic_data['slot_status'])
        bam_status = str(Dic_data['bam_status'])
        occupy_status = str(Dic_data['occupy_status'])
        org = str(Dic_data['org'])
        package_status = str(Dic_data['package_status'])
        return quryonSysSrc(country,
                            imsi=imsi,
                            status=status,
                            business_status=business_status,
                            slot_status=slot_status,
                            bam_status=bam_status,
                            occupy_status=occupy_status,
                            org=org,
                            package_status=package_status)

    return False


# ("以下为主页页面API接口-------------------------------------------------------------------------------------------------")
@api.route('/get_country_flower_static/')
def get_chart_country():
    """
    本api用于获取主页国家维度画板统计图数据：本国卡状态统计、老系统/新架构本国可用卡套餐流量统计
    :return:
    """
    country = request.args.get('country', '', type=str)

    return getVsimCountryStatic(country)


@api.route('/get_mutiLine_maxUser/', methods=['POST'])
def get_mutiLine_maxUser():
    """
    本api为绘制index主页峰值用户、卡数曲线接口
    :return: 峰值用户、在板卡数、可用卡数JSON数据
    """
    if request.method == 'POST':
        DicData = request.get_json()
        country = str(DicData['country'])
        begintime = str(DicData['begintime'])
        endtime = str(DicData['endtime'])
        butype = str(DicData['butype'])
        timedim = str(DicData['timedim'])

        return getindexHtmlMutiLineData(country, begintime, endtime, butype=butype, timedim=timedim)


@api.route('/get_countrySrcCon/', methods=['GET', 'POST'])
def get_countrySrcCon():
    """
    本API为主页国家概述面板获取国家不同套餐卡状态统计数据接口
    :return:
    """
    # print request.args.get('country', 'ad', type=str)
    if request.method == 'POST':
        DicData = request.get_json()
        country = str(DicData['country'])
        orgName = str(DicData['org'])
        vsimType = str(DicData['vsim_type'])

        return qurycountrySrcCon(country, orgName, vsimType)

    if request.method == 'GET':
        country = request.args.get('country', 'ad', type=str)
        orgName = request.args.get('org', 'gtbu', type=str)
        vsimType = request.args.get('vsim_type', '', type=str)

        return qurycountrySrcCon(country, orgName, vsimType)

    return False


@api.route('/get_countryProbVsimDic/', methods=['POST'])
def get_countryProbVsimDic():
    """

    :return:
    """
    if request.method == 'POST':
        Dic_data = request.get_json()
        querySort = str(Dic_data['querySort'])
        queryPram = str(Dic_data['queryPram'])
        queryPlmn = str(Dic_data['queryPlmn'])
        begintime = str(Dic_data['begintime'])
        endtime = str(Dic_data['endtime'])
        dispatch_begin_t = str(Dic_data['dispatchBeginTime'])
        dispatch_end_t = str(Dic_data['dispatchEndTime'])
        TimezoneOffset = int(Dic_data['TimezoneOffset'])
        DispatchThreshold = int(Dic_data['DispatchThreshold'])
        FlowerThreshold = int(Dic_data['FlowerThreshold'])
        return getProbFisrtDic(query_sort=querySort,
                               query_pram=queryPram,
                               query_plmn=queryPlmn,
                               begin_time=begintime,
                               end_time=endtime,
                               dispatch_begin_time = dispatch_begin_t,
                               dispatch_end_time = dispatch_end_t,
                               timezone_off_set=TimezoneOffset,
                               dispatch_threshold=DispatchThreshold,
                               flower_threshold=FlowerThreshold)
    return False


@api.route('/get_newVsimTestInforTable/', methods=['POST'])
def get_newVsimTestInforTable():
    """
    本api为资源页获取手工维护表数据
    :return:
    """
    if request.method == 'POST':
        Dic_data = request.get_json()
        test_vsim_info = str(Dic_data['test_vsim_info'])
        country = str(Dic_data['country'])
        person = str(Dic_data['person'])

        return get_new_vsim_test_info(person, country, test_vsim_info)

    return False


@api.route('/get_select2_orgdata/')
def get_select2_orgdata():
    """
    本api为资源页获取手工维护表数据
    :return:
    """
    return get_org()
