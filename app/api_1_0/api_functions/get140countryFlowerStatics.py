# -*- coding: utf-8 -*-

# import sys
import json
from bson import json_util
import mysql.connector
from .SqlPack.SQLModel import qureResultAsJson
import time
import datetime
import pymongo
# from SqlPack.pyMongoModel import (sql_info)
from .SqlPack.SqlLinkInfo import get140countryFlowerStatics as SqlInfo

sql_info = SqlInfo

imsiInfo_sysStr = sql_info['140src']['db']
imsiInfo_Database = sql_info['140src']['database']


def getJosonData(sys_str, data_base, query_str):
    """

    :param sys_str:
    :param data_base:
    :param query_str:
    :return:
    """
    jsonResults = qureResultAsJson(sysStr=sys_str,
                                   Database=data_base,
                                   query_str=query_str,
                                   where=[])
    return jsonResults


def timestamp_datetime(value):
    format_str = '%Y-%m-%d %H:%M:%S'
    # value为传入的值为时间�?(整形)，如�?1332888820
    value = time.localtime(value)
    # # 经过localtime转换后变�?
    # # time.struct_time
    # (tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # �?后再经过strftime函数转换为正常日期格式�??
    dt = time.strftime(format_str, value)
    return dt


def datetime_timestamp(dt):
    # dt为字符串
    # 中间过程，一般都�?要将字符串转化为时间数组
    time.strptime(dt, '%Y-%m-%d %H:%M:%S')
    # time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28,
    # tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
    # �?"2012-03-28 06:53:40"转化为时间戳
    s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
    return int(s)


def getGMT0StrTime(str_time, off_set):
    """

    :param str_time:
    :param off_set:
    :return:
    """
    try:
        GMT0dateTime = datetime.datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S')-datetime.timedelta(minutes=off_set)
    except ValueError:
        GMT0dateTime = datetime.datetime.strptime(str_time, '%Y-%m-%d') - datetime.timedelta(minutes=off_set)

    return str(GMT0dateTime)


def getlistimsi(Data):
    """
    本函数为获取符型list函数
    :param Data:dic,list,string数据转换为字符型list
    :return: list_imsi
    """
    imsiData = Data
    list_imsi = []
    if type(imsiData) is dict:
        for data in imsiData:
            list_imsi.append(str(data['imsi']))

    elif type(imsiData) is list:

        for data in imsiData:
            if type(data) is dict:
                list_imsi.append(str(data['imsi']))
            if type(data) is str:
                list_imsi.append(str(data))

    elif type(imsiData) is str:
        for data in imsiData.split(','):
            list_imsi.append(data)

    else:
        list_imsi = []

    return list_imsi


def get_allFlower(beginLUnix, endLUnix, list_imsi):
    """

    :param beginLUnix:
    :param endLUnix:
    :param list_imsi:
    :return:
    """
    if not list_imsi:
        return []
    else:
        groupID = {'imsi': "$imsi"}
        matchStages = {'createtime': {'$gte': beginLUnix, '$lte': endLUnix},
                       'imsi': {'$in': list_imsi}
                       }
        pipeline = [
            {"$match": matchStages
             },
            {"$group": {
                "_id": groupID,
                'all': {'$sum': {'$add': ["$userFlower", "$sysFlower"]}}
            }
            }]
        connection = pymongo.MongoClient(sql_info['get140Flower']['uri'])
        aggeData = list(
            connection.get_database(
                sql_info['get140Flower']['db']
            ).get_collection(
                sql_info['get140Flower']['collection']
            ).aggregate(pipeline)
        )
        for i in range(len(aggeData)):
            agg_id_temp = aggeData[i].pop('_id')  # {‘_id’:{}}转换成标准json数据
            aggeData[i].update(agg_id_temp)
            # 流量输出为MB
            aggeData[i]['all'] = round(((aggeData[i]['all']) / 1024 / 1024), 2)
        connection.close()

        return aggeData


def get_USFlower(beginLUnix, endLUnix, list_imsi):
    """

    :param beginLUnix:
    :param endLUnix:
    :param list_imsi:
    :return:
    """
    if not list_imsi:
        return []
    else:
        groupID = {'imsi': "$imsi"}
        matchStages = {'createtime': {'$gte': beginLUnix, '$lte': endLUnix},
                       'imsi': {'$in': list_imsi},
                       'mcc': {"$in": ['311', '310']},
                       'lac': {"$nin": ['0', '10', '60', '208']}
                       }
        pipeline = [
            {"$match": matchStages
             },

            {"$group": {
                "_id": groupID,
                'internalflower': {'$sum': {'$add': ["$userFlower", "$sysFlower"]}}
            }
            }]
        connection = pymongo.MongoClient(sql_info['get140Flower']['uri'])
        aggeData = list(connection.get_database(sql_info['get140Flower']['db']
                                                ).get_collection(
            sql_info['get140Flower']['collection']
            ).aggregate(pipeline))
        for i in range(len(aggeData)):
            agg_id_temp = aggeData[i].pop('_id')                      # {‘_id’:{}}转换成标准json数据
            aggeData[i].update(agg_id_temp)
            # 流量输出为MB
            aggeData[i]['internalflower'] = round(((aggeData[i]['internalflower']) / 1024 / 1024), 2)

        connection.close()

        return aggeData


def get_NotUSFlower(beginLUnix, endLUnix, list_imsi):
    """

    :param beginLUnix:
    :param endLUnix:
    :param list_imsi:
    :return:
    """
    if not list_imsi:
        return []
    else:
        groupID = {'imsi': "$imsi"}
        matchStages = {'createtime': {'$gte': beginLUnix, '$lte': endLUnix},
                       'imsi': {'$in': list_imsi},
                       "$or": [{'mcc': {"$in": ['311', '310']}, 'lac': {"$in": ['0', '10', '60', '208']}},
                               {'mcc': {"$nin": ['311', '310']}}]
                       }
        pipeline = [
            {"$match": matchStages
             },
            {"$group": {
                "_id": groupID,
                'externalflower': {'$sum': {'$add': ["$userFlower", "$sysFlower"]}}
            }
            }]
        connection = pymongo.MongoClient(sql_info['get140Flower']['uri'])
        aggeData = list(connection.get_database(sql_info['get140Flower']['db']
                                                ).get_collection(
            sql_info['get140Flower']['collection']
            ).aggregate(pipeline))
        for i in range(len(aggeData)):
            agg_id_temp = aggeData[i].pop('_id')                            # {‘_id’:{}}转换成标准json数据
            aggeData[i].update(agg_id_temp)
            # 流量输出为MB
            aggeData[i]['externalflower'] = round(((aggeData[i]['externalflower']) / 1024 / 1024), 2)

        connection.close()

        return aggeData


def get_140countryFlower(startDate, stopDate, data):
    """
    本函数用于获取140国卡流量统计接口
    :param startDate: string type datetime from web. Set mongodb begin unix time
    :param stopDate: string type datetime from web. Set mongodb end unix time
    :param data: 为140国卡资源信息表，为最后整合返回数据，后续统计完每张imsi流量记录后更新记录至该data
    :return: 返回最后的统计数据，类型为list dic[{}],{},...]
    """
    """
    beginLUnix and endLUnix is unix timestamp from 1970, is long int types.
    """
    beginLUnix = (datetime_timestamp(startDate)) * 1000
    endLUnix = (datetime_timestamp(stopDate)) * 1000
    imsiData = data
    list_imsi = getlistimsi(imsiData)
    # query total flower and us flower from mongodb
    allFlower = get_allFlower(beginLUnix=beginLUnix, endLUnix=endLUnix, list_imsi=list_imsi)
    usFlower = get_USFlower(beginLUnix=beginLUnix, endLUnix=endLUnix, list_imsi=list_imsi)
    for imsiinfo in imsiData:
        for all_flower in allFlower:
            if all_flower['imsi'] == imsiinfo['imsi']:
                imsiinfo.update({'all': all_flower['all']})
    for imsiinfo in imsiData:
        for us in usFlower:
            if us['imsi'] == imsiinfo['imsi']:
                imsiinfo.update({'internalflower': us['internalflower']})
    for imsiinfo in imsiData:
        if 'all' in imsiinfo.keys():
            if imsiinfo['all'] != 0:
                if 'internalflower' in imsiinfo.keys():
                    imsiinfo.update({'externalflower': (imsiinfo['all'] - imsiinfo['internalflower']),
                                     'percentage': round(
                                         ((imsiinfo['all'] - imsiinfo['internalflower'])/imsiinfo['all']) * 100, 2)
                                     })
                else:
                    imsiinfo.update({'externalflower': imsiinfo['all'],
                                     'percentage': round(((imsiinfo['all']) / imsiinfo['all']) * 100, 2)})

    return imsiData


def get_140countrySrc():
    """
    本函数获取系统中140国卡的imsi、org、state、groupname信息
    :return:
    """

    query_str = ("SELECT  "
                 "DISTINCT (CAST(a.`imsi` AS CHAR)) AS 'imsi',  "
                 "e.`org_name` AS 'org',  "
                 "a.`available_status` AS 'state',  "
                 "(case when a.`occupy_status` = 0 then '未占用' else '已占用' end) AS 'occupy_status', "
                 "GROUP_CONCAT(DISTINCT b.`package_type_name` "
                 "ORDER BY b.`package_type_name` SEPARATOR ';') AS 'package_type', "
                 "c.`name` AS 'groupname'  "
                 "FROM  `t_css_vsim` AS a  "
                 "LEFT  JOIN `t_css_vsim_packages` as b  "
                 "	ON a.`imsi`=b.`imsi`  "
                 "LEFT JOIN `t_css_plmnset` AS c  "
                 "	ON a.`plmnset_id`=c.`id`  "
                 "LEFT JOIN `t_css_operator` AS d  "
                 "	ON a.`operator_id`=d.`id`  "
                 "LEFT JOIN `t_css_group` AS e  "
                 "	ON a.`group_id`=e.`id`  "
                 "WHERE   a.`iso2`='us'  "
                 "	AND b.`package_type_name` LIKE '%140国%'  "
                 "GROUP BY (CAST(a.`imsi` AS CHAR)) "
                 )
    imsiInfo = getJosonData(sys_str=imsiInfo_sysStr,
                            data_base=imsiInfo_Database,
                            query_str=query_str)
    # print query_str
    return imsiInfo


def qury140countryFlowerStatics(begintime, endtime, TimezoneOffset):
    """

    :param begintime:
    :param endtime:
    :param TimezoneOffset:
    :return:
    """
    begindate = begintime
    enddate = endtime
    queryTimezoneOffset = int(TimezoneOffset)
    queryGMTOBeginTime = getGMT0StrTime(str_time=begindate,
                                        off_set=queryTimezoneOffset)
    queryGMTOEndTime = getGMT0StrTime(str_time=enddate,
                                      off_set=queryTimezoneOffset)
    Info140Country = []
    FlowerData = []
    errInfoSrc = ''
    errInfoFlower = ''
    if (not begindate) or (not enddate):
        DicResults = {'info': {'err': True, 'errinfo': '时间参数异常！'}, 'data': []}
        return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)
    else:
        try:
            Info140Country = get_140countrySrc()
        except mysql.connector.Error as err:
            errInfoSrc = "Something went wrong: {}".format(err)
        except:
            errInfoSrc = "Unexpected error"
        if errInfoSrc:
            DicResults = {'info': {'err': True, 'errinfo': errInfoSrc}, 'data': []}
            return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)
        elif not Info140Country:
            errInfoSrc = '系统无套餐名包含140国卡的信息！'
            DicResults = {'info': {'err': True, 'errinfo': errInfoSrc}, 'data': []}
            return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)
        else:
            try:
                FlowerData = get_140countryFlower(startDate=begindate,       # queryGMTOBeginTime,
                                                  stopDate=enddate,          # queryGMTOEndTime,
                                                  data=Info140Country)
            except ValueError:
                errInfoFlower = "input Date Time ValueError"
            except pymongo.errors.OperationFailure:
                errInfoFlower = "DataBase Authentication failed!"
            except pymongo.errors.NetworkTimeout:
                errInfoFlower = "DataBase Connection Exceeded SocketTimeoutMS!"
            except:
                errInfoFlower = "Unexpected error"
            if errInfoFlower:
                DicResults = {'info': {'err': True, 'errinfo': errInfoFlower}, 'data': []}
                return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)
            elif not FlowerData:
                errInfoFlower = '无指定时间范围内140国卡流量使用记录！'
                DicResults = {'info': {'err': True, 'errinfo': errInfoFlower}, 'data': []}
                return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)
            else:
                returnData = FlowerData
                DicResults = {'info': {'err': False, 'errinfo': ''}, 'data': returnData}
                return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)
