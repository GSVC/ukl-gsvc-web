# -*- coding: utf-8 -*-

import json
from bson import json_util
from .SqlPack.SQLModel import qureResultAsJson
import mysql.connector
from .SqlPack.SqlLinkInfo import getonSysSrc as Sql

sql_info = Sql


def getJosonData(sysStr, Database, query_str):
    """==========================================
    sql查询接口函数
    :param sysStr:
    :param Database:
    :param query_str:
    :return:
    =============================================="""
    jsonResults = qureResultAsJson(sysStr=sysStr,
                                   Database=Database,
                                   query_str=query_str,
                                   where=[])
    return jsonResults


def getVsimManulInfor(country, **kwargs):
    """==========================================================
    本部分代码用于获取国家负责人维度卡资源信息模块
    :param country: 前端返回必填国家选项，前端设置了此值不能为空逻辑
    :param kwargs:  后台可选参数，如果后续增加返回值，可以随意添加
    :return:
    ==============================================================="""
    jsonResults = []
    queryPerson = ''
    queryImsi = ''
    personWhere = ''
    imsiWhere = ''
    errInfo = ""
    queryCoutry = country
    if 'person' in kwargs.keys():
        queryPerson = kwargs['person']
    if 'imsi' in kwargs.keys():
        queryImsi = kwargs['imsi']
    # 逻辑判断
    if not queryCoutry:
        errInfo = '请设置查询国家'
    else:
        if queryPerson:
            personWhere = "AND `person_gsvc`=" + "'" + queryPerson + "' "
        if queryImsi:
            imsiWhere = "AND `imsi` LIKE '" + queryImsi + "%' "
        where = "WHERE `country_iso`=" + "'" + queryCoutry + "' " + personWhere + imsiWhere
        query_str = ("SELECT "
                     "`imsi`, "
                     "`country_iso`, "
                     "`country_cn`, "
                     "`person_gsvc`, "
                     "`person_operator`, "
                     "(CASE WHEN `bu_group`='N' THEN 'GTBU' "
                     "WHEN `bu_group`='S' THEN 'S' WHEN `bu_group`='Y' THEN 'Y' END )AS'sys', "
                     "`state`, "
                     "(CASE WHEN `slot_state`=0 THEN '在板' "
                     "WHEN `slot_state`=1 THEN '脱板' WHEN `slot_state`=2 THEN '重复占位' END )AS 'slot_state', "
                     "(CASE WHEN `owner_attr` =0 THEN '否' WHEN `owner_attr` =1 THEN '是' END )AS'owner_attr', "
                     "(CASE WHEN `country_attr` =0 THEN '否' WHEN `country_attr` =1 THEN '是' END )AS'country_attr', "
                     "`vsim_batch_num`, "
                     "`bam_code`, "
                     "`slot_num`, "
                     "`operator`, "
                     "`iccid`, "
                     "`package_type`, "
                     "`charge_noflower`, "
                     "`activated_time`, "
                     "`last_update_time`, "
                     "`next_update_time`, "
                     "`remarks`, "
                     "`phone_num`, "
                     "(CASE WHEN `pay_type`='1' THEN '预付费' WHEN `pay_type`='2' THEN '后付费' END) AS 'pay_type', "
                     "`apn`, "
                     "`shelved_time` "
                     "FROM `vsim_manual_infor` " + where + " "
                     )
        try:
            sysStr = sql_info['getVsimManulInfor']['db']
            Database = sql_info['getVsimManulInfor']['database']
            jsonResults = getJosonData(sysStr=sysStr, Database=Database, query_str=query_str)
        except KeyError:
            errInfo = ("KeyError:{}".format('本地数据库字典配置键值名称有误！'))
        except mysql.connector.Error as err:
            errInfo = ("Something went wrong: {}".format(err))
    if errInfo != '':
        DicResults = {'info': {'err': True, 'errinfo': errInfo}, 'data': []}

        return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)
    else:
        if not jsonResults:
            DicResults = {'info': {'err': False, 'errinfo': "No Query Data"}, 'data': []}

            return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)
        else:
            DicResults = {'info': {'err': False, 'errinfo': errInfo}, 'data': jsonResults}

            return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)


def qureyNVsim(country, imsi, status, business_status, slot_status, bam_status, occupy_status, org, package_status):
    """
    :param country:
    :param imsi:
    :param status:
    :param business_status:
    :param slot_status:
    :param bam_status:
    :param occupy_status:
    :return:
    """
    queryImsi = imsi
    imsiWhere = ''
    statusWhere = ''
    businessStatusWhere = ''
    slotStatusWhere = ''
    bamStatusWhere = ''
    occupyStatusWhere = ''
    orgWhere = ''
    packageStatusWhere = ''
    jsonResults = []
    errInfo = ""
    if not country:
        errInfo = '请设置查询国家！'
    else:
        if queryImsi:
            imsiWhere = "AND a.`imsi` LIKE '" + queryImsi + "%' "
        if status:
            statusWhere = "AND a.`available_status` in (" + status + ") "
        if business_status:
            businessStatusWhere = "AND a.`business_status` in (" + business_status + ") "
        if package_status:
            packageStatusWhere = "AND b.`package_status` in (" + package_status + ") "
        if slot_status:
            slotStatusWhere = "AND a.`slot_status` in (" + slot_status + ") "
        if bam_status:
            bamStatusWhere = "AND a.`bam_status` in (" + bam_status + ") "
        if occupy_status:
            occupyStatusWhere = "AND a.`occupy_status` in (" + occupy_status + ") "
        if org:
            orgWhere = "AND e.`org_name` = '" + org + "' "

        queryStr = ("SELECT "
                    "DISTINCT CAST(a.`imsi` AS CHAR) AS 'imsi', "
                    "a.`iso2`              AS 'country', "
                    "b.`package_type_name`, "
                    "a.`available_status`  AS 'state', "
                    "(CASE WHEN a.`occupy_status`='0' THEN '未占用' "
                    "WHEN a.`occupy_status`='1' THEN '已占用' END"
                    ") AS 'occupy_status', "
                    "(CASE WHEN a.`slot_status`='0' THEN '未拔出' "
                    "WHEN a.`slot_status`='1' THEN '已拔出' END"
                    ") AS 'slot_status', "
                    "(CASE WHEN a.`activate_status`='0' THEN '已激活' WHEN a.`activate_status`='1' THEN '未激活' END"
                    ") AS 'activate_status', "
                    "(CASE WHEN a.`identify_status`='1' THEN '未提交' WHEN a.`identify_status`='2' THEN '待认证' "
                    "WHEN a.`identify_status`='3' THEN '认证通过' WHEN a.`identify_status`='4' THEN '认证失败'  END"
                    ") AS 'identify_status', "
                    "(CASE WHEN a.`business_status`='0' THEN '卡未停用' WHEN a.`business_status`='1' THEN '卡已停用' "
                    "WHEN a.`business_status`='2' THEN '卡预停用' WHEN a.`business_status`='3' THEN '流量不足，停用' "
                    "WHEN a.`business_status`='4' THEN '卡Pending' WHEN a.`business_status`='5' THEN '待测试卡' "
                    "WHEN a.`business_status`='6' THEN '待下架卡' WHEN a.`business_status`='7' THEN '流量封顶停用' END"
                    ") AS 'business_status', "
                    "(CASE WHEN a.`bam_status`='0' THEN 'BAM正常' WHEN a.`bam_status`='1' THEN 'BAM异常' END "
                    ") AS 'bam_status', "
                    "(CASE WHEN b.`package_status`='0' THEN '正常' "
                    "      WHEN b.`package_status`='1' THEN '限速' "
                    "      WHEN b.`package_status`='2' THEN '不可用' "
                    "      WHEN b.`package_status`='3' THEN '套餐过期' END"
                    ") AS 'package_status', "
                    "(CASE WHEN a.`activate_type`='0' THEN '立即激活' ELSE '首次调用激活' END ) AS 'activate_type', "
                    "(CASE WHEN a.`use_locally`='0' THEN '否' WHEN a.`use_locally`='1' THEN '是' END) AS 'use_locally', "
                    "(CASE WHEN a.`vsim_type`='0' THEN '本国卡' WHEN a.`vsim_type`='1' THEN '多国卡' END) AS 'vsim_type', "
                    "CAST(b.`init_flow`/1024/1024 AS UNSIGNED) as 'init_flow', "
                    "CAST(b.`total_use_flow`/1024/1024 AS UNSIGNED) AS 'total_use_flow', "
                    "CAST(b.`leave_flow`/1024/1024 AS UNSIGNED) as 'leave_flow', "
                    "b.`activate_time`, "
                    "b.`update_time`, "
                    "b.`next_update_time`, "
                    "a.`iccid`, "
                    "a.`bam_id` AS 'bam_code', "
                    "CAST(a.`slot_no` AS CHAR)AS 'slot_num', "
                    "e.`org_name`, "
                    "a.`description` AS 'remarks' "
                    "FROM  `t_css_vsim`               AS a "
                    "LEFT  JOIN `t_css_vsim_packages` AS b  ON a.`imsi`=b.`imsi` "
                    "LEFT  JOIN `t_css_group`         AS e  ON a.`group_id`=e.`id` "
                    "WHERE a.`iso2` ="
                    " " + "'" + country + "' " + imsiWhere+statusWhere+businessStatusWhere+slotStatusWhere+
                    bamStatusWhere+occupyStatusWhere+orgWhere+packageStatusWhere)
        try:
            str_db = Sql['qureyNVsim']['db']
            database = Sql['qureyNVsim']['database']
            jsonResults = getJosonData(sysStr=str_db, Database=database, query_str=queryStr)
        except KeyError as keyerr:
            errInfo = ("KeyError:{}".format(keyerr))
        except mysql.connector.Error as err:
            errInfo = ("Something went wrong: {}".format(err))
    if errInfo != "":
        DicResults = {'info': {'err': True, 'errinfo': errInfo}, 'data': []}

        return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)
    else:
        if not jsonResults:
            DicResults = {'info': {'err': False, 'errinfo': "No Query Data"}, 'data': []}

            return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)
        else:
            DicResults = {'info': {'err': False, 'errinfo': errInfo}, 'data': jsonResults}

            return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)


def quryonSysSrc(country, **kwargs):
    """====================================
    查询新架构卡资源状态统计表单API接口
    :param country:
    :return:
    ======================================="""
    # ("查询新架构卡资源：---------------------------------------------------")
    queryImsi = ''
    queryStatus = ''
    queryBusinessStatus = ''
    querySlotStatus = ''
    queryBamStatus = ''
    queryOccupyStatus = ''
    queryOrg = ''
    queryPackageStatus = ''
    if 'imsi' in kwargs.keys():
        queryImsi = kwargs['imsi']
    if 'status' in kwargs.keys():
        queryStatus = kwargs['status']
    if 'business_status' in kwargs.keys():
        queryBusinessStatus = kwargs['business_status']
    if 'slot_status' in kwargs.keys():
        querySlotStatus = kwargs['slot_status']
    if 'bam_status' in kwargs.keys():
        queryBamStatus = kwargs['bam_status']
    if 'occupy_status' in kwargs.keys():
        queryOccupyStatus = kwargs['occupy_status']
    if 'org' in kwargs.keys():
        queryOrg = kwargs['org']
    if 'package_status' in kwargs.keys():
        queryPackageStatus = kwargs['package_status']

    N_VsimPackageRecord = qureyNVsim(country=country,
                                     imsi=queryImsi,
                                     status=queryStatus,
                                     business_status=queryBusinessStatus,
                                     slot_status=querySlotStatus,
                                     bam_status=queryBamStatus,
                                     occupy_status=queryOccupyStatus,
                                     org=queryOrg,
                                     package_status=queryPackageStatus)

    return N_VsimPackageRecord
