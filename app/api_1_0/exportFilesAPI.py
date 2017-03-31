# -*- coding: utf-8 -*-

"""
    exportFilesAPI
    ~~~~~~~~~~~~~~
    为web应用与后台导出文件（xls...）的接口
    api_functions 中：
    1、exportExcelFunc.py为Excel文件导出接口函数汇聚点，所有全局变量设置都在此；所有后台函数调用都在此设置

    :copyright: (c) 2015 by Armin kissf lu.
    :license: ukl, see LICENSE for more details.
"""

from flask import request
from flask import json
from . import api
import flask_excel as excel
# Python excel Mole
from .api_functions.exportExcelFunc import (get_excel140countryDataAndSorted,
                                           get_excelFlowerDataAndSorted,
                                           get_excelManulInfoDataAndSorted,
                                           get_excelOnSysInfoDataAndSorted,
                                           get_excelFirsProbDicDataAndSorted,
                                           get_excelManualDeleteTemple,
                                           get_excelManualInsertTemple,
                                           get_excelCountrySrcStaticDataAndSorted,
                                           get_excelNewVsimTestInfoDeleteTemple,
                                           get_excelNewVsimTestInfoInsertTemple,
                                           get_excelNewVsimTestInfoUpdateTemple,
                                           get_excelNewVsimTestInfo)


@api.route('/export_countrySrcStatic/', methods=['POST'])
def export_countrySrcStatic():
    if request.method == 'POST':
        dic_data = json.loads(request.form['data'])
        sortedDicData = get_excelCountrySrcStaticDataAndSorted(dic_data=dic_data)
        return excel.make_response_from_array(sortedDicData, "xls", file_name="ExportCountrySrcStaticData")
    else:
        return False


@api.route('/export_140country/', methods=['POST'])
def export_140country():
    if request.method == 'POST':

        dic_data = json.loads(request.form['data'])
        sortedDicData = get_excel140countryDataAndSorted(dic_data=dic_data)

        return excel.make_response_from_array(sortedDicData, "xls", file_name="Export140countryFlowerData")
    else:

        return False


@api.route('/export_Flower/', methods=['POST'])
def export_Flower():
    if request.method == 'POST':
        dic_data = json.loads(request.form['data'])
        sortedDicData = get_excelFlowerDataAndSorted(dic_data=dic_data)

        return excel.make_response_from_array(sortedDicData, "xls", file_name="ExportFlowerData")

    return False


@api.route('/export_ManualInfo/', methods=['POST'])
def export_ManualInfo():
    if request.method == 'POST':
        dic_data = json.loads(request.form['data'])
        sortedDicData = get_excelManulInfoDataAndSorted(dic_data=dic_data)

        return excel.make_response_from_array(sortedDicData, "xls", file_name="ExportManualInfoData")
    return False


@api.route('/export_manualDeleteTemplate/', methods=['POST'])
def export_manualDeleteTemplate():
    if request.method == 'POST':
        dic_data = [{'imsi': '460068029099402'}, {'imsi': '416770118932592'}]
        sortedDicData = get_excelManualDeleteTemple(dic_data=dic_data)

        return excel.make_response_from_array(sortedDicData, "xls", file_name="manualDeleteTemplate")
    return False


@api.route('/export_manualInsertTemplate/', methods=['POST'])
def export_manualInsertTemplate():
    if request.method == 'POST':
        dic_data = [{"imsi": "202052965490990",
                     u"负责人": u"刘超",
                     u"国家": u"希腊",
                     u"运营商": u"Vodafone",
                     u"超套餐限速/费用": u"不可用",
                     u"运营商网站的注册信息": "",
                     u"套餐办理方式": u"自动续办",
                     u"查询方式": "",
                     u"备注": u"无",
                     u"运营接口人": u"丁洁",
                     u"下架日期": u"2016-06-13 07:42:56",
                     u"卡批次": "",
                     u"是否代理商卡 0否，1是代理商卡": "0",
                     u"卡的国家属性 0本国卡，1是多国卡": "0"}]
        sortedDicData = get_excelManualInsertTemple(dic_data=dic_data)

        return excel.make_response_from_array(sortedDicData, "xls", file_name="manualInsertAndUpdateTemplate")
    return False


@api.route('/export_FirsProbDic/', methods=['POST'])
def export_FirsProbDic():
    if request.method == 'POST':
        dic_data = json.loads(request.form['data'])
        sortedDicData = get_excelFirsProbDicDataAndSorted(dic_data=dic_data)

        return excel.make_response_from_array(sortedDicData, "xls", file_name="ExportOnSysInfoData")
    return False


@api.route('/export_OnSysInfo/', methods=['POST'])
def export_OnSysInfo():
    if request.method == 'POST':
        dic_data = json.loads(request.form['data'])
        sortedDicData = get_excelOnSysInfoDataAndSorted(dic_data=dic_data)

        return excel.make_response_from_array(sortedDicData, "xls", file_name="ExportOnSysInfoData")
    return False


@api.route('/export_newVsimTestInfoDeleteTemplate/', methods=['POST'])
def export_newVsimTestInfoDeleteTemplate():
    if request.method == 'POST':
        # dic_data=json.loads(request.form['data'])
        dic_data = [{'id_newvsimtest': '460068029099402'}, {'id_newvsimtest': '416770118932592'}]
        sortedDicData = get_excelNewVsimTestInfoDeleteTemple(dic_data=dic_data)

        return excel.make_response_from_array(sortedDicData, "xls", file_name="NewVsimTestInfoDeleteTemple")

    return False


@api.route('/export_newVsimTestInfoUpdateTemplate/', methods=['POST'])
def export_newVsimTestInfoUpdateTemplate():
    if request.method == 'POST':
        # dic_data=json.loads(request.form['data'])
        dic_data = [{u"测试id": u"460068029099402",
                     u"卡提供人": u"丁洁",
                     u"测试人": u"凌刚",
                     u"测试卡信息": u"TELSTRA测试卡，2016.12.20到期",
                     u"卡类型(0本国, 1多国": u"0",
                     u"国家": u"澳大利亚",
                     u"简称": u"AU",
                     u"运营商": u"TELSTRA",
                     u"plmn": u"50501",
                     u"网络制式": u"24",
                     u"配置更改": u"更改卡制式为2G/3G",
                     u"imsi": u"505013502029797",
                     u"账户": u"test748_KR@uroaming.com",
                     u"imei": u"868740023157474",
                     u"设备类型": u"G2_160906",
                     u"调卡成功时间": u"2016-12-15 01:44:20",
                     u"换卡时间": u"2016-12-15 03:43:45",
                     u"注册运营商": u"TELSTRA",
                     u"eplmn": u"50501",
                     u"注册网络": u"8",
                     u"lac": u"338",
                     u"cellid": u"87282827",
                     u"基本可用性(0 否, 1是": u"1",
                     u"小时稳定性(0 否, 1是": u"1",
                     u"协商速率": u"3g convert dl:8640,ul:7936",
                     u"协商速率一致性(0 否, 1是": u"1",
                     u"失败原因": u"",
                     u"备注": u""
                     }]
        sortedDicData = get_excelNewVsimTestInfoUpdateTemple(dic_data=dic_data)

        return excel.make_response_from_array(sortedDicData, "xls",
                                              file_name="NewVsimTestInfoUpdateTemple")

    return False


@api.route('/export_newVsimTestInfoInsertTemplate/', methods=['POST'])
def export_newVsimTestInfoInsertTemplate():
    if request.method == 'POST':
        dic_data = [{u"卡提供人": u"丁洁",
                     u"测试人": u"凌刚",
                     u"测试卡信息": u"TELSTRA测试卡，2016.12.20到期",
                     u"卡类型(0本国, 1多国": u"0",
                     u"国家": u"澳大利亚",
                     u"简称": u"AU",
                     u"运营商": u"TELSTRA",
                     u"plmn": u"50501",
                     u"网络制式": u"24",
                     u"配置更改": u"更改卡制式为2G/3G",
                     u"imsi": u"505013502029797",
                     u"账户": u"test748_KR@uroaming.com",
                     u"imei": u"868740023157474",
                     u"设备类型": u"G2_160906",
                     u"调卡成功时间": u"2016-12-15 01:44:20",
                     u"换卡时间": u"2016-12-15 03:43:45",
                     u"注册运营商": u"TELSTRA",
                     u"eplmn": u"50501",
                     u"注册网络": u"8",
                     u"lac": u"338",
                     u"cellid": u"87282827",
                     u"基本可用性(0 否, 1是": u"1",
                     u"小时稳定性(0 否, 1是": u"1",
                     u"协商速率": u"3g convert dl:8640,ul:7936",
                     u"协商速率一致性(0 否, 1是": u"1",
                     u"失败原因": u"",
                     u"备注": u""
                     }]
        sortedDicData = get_excelNewVsimTestInfoInsertTemple(dic_data=dic_data)

        return excel.make_response_from_array(sortedDicData, "xls",
                                              file_name="NewVsimTestInfoInsertTemple")

    return False


@api.route('/export_newVsimTestInfo/', methods=['POST'])
def export_newVsimTestInfo():
    if request.method == 'POST':
        dic_data = json.loads(request.form['data'])
        sortedDicData = get_excelNewVsimTestInfo(dic_data=dic_data)

        return excel.make_response_from_array(sortedDicData, "xls",
                                              file_name="NewVsimTestInfo")

    return False
