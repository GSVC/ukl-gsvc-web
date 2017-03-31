# -*- coding: utf-8 -*-

import json
from bson import json_util
from .SqlPack.SQLModel import qureResultAsJson
import decimal
import mysql.connector


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


def mergeDataFunc(sourData, mergeData, mergekey, mergeindex):
    """

    :param sourData:
    :param mergeData:
    :param mergekey:
    :param mergeindex:
    :return:
    """
    havemeragenum = []
    for i in range(len(sourData)):
        premergeData = {}
        for j in range(len(mergeData)):
            ifmerge = True
            if j in havemeragenum:
                continue
            for key in mergekey:
                if (key in sourData[i].keys()) and (key in mergeData[j].keys()):
                    if sourData[i][key] == mergeData[j][key]:
                        continue
                    else:
                        ifmerge = False
                        break

            if ifmerge:
                havemeragenum.extend([j])  # 核实相同后记录核实行
                for key in mergeindex:
                    if key in mergeData[j].keys():
                        premergeData.update({key: mergeData[j][key]})
                break

        if premergeData != {}:
            sourData[i].update(premergeData)
    return sourData


def qureyNcountrySrcCon(sys_str, database, country, org_name):
    """

    :param sys_str:
    :param database:
    :param country:
    :param org_name:
    :return:
    """

    Country = country
    OrgName = org_name
    countrySet = ''
    orgNameSet = ''
    errInfo = ''
    qurey_result = []
    if Country:
        countrySet = "AND a.`iso2` = '" + Country + "' "
    if OrgName:
        if OrgName == 'all':
            orgNameSet = " "
        else:
            orgNameSet = "AND e.`org_name` = '" + OrgName + "' "
    query_str = (
        "(SELECT "
        "a.`iso2`              AS 'Country', "
        "CASE WHEN 1 THEN concat('1-合计-',a.`iso2`,'-',e.`org_name` ) END  AS 'PackageName', "
        "CASE WHEN 1 THEN '' END  AS 'NextUpdateTime', "
        "CASE WHEN e.`org_name` is null THEN '总计' else e.`org_name` END  AS 'ORG', "
        "COUNT(DISTINCT a.`imsi`) AS 'all_num', "
        "COUNT(DISTINCT (CASE WHEN a.`activate_status` = 1 THEN a.`imsi` END)) AS 'unact_num', "
        "COUNT(DISTINCT (CASE WHEN a.`business_status`= 3 THEN a.`imsi` END)) AS 'flow_unenought_num', "
        "COUNT(DISTINCT (CASE WHEN ((a.`available_status` = '0') "
        "                AND b.`next_update_time` IS NOT NULL "
        "                AND b.`next_update_time` > DATE(NOW())) "
        "                THEN a.`imsi` END)) AS 'ava_num', "
        "CASE WHEN 1 THEN '' END AS 'WarningFlow', "
        "CAST(SUM(CASE WHEN `activate_status` = 0 "
        "              THEN b.`init_flow` "
        "              ELSE 0 END )/1024/1024/1024 AS DECIMAL(64,1))AS 'TotalFlower', "
        "CAST(SUM(b.`total_use_flow`)/1024/1024/1024 AS DECIMAL(64,1)) AS 'UsedFlower', "
        "CAST(SUM(b.`leave_flow`)/1024/1024/1024 AS DECIMAL(64,1))    AS 'LeftFlower', "
        "CAST((SUM(b.`total_use_flow`)/SUM(CASE WHEN `activate_status` = 0 "
        "                                       THEN b.`init_flow` "
        "                                       ELSE 0 END ))*100  AS DECIMAL(64,1)) AS 'Percentage' "
        "FROM `t_css_vsim` AS a "
        "LEFT  JOIN `t_css_vsim_packages` AS b  ON a.`imsi`= b.`imsi` "
        "LEFT  JOIN `t_css_group`         AS e  ON a.`group_id`= e.`id` "
        "LEFT  JOIN `t_css_package_type`  AS c  ON c.`id` = b.`package_type_id` "
        "WHERE   a.`bam_status` = '0' "
        "        AND a.`slot_status` = '0'  " + countrySet + orgNameSet + " "
        "        AND b.`package_type_name` IS NOT NULL "
        "        AND b.`init_flow` is not null "
        "GROUP BY a.`iso2`,e.`org_name` "
        ") "
        "union "
        "( "
        "SELECT "
        "a.`iso2`              AS 'Country', "
        "b.`package_type_name` AS 'PackageName', "
        "DATE_FORMAT(b.`next_update_time`,'%Y-%m-%d %H')  AS 'NextUpdateTime', "
        "e.`org_name`          AS 'ORG', "
        "COUNT(DISTINCT a.`imsi`) AS 'all_num', "
        "COUNT(DISTINCT (CASE WHEN a.`activate_status` = 1 THEN a.`imsi` END)) AS 'unact_num', "
        "COUNT(DISTINCT (CASE WHEN a.`business_status`= 3 THEN a.`imsi` END)) AS 'flow_unenought_num', "
        "COUNT(DISTINCT (CASE WHEN ((a.`available_status` = '0') "
        "                     AND b.`next_update_time` IS NOT NULL "
        "                     AND b.`next_update_time` > DATE(NOW())) "
        "                THEN a.`imsi` END)) AS 'ava_num', "
        "CAST(c.`warning_flow`/1024/1024 AS UNSIGNED) AS 'warning_flow', "
        "CAST(SUM(CASE WHEN `activate_status` = 0 "
        "              THEN b.`init_flow` "
        "              ELSE 0 END )/1024/1024/1024 AS DECIMAL(64,1))AS 'TotalFlower', "
        "CAST(SUM(b.`total_use_flow`)/1024/1024/1024 AS DECIMAL(64,1)) AS 'UsedFlower', "
        "CAST(SUM(b.`leave_flow`)/1024/1024/1024 AS DECIMAL(64,1))    AS 'LeftFlower', "
        "CAST((SUM(b.`total_use_flow`)/SUM(CASE WHEN `activate_status` = 0 "
        "                                       THEN b.`init_flow` "
        "                                        ELSE 0 END ))*100  AS DECIMAL(64,1)) AS 'Percentage' "
        "FROM `t_css_vsim` AS a "
        "LEFT  JOIN `t_css_vsim_packages` AS b  ON a.`imsi`= b.`imsi` "
        "LEFT  JOIN `t_css_group`         AS e  ON a.`group_id`= e.`id` "
        "LEFT  JOIN `t_css_package_type`  AS c  ON c.`id` = b.`package_type_id` "
        "WHERE   a.`bam_status` = '0' "
        "        AND a.`slot_status` = '0'  " + countrySet + orgNameSet + " "
        "        AND b.`package_type_name` IS NOT NULL "
        "        AND b.`init_flow` is not null "
        "GROUP BY a.`iso2`,b.`package_type_name`,DATE_FORMAT(b.`next_update_time`,'%Y-%m-%d %H'), e.`org_name` "
        ") "
        "ORDER BY `Country`, `PackageName`, `ORG` "
    )
    try:
        qurey_result = getJosonData(sys_str,
                                    database,
                                    query_str)

    except KeyError as keyerr:
        errInfo = ("KeyError:{}".format(keyerr))
    except mysql.connector.Error as err:
        errInfo = ("Something went wrong: {}".format(err))
    if errInfo != '':
        DicResults = {'info': {'err': True, 'errinfo': errInfo}, 'data': []}
        return DicResults
    else:
        if not qurey_result:
            DicResults = {'info': {'err': False, 'errinfo': "No Query Data"}, 'data': []}
            return DicResults
        else:
            for cs in qurey_result:
                if type(cs['TotalFlower']) is decimal.Decimal:
                    cs['TotalFlower'] = float(cs['TotalFlower'])
                if type(cs['UsedFlower']) is decimal.Decimal:
                    cs['UsedFlower'] = float(cs['UsedFlower'])
                if type(cs['LeftFlower']) is decimal.Decimal:
                    cs['LeftFlower'] = float(cs['LeftFlower'])
                if type(cs['Percentage']) is decimal.Decimal:
                    cs['Percentage'] = float(cs['Percentage'])

            DicResults = {'info': {'err': False, 'errinfo': errInfo}, 'data': qurey_result}

            return DicResults


def qurycountrySrcCon(country, org_name):
    """

    :param country:
    :param org_name:
    :return:
    """

    # ("统计新架构卡资源：---------------------------------------------------")
    N_countrySrcCon = qureyNcountrySrcCon('config_N',
                                          'glocalme_css',
                                          country,
                                          org_name)

    return json.dumps(N_countrySrcCon, sort_keys=True, indent=4, default=json_util.default)
