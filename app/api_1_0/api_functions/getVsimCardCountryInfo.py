#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import decimal
from bson import json_util
import mysql.connector
from .SqlPack.SQLModel import qureResultAsJson

S_sysStr = 'config_S'
S_Database = 'ucloudplatform'
N_sysStr = 'config_N'
N_Database = 'glocalme_css'
amzami_sysStr = 'config_amzami'
amzami_Database = 'gsvcdatabase'


def getJosonData(sysStr, Database, query_str):
    """

    :param sysStr:
    :param Database:
    :param query_str:
    :return:
    """
    jsonResults = qureResultAsJson(sysStr=sysStr,
                                   Database=Database,
                                   query_str=query_str,
                                   where=[])
    return jsonResults


def getNVsimCountryStatic(country):
    """

    :param country:
    :return:
    """
    queryCoutry = country

    if queryCoutry == "":
        where = ""
    else:
        where = "AND `iso2`=" + "'" + queryCoutry + "' "

    query_str_vsim = ("SELECT "
                      "a.`iso2` AS 'country', "
                      "COUNT(1) AS 'all_num', "
                      "COUNT(CASE WHEN (a.`available_status`=0 "
                      "                 AND b.`package_status`<>2 "
                      "                 AND a.`business_status`IN('0','4','5') "
                      "                 AND c.`pool_id` IS NOT NULL "
                      "                 AND a.`expire_time`>=NOW() "
                      "                 AND b.`expire_time`>=NOW()) "
                      "           THEN '0' "
                      "      END) AS 'available_num', "
                      "   COUNT(CASE WHEN a.`available_status`=0 "
                      "               AND b.`package_status`<>2 "
                      "               AND a.`business_status`IN('0','4','5') "
                      "               AND c.`pool_id` IS NOT NULL "
                      "               AND a.`expire_time`>=NOW() "
                      "               AND b.`expire_time`>=NOW() "
                      "               AND a.`occupy_status`=0 "
                      "               THEN '1' "
                      "         END) AS 'unoccupy_num' "
                      "FROM `t_css_vsim`AS a "
                      "LEFT  JOIN `t_css_vsim_packages` b "
                      "      ON a.`imsi`=b.`imsi` "
                      "LEFT JOIN `t_css_v_pool_map` AS c "
                      "       ON c.`vsim_id`=a.`id` "
                      "WHERE "
                      "   (b.`package_type_name` NOT  REGEXP '.*[0-9]国.*') " + where + " "
                      "   AND a.`bam_status`=0 "
                      "   AND a.`slot_status`=0 "
                      "   AND a.`vsim_type` = 0 "
                      "   AND a.`dr`=0   "
                      "GROUP BY a.`iso2` "
                      "ORDER BY COUNT(DISTINCT a.`imsi`) DESC ")
    jsonResults_Nvsim = getJosonData(sysStr=N_sysStr, Database=N_Database, query_str=query_str_vsim)

    return jsonResults_Nvsim


def getVsimPackageflowStatus(country):
    """

    :return:
    """
    queryCoutry = country
    if queryCoutry == "":
        where = ""
    else:
        where = "AND `iso2`=" + "'" + queryCoutry + "' "

    query_str_flow = (
        "SELECT "
        "a.`iso2`              AS 'Country', "
        "b.`package_type_name` AS 'PackageName', "
        "DATE_FORMAT(b.`next_update_time`,'%Y-%m-%d %H')  AS 'NextUpdateTime', "
        "e.`org_name`          AS 'ORG', "
        "CAST((SUM(b.`total_use_flow`)/SUM(CASE WHEN `activate_status` = 0 THEN b.`init_flow` ELSE 0 END ))*100  AS DECIMAL(64,1)) AS 'Percentage' "
        "FROM `t_css_vsim` AS a "
        "LEFT  JOIN `t_css_vsim_packages` AS b  ON a.`imsi`= b.`imsi` "
        "LEFT  JOIN `t_css_group`         AS e  ON a.`group_id`= e.`id` "
        "LEFT  JOIN `t_css_package_type`  AS c  ON c.`id` = b.`package_type_id` "
        "WHERE   a.`bam_status` = '0' "
        "        AND a.`slot_status` = '0'  "
        "        " + where + " "
        "        AND b.`package_type_name` IS NOT NULL "
        "        AND b.`init_flow` IS NOT NULL "
        "        AND e.`org_name` = 'GTBU' "
        "GROUP BY a.`iso2`,b.`package_type_name`,DATE_FORMAT(b.`next_update_time`,'%Y-%m-%d %H'), e.`org_name` "
    )

    VsimPackageflowStatus = getJosonData(sysStr=N_sysStr, Database=N_Database, query_str=query_str_flow)

    return VsimPackageflowStatus


def getVsimCountryStatic(country, **kwargs):
    """
    为主页gsvc HOME popchart图形接口
    :param country: 按国家进行数据统计
    :param kwargs: 后续根据需求变化增加变量
    :return:
    """
    queryCoutry = country
    errInfo = ''
    vsimFlowerStatic = []
    try:
        vsimFlowerStatic = getVsimPackageflowStatus(queryCoutry)
    except KeyError as keyerr:
        errInfo = ("when query MaxUser raise KeyError:{}".format(keyerr))
    except mysql.connector.Error as err:
        errInfo = ("Something went wrong when query MaxUser: {}".format(err))
    if errInfo:
        DicResults = {'info': {'err': True, 'errinfo': errInfo},
                      'data': []}
    else:
        if not vsimFlowerStatic:
            DicResults = {'info': {'err': False, 'errinfo': "No Data"},
                          'data': []}

        else:
            for fs in vsimFlowerStatic:
                if type(fs['Percentage']) is decimal.Decimal:
                    fs['Percentage'] = float(fs['Percentage'])

            DicResults = {'info': {'err': False, 'errinfo': ''},
                          'data': vsimFlowerStatic}
    return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)


def getMutiLineNonshelfandAvaCard(country):
    """
    本函数用于获取新架构在架卡状态统计数据：在架卡数、可用卡数
    :param country:
    :return:
    """
    queryCountry = country
    # (当前国家总计卡数、可用卡数数据获取------------------------------GTBU-----------------------------------------)
    query_str_N_onshelfandAvaCard = ("SELECT "
                                     "a.`iso2` AS 'country', "
                                     "COUNT(1) AS 'on_shelf_num', "
                                     "COUNT(CASE WHEN (a.`available_status`=0 "
                                     "                 AND b.`package_status`<>2 "
                                     "                 AND a.`business_status`IN('0','4','5') "
                                     "                 AND c.`pool_id` IS NOT NULL "
                                     "                 AND a.`expire_time`>=NOW() "
                                     "                 AND b.`expire_time`>=NOW()) "
                                     "           THEN '0' "
                                     "      END) AS 'ava_num' "
                                     "FROM `t_css_vsim`AS a "
                                     "LEFT  JOIN `t_css_vsim_packages` b "
                                     "      ON a.`imsi`=b.`imsi` "
                                     "LEFT JOIN `t_css_v_pool_map` AS c "
                                     "      ON c.`vsim_id`=a.`id` "
                                     "WHERE "
                                     "   (b.`package_type_name` NOT  REGEXP '.*[0-9]国.*')"
                                     "   AND a.`iso2`=" + "'" + queryCountry + "' "
                                     "   AND a.`bam_status`=0 "
                                     "   AND a.`slot_status`=0 "
                                     "   AND a.`vsim_type` = 0 "
                                     "   AND a.`dr`=0   "
                                     "GROUP BY a.`iso2` "
                                     )
    jsonResults_N_onshelfandAvaCard = getJosonData(sysStr=N_sysStr,
                                                   Database=N_Database,
                                                   query_str=query_str_N_onshelfandAvaCard)
    return jsonResults_N_onshelfandAvaCard


def getMutiLineSonshelfandAvaCard(country):
    """
    本函数用于获取老系统在架卡状态统计数据：在架卡数、可用卡数
    :param country:
    :return:
    """
    queryCountry = country
    # (当前国家总计卡数、可用卡数数据获取------------------------------S-----------------------------------------)
    query_str_S_onshelfandAvaCard = ("SELECT  "
                                     "a.`country_code2`AS 'country', "
                                     "COUNT(1) AS 'on_shelf_num', "
                                     "COUNT(CASE WHEN  "
                                     " a.`state`='00000' OR a.`state`='10000' THEN 1 END )AS 'ava_num' "
                                     "FROM `t_resvsim` AS a "
                                     "LEFT JOIN `t_resvsimpackagetype`AS c ON c.`itemid`=a.`packagetype` "
                                     "LEFT JOIN `t_resvsimowner`AS e ON e.`sourceid`=a.`imsi` "
                                     "LEFT JOIN `t_resoperator` AS r ON r.`code`=a.`sid` "
                                     "LEFT JOIN `t_usmguser_parent`   AS f    ON f.`uid`=e.`ownerid`  "
                                     "WHERE a.`state` LIKE '_0__0' "  # 在板卡条件
                                     "AND e.`sourceid` IS NULL  "  # 是否代理商卡判断，NULL非代理商卡
                                     "AND (c.`name` NOT  REGEXP '.*[0-9]国.*') "
                                     "AND a.`country_code2`=" + "'" + queryCountry + "'"
                                     "GROUP BY a.`country_code2` ")

    jsonResults_S_onshelfandAvaCard = getJosonData(sysStr=S_sysStr,
                                                   Database=S_Database,
                                                   query_str=query_str_S_onshelfandAvaCard)
    return jsonResults_S_onshelfandAvaCard


def getMutiLineMaxUser(country, begintime, endtime, butype_set, timedim_set):
    """

    :param country:
    :param begintime:
    :param endtime:
    :param butype_set:
    :param timedim_set:
    :return:
    """
    queryCountry = country
    queryBeginTime = begintime
    queryEndTime = endtime
    butype_set = butype_set
    timedim_set = timedim_set
    query_str_MaxUser = (
        "SELECT b.country,"
        "       DATE_FORMAT(b.sampletime, " + timedim_set + ") AS sampletime , "
        "       MAX(b.onlinemax) AS onlinemax "
        "FROM ( "
        "SELECT a.`country`, a.`createtime` AS sampletime, CAST(SUM(a.`onlinemax`) AS UNSIGNED) AS onlinemax "
        "FROM `gsvcdatabase`.`max_onlingusr_hour` AS a "
        "WHERE a.`country`= " + "'" + queryCountry + "' "
        "      AND a.`createtime`>= " + "'" + queryBeginTime + "' " + "AND a.`createtime`<" + "'" + queryEndTime + "' "
        "   " + butype_set +
        "GROUP BY a.`country`, a.`createtime` ) AS b "
        "GROUP BY b.country ,DATE_FORMAT(b.sampletime, " + timedim_set + ")")
    jsonResults_MaxUser = getJosonData(sysStr=amzami_sysStr, Database=amzami_Database, query_str=query_str_MaxUser)

    return jsonResults_MaxUser


def getindexHtmlMutiLineData(country, begintime, endtime, **kwargs):
    """
    :本部分用于获取绘制主页国家峰值曲线图数据。获取国家峰值用户、在板卡数、可用卡数统计数据
    :param country:
    :param begintime:
    :param endtime:
    :param kwargs:
    :return:
    """
    # (maxonline 曲线数据获取)
    BU = ''
    butype_set = " "  # BU类型设置
    timedim_set = "'%Y-%m-%d'"  # 时间维度设置
    MaxUser = []
    VsimCon = []
    errInfo = ''
    if 'butype' in kwargs.keys():
        butype = kwargs['butype']
        BU = kwargs['butype']
        if butype:
            if butype == 'GTBU':
                butype = '2'
                butype_set = butype_set + " AND a.`butype`= " + butype + " "

    if 'timedim' in kwargs.keys():
        timedim = kwargs['timedim']
        if timedim != "":
            if timedim == 'month':
                timedim_set = "'%Y-%m'"
    try:
        MaxUser = getMutiLineMaxUser(country=country,
                                     begintime=begintime,
                                     endtime=endtime,
                                     butype_set=butype_set,
                                     timedim_set=timedim_set)
    except KeyError as keyerr:
        errInfo = ("when query MaxUser raise KeyError:{}".format(keyerr))
    except mysql.connector.Error as err:
        errInfo = ("Something went wrong when query MaxUser: {}".format(err))
    if errInfo:
        DicResults = {'info': {'err': True, 'errinfo': errInfo},
                      'data': []}
    else:
        if not MaxUser:
            DicResults = {'info': {'err': False, 'errinfo': "No MaxUser Data"},
                          'data': []}

        else:
            try:
                if BU == 'ALL':
                    VsimCon = getMutiLineNonshelfandAvaCard(country=country)
                else:
                    VsimCon = getMutiLineNonshelfandAvaCard(country=country)
            except KeyError as keyerr:
                errInfo = ("when query VsimCon raise KeyError:{}".format(keyerr))
            except mysql.connector.Error as err:
                errInfo = ("Something went wrong when query VsimCon: {}".format(err))
            if errInfo:
                DicResults = {'info': {'err': True, 'errinfo': errInfo},
                              'data': []}
            else:
                DicResults = {'info': {'err': False, 'errinfo': ''},
                              'data': {'max_user': MaxUser, 'sim_con': VsimCon}}

    return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)
