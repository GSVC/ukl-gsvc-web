# -*- coding: utf-8 -*-

"""

    exportExcelFunc
    ~~~~~~~~~~~~~~
    外部接口:
    1、exportFilesAPI

    本单元函数自成一体，重点实现EXCEL文件导出，实现list dic类数据的导出xls,不做后台xls数据存储

    :copyright: (c) 2015 by Armin kissf lu.
    :license: ukl, see LICENSE for more details.
"""
import datetime as dt
from datetime import datetime


def getDictExcelData(array_data):
    """

    :param array_data:
    :return:
    """
    dicData = []
    key_dic = []
    errinfo = ''
    if (type(array_data) is list) and (len(array_data) >= 2):
        for i in range(len(array_data)):
            temp_dic = {}
            if i == 0:
                key_dic = array_data[0]
            else:
                for j in range(len(key_dic)):
                    try:
                        temp_dic.update({key_dic[j]: array_data[i][j]})

                    except IndexError:
                        errinfo = 'Index Error'
                dicData.append(temp_dic)

    else:
        errinfo = 'Data Error'
    if errinfo:
        returnDictData = {'err': True, 'errinfo': errinfo, 'data': []}
    else:
        returnDictData = {'err': False, 'errinfo': errinfo, 'data': dicData}

    return returnDictData


def getListExcelData(dic_data, sort_key, datetimekey):
    """

    :param dic_data:
    :param sort_key:
    :param datetimekey: 数据中的时间数据
    :return:
    """
    dicData = dic_data
    datetimeKey = datetimekey
    max_key = []
    sort_max_key = []
    sorted_list_data = []
    sortKey = sort_key
    temp_null_key = []

    if datetimeKey:
        for data in dicData:
            for date in datetimeKey:
                if date in data.keys():
                    if (data[date] is not None) and (data[date] != ''):
                        data[date] = str(datetime.strptime(data[date], '%Y-%m-%dT%H:%M:%S.%fZ') + dt.timedelta(hours=8))
    for dic in dicData:
        temp_key = dic.keys()
        if len(max_key) < len(temp_key):
            max_key = temp_key

    for sortofkey in sortKey:
        if sortofkey not in max_key:
            temp_null_key.append(sortofkey)

    if temp_null_key:
        for k in temp_null_key:
            sortKey.remove(k)

    for sk in sortKey:
        for mk in max_key:
            if sk == mk:
                sort_max_key.append(sk)
    # 添加标同行
    sorted_list_data.append(sort_max_key)

    for i in range(len(dicData)):
        # 每次清除上次记录
        temp_one_list = []
        for key in sort_max_key:
            try:
                temp_one_list.append(dicData[i][key])
            except KeyError:
                temp_one_list.append('')
        sorted_list_data.append(temp_one_list)

    return sorted_list_data


def getDayHourListExcelData(dic_data, sort_key, datetimekey):
    """

    :param dic_data:
    :param sort_key:
    :param datetimekey: 数据中的时间数据
    :return:
    """
    dicData = dic_data
    datetimeKey = datetimekey
    max_key = []
    sort_max_key = []
    sorted_list_data = []
    sortKey = sort_key
    temp_null_key = []

    if datetimeKey:
        for data in dicData:
            for date in datetimeKey:
                if date in data.keys():
                    if (data[date] is not None) and (data[date] != ''):
                        data[date] = str(datetime.strptime(data[date], '%Y-%m-%d %H') + dt.timedelta(hours=8))
    for dic in dicData:
        temp_key = dic.keys()
        if len(max_key) < len(temp_key):
            max_key = temp_key

    for sortofkey in sortKey:
        if sortofkey not in max_key:
            temp_null_key.append(sortofkey)

    if temp_null_key:
        for k in temp_null_key:
            sortKey.remove(k)

    for sk in sortKey:
        for mk in max_key:
            if sk == mk:
                sort_max_key.append(sk)
    # 添加标同行
    sorted_list_data.append(sort_max_key)

    for i in range(len(dicData)):
        # 每次清除上次记录
        temp_one_list = []
        for key in sort_max_key:
            try:
                temp_one_list.append(dicData[i][key])
            except KeyError:
                temp_one_list.append('')
        sorted_list_data.append(temp_one_list)

    return sorted_list_data


def get_excelCountrySrcStaticDataAndSorted(dic_data):
    """

    :param dic_data:
    :return:
    """
    dicData = dic_data
    sortKey = [u'国家',
               u'套餐名称',
               u'套餐更新日期',
               u'归属机构',
               u'在架卡数',
               u'可用卡数',
               u'流量不足卡数',
               u'未激活卡数',
               u'流量预警阀值_MB',
               u'总计流量_GB',
               u'使用流量_GB',
               u'剩余流量_GB',
               u'流量使用率']

    dateTimeKey = [u'套餐更新日期']
    # print (dicData[0][u'套餐更新日期'])
    sorted_list_data = getDayHourListExcelData(dic_data=dicData,
                                               sort_key=sortKey,
                                               datetimekey=dateTimeKey)

    return sorted_list_data


def get_excel140countryDataAndSorted(dic_data):
    """

    :param dic_data:
    :return:
    """
    dicData = dic_data
    sortKey = [u'imsi',
               u'国际流量',
               u'国内流量',
               u'总计流量',
               u'国际流量占比',
               u'套餐类型',
               u'网络集名',
               u'ORG',
               u'占用状态',
               u'state']

    dateTimeKey = []
    sorted_list_data = getListExcelData(dic_data=dicData,
                                        sort_key=sortKey,
                                        datetimekey=dateTimeKey)

    return sorted_list_data


def get_excelFlowerDataAndSorted(dic_data):
    """

    :param dic_data: 待装换原始数据
    :return:
    """
    dicData = dic_data
    sortKey = [u'imsi',
               u'time',
               u'mcc',
               u'plmn',
               u'lac',
               u'Flower']

    dateTimeKey = [u'time']
    sorted_list_data = getListExcelData(dic_data=dicData,
                                        sort_key=sortKey,
                                        datetimekey=dateTimeKey)

    return sorted_list_data


def get_excelManulInfoDataAndSorted(dic_data):
    """

    :param dic_data:
    :return:
    """
    dicData = dic_data
    sortKey = [u'imsi',
               u'country_iso',
               u'country_cn',
               u'GSVC负责人',
               u'运营负责人',
               u'系统',
               u'state',
               u'slot_state',
               u'是否代理商卡',
               u'是否多国卡',
               u'卡批次',
               u'BAM编码',
               u'卡位',
               u'operator',
               u'iccid',
               u'套餐',
               u'套餐外付费类型',
               u'激活日期',
               u'上次套餐更新日期',
               u'下次套餐更新日期',
               u'备注',
               u'电话号码',
               u'付费类型',
               u'apn',
               u'上架日期']

    dateTimeKey = [u'激活日期',
                   u'上次套餐更新日期',
                   u'下次套餐更新日期',
                   u'上架日期']
    print (dicData[0][u'上次套餐更新日期'])
    sorted_list_data = getListExcelData(dic_data=dicData,
                                        sort_key=sortKey,
                                        datetimekey=dateTimeKey)

    return sorted_list_data


def get_excelOnSysInfoDataAndSorted(dic_data):
    """

    :param dic_data:
    :return:
    """
    dicData = dic_data
    sortKey = [u'imsi',
               u'country',
               u'卡分组属性',
               u'套餐',
               u'state',
               u'占用状态',
               u'卡位状态',
               u'激活状态',
               u'认证状态',
               u'业务状态',
               u'BAM状态',
               u'套餐状态',
               u'激活类型',
               u'本网可用',
               u'是否多国卡',
               u'初始流量MB',
               u'累计使用流量MB',
               u'剩余流量MB',
               u'激活日期',
               u'上次套餐更新日期',
               u'下次套餐更新日期',
               u'iccid',
               u'BAM编码',
               u'卡位',
               u'备注']
    dateTimeKey = [u'激活日期',
                   u'上次套餐更新日期',
                   u'下次套餐更新日期']
    sorted_list_data = getListExcelData(dic_data=dicData,
                                        sort_key=sortKey,
                                        datetimekey=dateTimeKey)
    return sorted_list_data


def get_excelFirsProbDicDataAndSorted(dic_data):
    """

    :param dic_data: 待装换原始数据
    :return:
    """
    dicData = dic_data
    sortKey = [u'country',
               u'imsi',
               u'iccid',
               u'套餐类型',
               u'套餐更新日期',
               u'BAM',
               u'分卡次数',
               u'不同终端数',
               u'累计流量MB',
               u'报错信息']
    dateTimeKey = [u'套餐更新日期']
    sorted_list_data = getListExcelData(dic_data=dicData,
                                        sort_key=sortKey,
                                        datetimekey=dateTimeKey)

    return sorted_list_data


def get_excelManualDeleteTemple(dic_data):
    """

    :param dic_data:
    :return:
    """
    dicData = dic_data
    sortKey = [u'imsi']
    dateTimeKey = []
    sorted_list_data = getListExcelData(dic_data=dicData,
                                        sort_key=sortKey,
                                        datetimekey=dateTimeKey)

    return sorted_list_data


def get_excelManualInsertTemple(dic_data):
    """

    :param dic_data:
    :return:
    """
    dicData = dic_data
    sortKey = [u'imsi',
               u'负责人',
               u'国家',
               u'运营商',
               u'超套餐限速/费用',
               u'运营商网站的注册信息',
               u'套餐办理方式',
               u'查询方式',
               u'备注',
               u'运营接口人',
               u'下架日期',
               u'卡批次',
               u'是否代理商卡 0否，1是代理商卡',
               u'卡的国家属性 0本国卡，1是多国卡']

    dateTimeKey = []
    sorted_list_data = getListExcelData(dic_data=dicData,
                                        sort_key=sortKey,
                                        datetimekey=dateTimeKey)

    return sorted_list_data


def get_excelNewVsimTestInfoDeleteTemple(dic_data):
    """

    :param dic_data:
    :return:
    """
    dicData = dic_data
    sortKey = [u'id_newvsimtest']
    dateTimeKey = []
    sorted_list_data = getListExcelData(dic_data=dicData,
                                        sort_key=sortKey,
                                        datetimekey=dateTimeKey)

    return sorted_list_data


def get_excelNewVsimTestInfoUpdateTemple(dic_data):
    """

    :param dic_data:
    :return:
    """
    dicData = dic_data
    sortKey = [u"测试id",
               u"卡提供人",
               u"测试人",
               u"测试卡信息",
               u"卡类型(0本国, 1多国)",
               u"国家",
               u"简称",
               u"运营商",
               u"plmn",
               u"网络制式",
               u"配置更改",
               u"imsi",
               u"账户",
               u"imei",
               u"设备类型",
               u"调卡成功时间",
               u"换卡时间",
               u"注册运营商",
               u"eplmn",
               u"注册网络",
               u"lac",
               u"cellid",
               u"基本可用性(0 否, 1是)",
               u"小时稳定性(0 否, 1是)",
               u"协商速率",
               u"协商速率一致性(0 否, 1是)",
               u"失败原因",
               u"备注"
               ]
    dateTimeKey = []
    sorted_list_data = getListExcelData(dic_data=dicData,
                                        sort_key=sortKey,
                                        datetimekey=dateTimeKey)

    return sorted_list_data


def get_excelNewVsimTestInfoInsertTemple(dic_data):
    """

    :param dic_data:
    :return:
    """
    dicData = dic_data
    sortKey = [u"卡提供人",
               u"测试人",
               u"测试卡信息",
               u"卡类型(0本国, 1多国)",
               u"国家",
               u"简称",
               u"运营商",
               u"plmn",
               u"网络制式",
               u"配置更改",
               u"imsi",
               u"账户",
               u"imei",
               u"设备类型",
               u"调卡成功时间",
               u"换卡时间",
               u"注册运营商",
               u"eplmn",
               u"注册网络",
               u"lac",
               u"cellid",
               u"基本可用性(0 否, 1是)",
               u"小时稳定性(0 否, 1是)",
               u"协商速率",
               u"协商速率一致性(0 否, 1是)",
               u"失败原因",
               u"备注"
               ]
    dateTimeKey = []
    sorted_list_data = getListExcelData(dic_data=dicData,
                                        sort_key=sortKey,
                                        datetimekey=dateTimeKey)

    return sorted_list_data


def get_excelNewVsimTestInfo(dic_data):
    """

    :param dic_data:
    :return:
    """
    dicData = dic_data
    sortKey = [u"测试id",
               u"卡提供人",
               u"测试人",
               u"测试卡信息",
               u"本国_多国",
               u"国家",
               u"简称",
               u"运营商",
               u"plmn",
               u"网络制式",
               u"配置更改",
               u"imsi",
               u"账户",
               u"imei",
               u"设备类型",
               u"调卡成功时间",
               u"换卡时间",
               u"注册运营商",
               u"eplmn",
               u"注册网络",
               u"lac",
               u"cellid",
               u"基本可用性",
               u"小时稳定性",
               u"协商速率",
               u"协商速率一致性",
               u"失败原因",
               u"备注"
               ]
    dateTimeKey = []
    sorted_list_data = getListExcelData(dic_data=dicData,
                                        sort_key=sortKey,
                                        datetimekey=dateTimeKey)

    return sorted_list_data
