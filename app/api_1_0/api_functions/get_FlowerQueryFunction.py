# -*- coding: utf-8 -*-


import json
from bson import json_util
from .SqlPack.SQLModel import qureResultAsJson
import time
import pymongo
import datetime
# 获取连接信息
from .SqlPack.SqlLinkInfo import getFlowerQueryFunction as Sql
# 获取新架构卡资源数据库连接信息
sql_info = Sql


def datetime_timestamp(dt):
    #  dt为字符串标准时间，返回的s为unix时间戳
    #  time.strptime(dt, '%Y-%m-%d %H:%M:%S')
    #  time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28,
    #  tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
    # �?"2012-03-28 06:53:40"转化为时间戳
    try:
        # 此处为了匹配长天格式时间
        s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
    except ValueError:
        # 此处为了匹配短天格式时间
        s = time.mktime(time.strptime(dt, '%Y-%m-%d'))
    return int(s)


def timestamp_datetime(value):
    format1 = '%Y-%m-%d %H:%M:%S'
    format2 = '%Y-%m-%d'
    # value为传入的值为时间戳(整形)，如：1332888820
    structFormate = time.localtime(value)
    # 经过localtime转换后变成结构型时间
    # 最后再经过strftime函数转换为字符型正常日期格式。
    try:
        dt = time.strftime(format1, structFormate)
    except ValueError:
        dt = time.strftime(format2, structFormate)

    return dt


def StrTimeTOUnix(dt, format_str):
    """=====================================

    :param dt:
    :param format_str:
    :return:
    ==============================================="""
    s = time.mktime(time.strptime(dt, format_str))

    return s


def UnixTOStrTime(value, format_str):
    """============================================

    :param value:
    :param format_str:
    :return:
    "==============================================="""
    # 最后再经过strftime函数转换为字符型正常日期格式。
    dt = time.strftime(format_str, time.localtime(value))
    return dt


def getGMT0StrTime(strTime, offSet):
    """=======================================
    :param strTime:
    :param offSet:
    :return:
    ==========================================="""
    try:
        GMT0dateTime = datetime.datetime.strptime(strTime, '%Y-%m-%d %H:%M:%S')-datetime.timedelta(minutes=offSet)
    except ValueError:
        GMT0dateTime = datetime.datetime.strptime(strTime, '%Y-%m-%d') - datetime.timedelta(minutes=offSet)

    return str(GMT0dateTime)


def getlistimsi(Data):
    """===========================

    :param Data:
    :return: list_imsi
    ===================================="""
    imsiData = Data
    list_imsi = []
    if type(imsiData) is dict:
        for data in imsiData:
            list_imsi.append(str(data['imsi']))
    elif type(imsiData) is list:
        for data in imsiData:
            list_imsi.append(str(data))

    elif type(imsiData) is str:
        for data in imsiData.split(','):
            list_imsi.append(data)

    else:
        list_imsi = []

    return list_imsi


def getJosonData(sysStr, Database, query_str):
    """=======================================

    :param sysStr:
    :param Database:
    :param query_str:
    ===========================================
    :return:
    ============================================"""
    jsonResults = qureResultAsJson(sysStr=sysStr,
                                   Database=Database,
                                   query_str=query_str,
                                   where=[])
    return jsonResults


def getHoursFlower(imsi, Begintime, Endtime, Mcc, Plmn, FlowerKey):
    """===================================
    :param imsi: type [],
    :param Begintime:
    :param Endtime:
    :param Mcc: 流量日志表mcc查询条件
    :param Plmn: 流量日志表plmn 查询条件
    :param FlowerKey: mongo group id, 用于添加不同group维度
    =======================================
    :return:
    ======================================="""
    list_imsi = imsi
    returnData = []
    # 查询起始和截止时间
    flowerBegintime = Begintime
    flowerEndtime = Endtime
    queryMcc = Mcc
    queryPlmn = Plmn
    groupItem = FlowerKey
    groupID = {'imsi': "$imsi"}
    if groupItem is None:
        keysNULL = 'NULL'
    else:
        for keys in groupItem:
            if keys == 'plmn':
                addID = {'plmn': "$plmn"}
            elif keys == 'time':
                addID = {'time': "$createtime"}
            elif keys == 'mcc':
                addID = {'mcc': "$mcc"}
            elif keys == 'lac':
                addID = {'lac': "$lac"}
            else:
                continue
            groupID.update(addID)

    # Match Stages Set
    # Unix Time Make
    beginLUnix = (datetime_timestamp(flowerBegintime)) * 1000
    endLUnix = (datetime_timestamp(flowerEndtime)) * 1000
    matchStages = {}
    if queryPlmn and queryMcc:
            matchStages = {'createtime': {'$gte': beginLUnix, '$lte': endLUnix},
                           'imsi': {'$in': list_imsi},
                           'mcc': queryMcc,
                           'plmn': queryPlmn
                           }
    elif queryMcc and not queryPlmn:
            matchStages = {'createtime': {'$gte': beginLUnix, '$lte': endLUnix},
                           'imsi': {'$in': list_imsi},
                           'mcc': queryMcc
                           }
    elif not queryMcc and queryPlmn:
            matchStages = {'createtime': {'$gte': beginLUnix, '$lte': endLUnix},
                           'imsi': {'$in': list_imsi},
                           'plmn': queryPlmn
                           }
    else:
        matchStages = {'createtime': {'$gte': beginLUnix, '$lte': endLUnix},
                       'imsi': {'$in': list_imsi}
                       }
    pipeline = [
        {"$match": matchStages
         },
        {"$group": {
            "_id": groupID,
            'Flower': {'$sum': {'$add': ["$userFlower", "$sysFlower"]}}
        }
        }]
    connection = pymongo.MongoClient(sql_info['queryhourFlower']['uri'])
    aggeData = list(connection.get_database(sql_info['queryhourFlower']['db']
                                            ).get_collection(sql_info['queryhourFlower']['collection']
                                                             ).aggregate(pipeline)
                    )
    for i in range(len(aggeData)):
        agg_id_temp = aggeData[i].pop('_id')                  # {‘_id’:{}}转换成标准json数据
        aggeData[i].update(agg_id_temp)
        aggeData[i]['Flower'] = round(((aggeData[i]['Flower'])/1024/1024), 2)  # 流量输出为MB
        if groupItem is not None:
            if ('time' in groupItem) and ('time' in aggeData[i]):
                aggeData[i]['time'] = timestamp_datetime(aggeData[i]['time']/1000)
    connection.close()

    return aggeData


def getDaysFlower(imsi, Begintime, Endtime, Mcc, Plmn, FlowerKey):
    """

    :param imsi:
    :param Begintime:
    :param Endtime:
    :param Mcc:
    :param Plmn:
    :param FlowerKey:
    :return:
    """
    list_imsi = imsi
    returnData = []
    # 查询起始和截止时间
    flowerBegintime = Begintime
    flowerEndtime = Endtime
    queryMcc = Mcc
    queryPlmn = Plmn
    groupItem = FlowerKey
    groupID = {'imsi': "$imsi"}
    if groupItem is None:
        keysNULL = 'NULL'
    else:
        for keys in groupItem:
            if keys == 'plmn':
                addID = {'plmn': "$plmn"}
            elif keys == 'time':
                addID = {'time': "$createtime"}
            elif keys == 'mcc':
                addID = {'mcc': "$mcc"}
            elif keys == 'lac':
                addID = {'lac': "$lac"}
            else:
                continue

            groupID.update(addID)

    # Match Stages Set---------------------------------------------------
    # Unix Time Make
    beginLUnix = (datetime_timestamp(flowerBegintime)) * 1000
    endLUnix = (datetime_timestamp(flowerEndtime)) * 1000
    if queryPlmn and queryMcc:
            matchStages = {'createtime': {'$gte': beginLUnix, '$lte': endLUnix},
                           'imsi': {'$in': list_imsi},
                           'mcc': queryMcc,
                           'plmn': queryPlmn
                           }
    elif queryMcc and not queryPlmn:
            matchStages = {'createtime': {'$gte': beginLUnix, '$lte': endLUnix},
                           'imsi': {'$in': list_imsi},
                           'mcc': queryMcc
                           }
    elif not queryMcc and queryPlmn:
            matchStages = {'createtime': {'$gte': beginLUnix, '$lte': endLUnix},
                           'imsi': {'$in': list_imsi},
                           'plmn': queryPlmn
                           }
    else:
        matchStages = {'createtime': {'$gte': beginLUnix, '$lte': endLUnix},
                       'imsi': {'$in': list_imsi}
                       }
    pipeline = [
        {"$match": matchStages
         },
        {"$group": {
            "_id": groupID,
            'Flower': {'$sum': {'$add': ["$userFlower", "$sysFlower"]}}
        }
        }]
    connection = pymongo.MongoClient(sql_info['querydayFlower']['uri'])
    aggeData = list(connection.get_database(sql_info['querydayFlower']['db']
                                            ).get_collection(sql_info['querydayFlower']['collection']
                                                             ).aggregate(pipeline)
                    )
    for i in range(len(aggeData)):
        agg_id_temp = aggeData[i].pop('_id')         # {‘_id’:{}}转换成标准json数据
        aggeData[i].update(agg_id_temp)
        aggeData[i]['Flower'] = round(((aggeData[i]['Flower'])/1024/1024), 2)  # 流量输出为MB
        if groupItem is not None:
            if ('time' in groupItem) and ('time' in aggeData[i]):
                aggeData[i]['time'] = timestamp_datetime(aggeData[i]['time']/1000)
    connection.close()

    return aggeData


def getFlowers(querySort, begintime, endtime, mcc, plmn, imsi, flower_query_key, TimezoneOffset):
    """=====================================================================
    gsvc mongodb 流量查询接口函数。完成小时/月维度imsi流量查询，返回查询数据

    ========================================================================
    :param querySort: hour/day 类型的查询，小时或天；
    :param begintime: 起始查询时间hour(yyyy-dd-MM mm:hh:ss), day（yyyy-dd-MM）
    :param endtime: 截止查询时间hour(yyyy-dd-MM mm:hh:ss), day（yyyy-dd-MM）
    :param mcc: 设置查询mcc
    :param plmn: 设置查询plmn
    :param imsi: type: sting , 设置查询imsi,
    :param flower_query_key: 流量查询的附加聚合键值
    :param TimezoneOffset: 时区，相对GMT0时间
    =========================================================================
    :return: 返回带有err，data信息 DicResults = {'info': {'err': False, 'errinfo': errInfo}, 'data': DicData}
    =============================================================================================================="""
    querysort = querySort
    queryBegintime = begintime
    queryEndtime = endtime
    queryMcc = str(mcc)
    queryPlmn = str(plmn)
    queryImsi = getlistimsi(imsi)
    queryFlowerKey = flower_query_key
    queryTimezoneOffset = int(TimezoneOffset)
    # 部署服务器是时间为GMT0时间
    queryGMTOBeginTime = getGMT0StrTime(strTime=queryBegintime, offSet=queryTimezoneOffset)
    queryGMTOEndTime = getGMT0StrTime(strTime=queryEndtime, offSet=queryTimezoneOffset)
    errInfo = ''
    DicData = []
    if (not querysort) or (not queryImsi) or (not queryBegintime) or (not queryEndtime):
        DicResults = {'info': {'err': True, 'errinfo': '存在空类型参数'}, 'data': []}
        return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)
    else:
        if querysort == 'hours':
            try:
                DicData = getHoursFlower(imsi=queryImsi,
                                         Begintime=queryBegintime,
                                         Endtime=queryEndtime,
                                         Mcc=queryMcc,
                                         Plmn=queryPlmn,
                                         FlowerKey=queryFlowerKey)
            except ValueError:
                errInfo = "input Date Time ValueError"        # 'Database Error!'
            except pymongo.errors.OperationFailure:
                errInfo = "DataBase Authentication failed!"
            except pymongo.errors.NetworkTimeout:
                errInfo = "DataBase Connection Exceeded SocketTimeoutMS!"
            except:
                errInfo = "Unexpected error"
            if errInfo:
                DicResults = {'info': {'err': True, 'errinfo': errInfo}, 'data': DicData}
                return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)
            else:
                if DicData:
                    DicResults = {'info': {'err': True, 'errinfo': '无查询结果，请重新设置查询参数'}, 'data': DicData}
                    return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)
                else:
                    DicResults = {'info': {'err': False, 'errinfo': errInfo}, 'data': DicData}
                    return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)
        else:
            try:
                DicData = getDaysFlower(imsi=queryImsi,
                                        Begintime=queryBegintime,
                                        Endtime=queryEndtime,
                                        Mcc=queryMcc,
                                        Plmn=queryPlmn,
                                        FlowerKey=queryFlowerKey)
            except ValueError:
                errInfo = "天维度的短时间日期有问题！"                     # 'Database Error!'
            except pymongo.errors.OperationFailure:
                errInfo = "DataBase Authentication failed!"
            except pymongo.errors.NetworkTimeout:
                errInfo = "DataBase Connection Exceeded SocketTimeoutMS!"
            except:
                errInfo = "Unexpected error"
            if errInfo:
                DicResults = {'info': {'err': True, 'errinfo': errInfo}, 'data': DicData}
                return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)
            else:
                if DicData:
                    DicResults = {'info': {'err': True, 'errinfo': '无查询结果，请重新设置查询参数'}, 'data': DicData}
                    return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)
                else:
                    DicResults = {'info': {'err': False, 'errinfo': errInfo}, 'data': DicData}
                    return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)
